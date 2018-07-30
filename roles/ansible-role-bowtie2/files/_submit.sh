#!/bin/bash

for file in "$1"/merging/output/*extendedFrags.fastq;
    do sbatch --output=/dev/null --account="$3" --dependency=singleton "$1"/bowtie2/bowtie2.sh "$file" "$1";
done;

# for file in "$1"/primer_removal/output/*.fastq.gz;
#     do sbatch --output=/dev/null --account="$3" --dependency=singleton "$1"/bowtie2/bowtie2.sh "$file" "$1";
# done;

exit 0;
