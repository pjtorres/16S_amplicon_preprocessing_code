'''If you have a single fna file with multiple fasta within and want to split up into individual files for each fasta use this script. I modified it to change the header name as well'''
#!usr/bin/env python  
import os

def splitfasta_file(fasta):
    fin=open(fasta,"r")
    count=0
    for line in fin:
        if line.startswith('>'):
            line=line.split('|')
            fout=open("gi"+''+line[1]+"_genomic.tax.fna","w")
            count+=1
            fout.write('>'+line[1]+' '+ line[4]) # this was added to change the name of the fasta header but you can change it to simple fout.write(line) to simply write the fasta header in the original file
        else:
            fout.write(line)
            if line.startswith('>'):
                pass
    fout.close()
    fin.close()
    print "There are "+str(count)+ " fasta headers" 
    return count
        
# splitfasta_file(fasta="/Volumes/Transcend/Candidatus_Bacteroides_periocalifornicus/LIIK01.1.fsa_nt")# change this to file desired
