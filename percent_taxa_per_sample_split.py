__author__= 'Pedro J. Torres'
import argparse
import os
import pandas,numpy

"""Script allows you to take in an output file from qiime2 barplots and split each
sample into its own file with the raw counts in one row and the percent abudnance in another."""

#-----------Command Line Arguments-----------------
parser=argparse.ArgumentParser(description="This script uses  numpy and pandas. Make sure both are installed. Script will make an individual file for each sample from a qiime2 barplot otput and give their raw counts and percent abudnances. - Pedro J. Torres")
parser.add_argument('-i','--input', help=' Input csv file you want to split',required=True)
args = parser.parse_args()
csvfile=str(args.input) #name of fasta file want to change

#---------Rearrange Taxa category to make it easier to parse-----
print ('split script has started ...')
fin=open(csvfile, 'rU')
fout=open('temp1.csv','w+')
header=fin.readline()
fout.write('Taxa'+','+header[48:])


#This will re organize the file to make it easier to transform our data sicne K,P,C,O ECT.. are tab delimeted
for line in fin:
    line= line.split(',')
    taxa=line[:6]
    taxa=(";".join(taxa))#taxa is now ';' seperated
    taxa=taxa.strip('\n')
    taxabundance=line[6:]# this is all our taxa abundance
    taxabundance=(",".join(taxabundance))
    newline=taxa+'\t'+taxabundance
    fout.write(newline)
 

fout.close()
fin.close()

#------------Temp file will be transformed in pandas to split easier-----
df=pandas.read_csv('temp1.csv')
dft=(df.set_index('Taxa').T)
dft.to_csv('temp.csv')
os.remove("temp1.csv")# remove old temp file from before

#-------------- Split columns into different Temp files based on sample ------
fin2=open('temp.csv', 'rU')
fout2=open('tmp2.csv', 'w+')
header=fin2.readline()
header= header.strip(',').replace('\t','_').replace(" ","_")
heads="SampleID"+','+header
heads=heads.split(',')
heads= '\t'.join(heads)
for line in fin2:
    linesplit= line.split(',')
    filename = linesplit[0]# nme of file
    fout2=open(filename+".tmp.csv",'w+')
    rowinfo ="\t".join(linesplit)
    fout2.write(heads)
    fout2.write(rowinfo)
fin2.close()
fout2.close()

#---------------- Make Final file with Taxa, raw counts, and percetn abundance
os.remove('temp.csv')
os.remove('tmp2.csv')
F=[i for i in os.listdir('.') if i.split('.')[-2]=='tmp']
count=0
for f in F:
    count += 1
    try:
        colname=f.split('.')[0]
        newfile= f.split('.')[0]+'_percent.csv'
        df=pandas.read_table(f, sep='\t')
        dft=(df.set_index('SampleID').T)
        dft = dft.sort_values(colname, ascending=False)
        dft['Percent']= (dft[colname]/dft[colname].sum())*100
        dft.to_csv(newfile)
        os.remove(f)
    except pandas.io.common.EmptyDataError:
        print (f, " is empty")

print ('Done :)')
print ("There are " + str(count)+ " samples")
