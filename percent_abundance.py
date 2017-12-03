__author__= 'Pedro J. Torres'
import argparse
import os
import pandas,numpy

"""Script allows you to convert the downloaded csv file obtained from the taxa-bar-plots.qzv in qiime2 and then convert it to percent abundance and transforms it"""
#-----------Command Line Arguments-----------------
parser=argparse.ArgumentParser(description="Script allows you to convert the downloaded csv file obtained from the taxa-bar-plots.qzv in qiime2")
parser.add_argument('-i','--input', help=' Input csv file you want covnert to percentage',required=True)
parser.add_argument('-o','--out', help='Name of output file: jsut the mae e.g., "Percent_taxa-L7"', required=True)#require later
args = parser.parse_args()
o_file=str(args.out)
csvfile=str(args.input) 

#-----------open csv file in with pandas and only include patient and bacteria metadata remove all other metadata information -------
print ("Retrieving percent abundance")
df=pandas.read_csv(csvfile)
cols = [c for c in df.columns if c[0] == 'i' or  c[0] == 'k']
df=df[cols]

#--------------- Convert raw counts to percentages -------
dft=(df.set_index('index').T)
cols= df['index'].tolist()
dft[cols] = dft[cols].div(dft[cols].sum(axis=0), axis=1).multiply(100)# remove this '.multiple(100)' if you only want relative abudnace
dft.to_csv(o_file+'.csv')
print ("Done :)")


