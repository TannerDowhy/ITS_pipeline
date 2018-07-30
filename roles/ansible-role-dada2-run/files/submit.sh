#!/bin/bash

# while true
# do
#     if ["$(squeue -u "$2" | wc -l)" == "1"]
#     then
#         break;
#     fi
#     sleep 10;
# done

# echo "Queue empty..."
#
# cat "$1"/bowtie2/output/*.fastq > "$1"/dada/combined.fastq;

# echo "Combined..."
#
# sh "$1"/software/bbmap/readlength.sh in="$1"/dada/combined.fastq out="$1"/dada/hist.txt bin=1;

len=`python $1/dada/read_length.py -f $1/dada/hist.txt`;

`sbatch --account=$2 --output=$1/dada/sample_inference.out $1/dada/dada_sample_inference.sh $1/bowtie2/output 407 $1/dada/plot.png $1/dada/seq_tab.csv $1/dada/seq_tab.rds`;

`sbatch --account=$2 --dependency=singleton --output=$1/dada/chimera_taxonomy.out $1/dada/dada_chimera_taxonomy.sh $1/dada/seq_tab.rds $1/dada/seqtab_final.csv $1/dada/tax_final.csv $1/dada/seqtab_final.rds $1/dada/tax_final.rds $1/dada/tax_gg.csv $1/dada/tax_gg.rds`;

# sh _submit.sh "$1" "$2" "$len";

exit 0;
