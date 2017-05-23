'''If you have a single fna file with multiple fasta within and want to split up into individual fies for each fasta use this script. I modified it to change the name'''
import os

def splitfasta_file(fasta):
    fin=open(fasta,"r")
    count=0
    for line in fin:
        if line.startswith('>'):
            fout=open(line[1:15]+"_genomic.tax.fna","w")
            count+=1
            fout.write(line[0]+'NZ_'+line[4:12]+"|kraken:taxid|"+str(count)+" Candidatus Bacteroides periocalifornicus, "+'contig '+str(count)+'\n') # this was added to change the name of the fasta header but you can change it to simple fout.write(line) to simply write the fasta heaer in the original file
        else:
            fout.write(line)
            sfasta[header]= line
            if line.startswith('>'):
                pass
    fout.close()
    fin.close()
    print "There are "+str(count)+ " fasta headers" 
    return count
        
splitfasta_file(fasta="/Volumes/Transcend/Candidatus_Bacteroides_periocalifornicus/LIIK01.1.fsa_nt")# change this to file desired
