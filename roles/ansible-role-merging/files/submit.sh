#!/bin/bash

# for file in "$1"/primer_removal/output/*_R1*.fastq.gz;
#     do sbatch --output=/dev/null --account="$2" --dependency=singleton "$1"/merging/merge.sh "$file" "$1";
# done;
for file in "$1"/*_R1*.fastq.gz;
    do sbatch --output=/dev/null --account="$2" "$1"/merging/merge.sh "$file" "$1";
done;

exit 0;
