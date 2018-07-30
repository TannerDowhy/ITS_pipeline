#!/bin/bash

for file in "$1"/*_R1*.fastq.gz;
    do sbatch --account="$3" "$1"/primer_removal/run_adapter.sh "$2" "$file" "$1"; 
done;

exit 0;
