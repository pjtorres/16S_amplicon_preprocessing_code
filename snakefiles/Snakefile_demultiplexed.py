#_author_= 'Pedro J. Torres  2017)

# Persephone Biome 16S pipeline. R1 reads. Make sure dependencies have been meet
# and that you are inside a qiime environment

rule all:#dont forget to add this, or else full dataset will not run!
    input:"rooted-tree.qza","demux.qzv","core-metrics-results","visualization/beta","visualization/alpha","visualization/taxa","taxonomy.qza"
    #input:"rooted-tree.qza","demux.qzv","visualization/taxa-barplot.qzv","core-metrics-results","visualization/beta","visualization/alpha","taxonomy.qza"
    #input:"taxa-barplot.qzv","demux.qzv","rep-seqs-dada2.qza","rooted-tree.qza","core-metrics-results","taxonomy.qza"
#        ""

######################################
## Make qiime2 artifacts from R1 reads
######################################
rule make_artifacts:
    input:
        "R1_files"
    output:
        "demux-single-end.qza"
    message:
        "Welcome to the Persephone Biome 16S rRNA Pipeline. Make sure all your dependencies are meet and that you have all the proper files in their proper folder. If unsure look at the jupyter notebook tutorial."
    shell:
        "qiime tools import \
  --type 'SampleData[SequencesWithQuality]' \
  --input-path {input} \
  --source-format CasavaOneEightSingleLanePerSampleDirFmt \
  --output-path {output}"
######################################
## Summarize demultiplexed data
######################################
rule summarize_demux:
    input:
        "demux-single-end.qza"
    output:
        "demux.qzv"
    shell:
        "qiime demux summarize \
  --i-data {input} \
  --o-visualization {output}"

######################################
## Denoise Using DADA2
######################################
rule denoise_single:
    input:
        "demux-single-end.qza"
    output:
        rep="rep-seqs-dada2.qza",
        table="table-dada2.qza"
    message:
        "This is a very long step. Your sequences are being analyzed for sequencing errors, duplicates and chimeras. Will remove spurious OTUs and reduce inflation commonly associated with OTU clustering. Will also reduce dataset size so don't be alarmed if you notice this. It is necessary. Make sure you are in a 'screen' like environment or do not close your computer. Depending on the data size and computer strength this could take little to a long time. Don't be worried if it takes a while."
    shell:
        "qiime dada2 denoise-single \
    --i-demultiplexed-seqs {input} \
    --p-trim-left 12 --p-trunc-len 220 \
    --o-representative-sequences {output.rep}\
    --o-table {output.table}"

######################################
## Summarize feature tables and rep seqs
######################################
rule table_summary:
    input:
        "table-dada2.qza"
    output:
        "table-dada2.qzv"
    shell:
        "qiime feature-table summarize \
  --i-table  {input} \
  --o-visualization  {output} \
  --m-sample-metadata-file Mapping_file.txt"

rule rep_summary:
    input:
        "rep-seqs-dada2.qza"
    output:
        "rep-seqs-dada2.qzv"
    shell:
        "qiime feature-table tabulate-seqs \
  --i-data  {input} \
  --o-visualization  {output}"

######################################
## Generate phylogenetic tree
######################################
rule phylogenetic_tree:
    input:
        "rep-seqs-dada2.qza"
    output:
        "aligned-rep-seqs.qza"
    message:
        "Next steps will generate phylogenetic tree."
    shell:
        "qiime alignment mafft \
  --i-sequences {input} \
  --o-alignment {output}"

rule alignment:
    input:
        "aligned-rep-seqs.qza"
    output:
        "masked-aligned-rep-seqs.qza"
    shell:
        "qiime alignment mask \
  --i-alignment {input} \
  --o-masked-alignment {output}"

rule phylogeny_fasttree:
    input:
        "masked-aligned-rep-seqs.qza"
    output:
        "unrooted-tree.qza"
    shell:
        "qiime phylogeny fasttree \
  --i-alignment {input} \
  --o-tree {output}"

rule midpoint:
    input:
        "unrooted-tree.qza"
    output:
        "rooted-tree.qza"
    shell:
        "qiime phylogeny midpoint-root \
  --i-tree {input} \
  --o-rooted-tree {output}"

######################################
## Core diversity Metrics
######################################
rule alpha_beta_metrics:
    input:
        tree="rooted-tree.qza",
        table="table-dada2.qza"
    output:
        "core-metrics-results"
    shell:
        "qiime diversity core-metrics \
  --i-phylogeny {input.tree} \
  --i-table {input.table} \
  --p-sampling-depth 2500 \
  --output-dir {output}"

######################################
## Alpha and beta Visualization
######################################
rule alpha_visualization:
    #input:
    #    "core-metrics-phylogenetic/{sample}_vector.qza"
    output:
        "visualization/alpha"
    shell:
        """
        echo "Running Alpha Visualization"
        mkdir {output}

        qiime diversity alpha-group-significance --i-alpha-diversity core-metrics-results/evenness_vector.qza --m-metadata-file Mapping_file.txt --o-visualization visualization/alpha/evenness_vector.qzv
        qiime diversity alpha-group-significance --i-alpha-diversity core-metrics-results/faith_pd_vector.qza --m-metadata-file Mapping_file.txt --o-visualization visualization/alpha/faith_pd_vector.qzv
        qiime diversity alpha-group-significance --i-alpha-diversity core-metrics-results/observed_otus_vector.qza --m-metadata-file Mapping_file.txt --o-visualization visualization/alpha/observed_otus_vector.qzv
        qiime diversity alpha-group-significance --i-alpha-diversity core-metrics-results/shannon_vector.qza --m-metadata-file Mapping_file.txt --o-visualization visualization/alpha/shannon_vector.qzv

        """

rule beta_visualization:
    output:
        "visualization/beta"
    shell:
        """
        echo "Running Beta Group Significance"
        mkdir {output}
        qiime emperor plot --i-pcoa core-metrics-results/unweighted_unifrac_pcoa_results.qza --m-metadata-file Mapping_file.txt --o-visualization visualization/beta/unweighted-unifrac-emperor.qzv
        qiime emperor plot --i-pcoa core-metrics-results/weighted_unifrac_pcoa_results.qza --m-metadata-file Mapping_file.txt --o-visualization visualization/beta/weighted-unifrac-emperor.qzv
        qiime emperor plot --i-pcoa core-metrics-results/bray_curtis_pcoa_results.qza --m-metadata-file Mapping_file.txt --o-visualization visualization/beta/bray_curtis-emperor.qzv
        qiime emperor plot --i-pcoa core-metrics-results/jaccard_pcoa_results.qza --m-metadata-file Mapping_file.txt --o-visualization visualization/beta/jaccard-emperor.qzv
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
        "visualization/taxa"
    shell:
        """
        mkdir {output}
        qiime taxa barplot --i-table table-dada2.qza \
        --i-taxonomy taxonomy.qza --m-metadata-file Mapping_file.txt  \
        --o-visualization visualization/taxa/taxa-barplot.qzv

        """
