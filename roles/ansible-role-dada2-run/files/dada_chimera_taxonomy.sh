#!/bin/bash

#SBATCH --time=1:00:00
#SBATCH --job-name=P2IRC
#SBATCH --mem=64G
#SBATCH --nodes=4
#SBATCH --tasks-per-node=32

# module load r;
# /cvmfs/soft.computecanada.ca/easybuild/software/2017/avx2/Compiler/intel2016.4/r/3.4.3/bin/Rscript $8/dada/dada_chimera_taxonomy.R $1 $2 $3 $4 $5 $6 $7;
/cvmfs/soft.computecanada.ca/easybuild/software/2017/avx2/Compiler/intel2016.4/r/3.4.3/bin/Rscript dada_chimera_taxonomy.R ${1} ${2} ${3} ${4} ${5} ${6} ${7};

exit 0;
