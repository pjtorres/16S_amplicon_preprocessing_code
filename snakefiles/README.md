Recieve a single fastq file from core (no barcode file and not yet demultiplexed). Can follow example [here](https://forum.qiime2.org/t/problems-with-fastq-files-paired-end-without-barcode-file/960/2)

In short you will need to extract your barcodes from your singel fastq file. I used 12bp golay barcodes so I use this command in qiime1:

```python
extract_barcodes.py -f <file.fastq> \
                    -c barcode_single_end \
                    --bc1_len 12 \
                    -o split_files \
                    -m mappingfile.txt
```

Now for the Snakefile in this directory to work we will rename our files and make a new directory. And change the name of your mappingfile  file

```bash
  mv reads.fastq sequences.fastq #Change name of reads.fastq file in the split_files/ folder after running the above code
  
  gzip sequences.fastq 

  gzip barcodes.fastq 

  mkdir emp-single-end-sequences # make this directory and move the sequences and barcodes file into this directory

  mv sequences.fastq.gz emp-single-end-sequences

  mv barcodes.fastq.gz emp-single-end-sequences

  cp mapping_file.txt sample-metadata.tsv #Change name of mapping file
```
Now make sure the folder taxonomic_classifier is int the same directory.

In your current folder you should have
emp-single-end-sequences/   sample-metadata.tsv  Snakefile  taxonomic_classifier/

Then you can run:
```bash
snakemake
```
