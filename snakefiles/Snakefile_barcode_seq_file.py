#_author_='Pedro J Torres 2017'
#make a snakefile for qiime2 example
#rememeber you  need to have python3 and be in qiime2 environment for these scripts to run
# these are for files with foward reads and barcode file not demultiplexed yet

rule all:#dont forget to add this, or else full dataset will not run!
    input:"visualization/taxa-barplot.qzv","taxa-barplot.qzv","core-metrics-results","visualization/beta","visualization/alpha","taxonomy.qza"


rule make_artifacts:
    input:
        "emp-single-end-sequences"
    output:
        "emp-single-end-sequences.qza"
    shell:
        "qiime tools import \
  --type EMPSingleEndSequences \
  --input-path {input} \
  --output-path {output}"

#step2 demultiplex sequences

rule demultiplex:
    input:
        "emp-single-end-sequences.qza"
    output:
        "demux.qza"
    shell:
        "qiime demux emp-single \
    --i-seqs {input}\
    --m-barcodes-file sample-metadata.tsv \
    --m-barcodes-category BarcodeSequence \
    --o-per-sample-sequences {output}"
#
rule demux_summarize:
    input:
        "demux.qza"
    output:
        "demux.qzv"
    shell:
        "qiime demux summarize \
  --i-data {input} \
  --o-visualization {output}"

#step4: sequence qualituy control via dada2
rule seq_quality_control:
    input:
        "demux.qza"
    output:
        "rep-seqs-dada2.qza"
    shell:
        "qiime dada2 denoise-single \
  --i-demultiplexed-seqs {input} \
  --p-trim-left 0 \
  --p-trunc-len 120 \
  --o-representative-sequences {output} \
  --o-table table-dada2.qza"

  #feature data summary
rule feature_table:
    input:
        "table-dada2.qza"
    output:
        "table.qzv"
    shell:
        "qiime feature-table summarize \
  --i-table {input} \
  --o-visualization {output} \
  --m-sample-metadata-file sample-metadata.tsv"

rule tabulate:
    input:
        "rep-seqs-dada2.qza"
    output:
        "rep-seqs.qzv"
    shell:
        "qiime feature-table tabulate-seqs \
  --i-data {input} \
  --o-visualization {output}"

rule alignment:
    input:
        "rep-seqs-dada2.qza"
    output:
        "aligned-rep-seqs.qza"
    shell:
        "qiime alignment mafft \
  --i-sequences {input} \
  --o-alignment {output}"

rule mask:
    input:
        "aligned-rep-seqs.qza"
    output:
        "masked-aligned-rep-seqs.qza"
    shell:
        "qiime alignment mask \
  --i-alignment {input} \
  --o-masked-alignment {output}"

rule phylogeny:
    input:
        "masked-aligned-rep-seqs.qza"
    output:
        "unrooted-tree.qza"
    shell:
        "qiime phylogeny fasttree \
  --i-alignment {input} \
  --o-tree {output}"

rule midpoit:
    input:
        "unrooted-tree.qza"
    output:
        "rooted-tree.qza"
    shell:
        "qiime phylogeny midpoint-root \
  --i-tree {input} \
  --o-rooted-tree {output}"


rule alpha_beta:
    input:
        "rooted-tree.qza"
        #table="table.qza"
    output:
        "core-metrics-results"
    shell:
        "qiime diversity core-metrics-phylogenetic \
  --i-phylogeny {input} \
  --i-table table-dada2.qza \
  --p-sampling-depth 1109 \
  --output-dir {output}"

rule alpha_visualization:
    #input:
    #    "core-metrics-phylogenetic/{sample}_vector.qza"
    output:
        "visualization/alpha"
    shell:
        """
        echo "Running Alpha Visualization"
        mkdir {output}

        qiime diversity alpha-group-significance --i-alpha-diversity core-metrics-results/evenness_vector.qza --m-metadata-file sample-metadata.tsv --o-visualization visualization/alpha/evenness_vector.qzv
        qiime diversity alpha-group-significance --i-alpha-diversity core-metrics-results/faith_pd_vector.qza --m-metadata-file sample-metadata.tsv --o-visualization visualization/alpha/faith_pd_vector.qzv
        qiime diversity alpha-group-significance --i-alpha-diversity core-metrics-results/observed_otus_vector.qza --m-metadata-file sample-metadata.tsv --o-visualization visualization/alpha/observed_otus_vector.qzv
        qiime diversity alpha-group-significance --i-alpha-diversity core-metrics-results/shannon_vector.qza --m-metadata-file sample-metadata.tsv --o-visualization visualization/alpha/shannon_vector.qzv

        """

rule beta_visualization:
    output:
        "visualization/beta"
    shell:
        """
        echo "Running Beta Group Significance"
        mkdir {output}
        qiime emperor plot --i-pcoa core-metrics-results/unweighted_unifrac_pcoa_results.qza --m-metadata-file sample-metadata.tsv --o-visualization visualization/beta/unweighted-unifrac-emperor.qzv
        qiime emperor plot --i-pcoa core-metrics-results/weighted_unifrac_pcoa_results.qza --m-metadata-file sample-metadata.tsv --o-visualization visualization/beta/weighted-unifrac-emperor.qzv
        qiime emperor plot --i-pcoa core-metrics-results/bray_curtis_pcoa_results.qza --m-metadata-file sample-metadata.tsv --o-visualization visualization/beta/bray_curtis-emperor.qzv
        qiime emperor plot --i-pcoa core-metrics-results/jaccard_pcoa_results.qza --m-metadata-file sample-metadata.tsv --o-visualization visualization/beta/jaccard-emperor.qzv
        """
###########################
###Taxonomic Analysis######
###########################
rule feature_classifier:
    input:
        classifier= "taxonomic_classifier/classifier.qza",
        repseq="rep-seqs-dada2.qza"
    output:
        "taxonomy.qza"
    shell:
        """
        echo "Running feature classifier"
        qiime feature-classifier classify-sklearn --i-classifier {input.classifier} --i-reads {input.repseq} --o-classification {output}
        """

rule taxa_barplot:
    input:
        "taxonomy.qza"
    output:
        "visualization/taxa-barplot.qzv"
    shell:
        "qiime taxa barplot --i-table table-dada2.qza --i-taxonomy taxonomy.qza --m-metadata-file sample-metadata.tsv --o-visualization visualization/taxa-barplot.qzv"
