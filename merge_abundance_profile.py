'''This script allows the merging of multiple blastn output files, while simultaneously allowing the addition of a zero to samples which did not recieve a hit found in other samples''' 

import os


taxa={}

F=[i for i in os.listdir(os.curdir) if i.split(".")[-1]=="txt"]
for myfile in F:
    f=open(myfile,"r")
    f.readline()
    for line in f:
	#print line        
	line=line.strip()
        line=line.split("|")
	num=line[0].replace("ref","")
        #print num
	if line[2] not in taxa:
            taxa[line[2]]=[0]*len(F)
        else:pass
        taxa[line[2]][F.index(myfile)]+=float(num)

o=open("Combined_Abundance.xls","w+")
o.write("Gene_name\t"+"\t".join(F)+"\n")
for i in taxa:
    o.write(i+"\t"+"\t".join([str(xx) for xx in taxa[i]])+"\n")
o.close()

