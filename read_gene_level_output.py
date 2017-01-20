'''
Created on 20 Jan 2017

@author: aled
'''
class read_gene_level():
    def __init__(self):
        # chanjo output
        self.chanjo_output="/home/aled/Downloads/epilepsy_mid_bams/epilepsy_gene_out.json"
        #output file
        self.output="/home/aled/Downloads/epilepsy_mid_bams/gene_coverage.txt"
        #a sambamba file to translate entrez id to gene symbol
        self.sambamba_file="/home/aled/Downloads/epilepsy_mid_bams/NGS118c_48_87777_CH_Epi1_S16_R1_001.refined.bam.sambamba_output.bed.2"
        
        #dictionaries to populate
        self.dict={}
        self.gene_entrez={}
        
    def summarise(self):
        # open chanjo output
        chanjo_out=open(self.chanjo_output,'r')
        #open output file
        output_file=open(self.output,'w')
        
        #loop through chanjo output file
        for line in chanjo_out:
            #capture entrez id
            entrezid=int(line.split("{")[2].replace("\"","").replace(": ",""))
            #capture the mean coverage
            coverage=float(line.split("mean_coverage\": ")[1].split("}")[0])
            #create a list for each gene
            if entrezid in self.dict:
                self.dict[entrezid].append(coverage)
            else:
                self.dict[entrezid]=[coverage]
        chanjo_out.close()
        
        #open sambamba file
        sambamba=open(self.sambamba_file,'r')
        for line in sambamba:
            if line.startswith("#"):
                pass
            else:
                #create a dict with entrez as a key and gene symbol as a value
                splitline=line.split("\t")
                self.gene_entrez[int(splitline[7])]=splitline[6]
        
        #write header to output file                
        output_file.write("Gene\taverage_coverage\n")
        
        #loop through dict
        for gene in self.dict:
            #calculate average coverage for this gene
            average_coverage=sum(self.dict[gene])/len(self.dict[gene])
            #write to file
            output_file.write(str(self.gene_entrez[gene])+"\t"+str(average_coverage)+"\n")
            
if __name__ == '__main__':
    a=read_gene_level()
    a.summarise()