#!/bin/bash

sbatch --account="$2" --output="$1"/dada/sample_inference.out "$1"/dada/dada_sample_inference.sh "$1"/bowtie2/out "$3" "$1"/dada/plot.png "$1"/dada/seq_tab.csv "$1"/dada/seq_tab.rds;

sbatch --account="$2" --output="$1"/dada/chimera_taxonomy.out --dependency=singleton "$1"/dada/dada_chimera_taxonomy.sh "$1"/dada/seq_tab.rds "$1"/dada/seqtab_final.csv "$1"/dada/tax_final.csv "$1"/dada/seqtab_final.rds "$1"/dada/tax_final.rds;

exit 0;
