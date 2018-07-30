#!/bin/bash

#SBATCH --time=2:00:00
#SBATCH --job-name=P2IRC
#SBATCH --mem=2G

inp="$1";
file=${inp##*/};
base=${file%*.extended*};
# base=${file%*.cutadapted*};
path=$(dirname "${1}");

module load bowtie2;
bowtie2 -x "$2"/bowtie2/contaminants_indx "$1" --un "$2"/bowtie2/output/"$base".fastq > "$2"/bowtie2/sam/"$base".out;

exit 0;
