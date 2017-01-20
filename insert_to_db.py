'''
Created on 20 Jan 2017

@author: aled
'''
import MySQLdb
import os

class Insert():
    def __init__(self):
        #  define parameters used when connecting to database
        self.host = "127.0.0.1"
        self.port = int(3306)
        self.username = "root"
        self.passwd = "mysql"
        self.database = "170120_epilepsy"
        
        self.folder="/home/aled/Downloads/epilepsy_mid_bams/"
    
    def find_sambamba_files(self):
        for file in os.listdir(self.folder):
            if file.endswith("sambamba_output.bed"):
                sambambafile=open(self.folder+file)
                for line in sambambafile:
                    if line.startswith("#"):
                        pass
                    else:
                        splitline=line.split("\t")
                        chr=splitline[0]
                        start=splitline[1]
                        stop=splitline[2]
                        pos=splitline[3]
                        gene=splitline[6]
                        entrez=splitline[7]
                        readcount=splitline[8]
                        meancov=splitline[9]
                        percent30=splitline[10]
                        samplename=file.replace(".refined.bam.sambamba_output.bed","")
                         
                        # open connection to database and run SQL statement
                        db = MySQLdb.Connect(host=self.host, port=self.port, user=self.username, passwd=self.passwd, db=self.database)
                        cursor = db.cursor()
                        
                        sql_insert="insert into sambamba_output(Chr,start,stop,Pos,Gene,EntrezID,readcount,meanCoverage,percentage30,samplename) values ('"+chr+"',"+start+","+stop+",'"+pos+"','"+gene+"',"+entrez+","+readcount+","+meancov+","+percent30+",'"+samplename+"')"
                        
                        #print sql_insert
                        try:
                            cursor.execute(sql_insert)
                            db.commit()
                        except MySQLdb.Error, e:
                            db.rollback()
                            print "fail - unable to insert "
                            if e[0] != '###':
                                raise
                        finally:
                            db.close()

if __name__ == '__main__':
    a=Insert()
    a.find_sambamba_files()
    