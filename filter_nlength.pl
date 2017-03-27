## removesmalls.pl
#!/usr/bin/perl
use strict;
use warnings;

my $minlen = shift or die "Error: `minlen` parameter not provided\n";
{
    local $/=">";
    while(<>) {
        chomp;
        next unless /\w/;
        s/>$//gs;
        my @chunk = split /\n/;
        my $header = shift @chunk;
        my $seqlen = length join "", @chunk;
        print ">$_" if($seqlen <= $minlen);
    }
    local $/="\n";
}

# How to use to filter
# perl filter_nlength.pl 293 /Volumes/PBD/PCOS.PhD/PCOS_CH_7_14_16/split_fastq2/seqs.fna> /Volumes/PBD/PCOS.PhD/PCOS_CH_7_14_16/split_fastq2/seqs.293bp.fna


# get a summary
# cat /Volumes/PBD/PCOS.PhD/PCOS_CH_OM_6_20_16/split_fastq/seqs.lengthmax293.fna | grep '^>' | sed 's/_.*//' | sort  | uniq -c > /Volumes/PBD/PCOS.PhD/PCOS_CH_OM_6_20_16/split_fastq/seqs.lengthmax293.txt
