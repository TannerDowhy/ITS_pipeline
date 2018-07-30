#!/bin/bash

#SBATCH --time=12:00:00
#SBATCH --job-name=P2IRC
#SBATCH --mem=64G
#SBATCH --nodes=8
#SBATCH --tasks-per-node=32

# `module load r`;
# `/cvmfs/soft.computecanada.ca/easybuild/software/2017/avx2/Compiler/intel2016.4/r/3.4.3/bin/Rscript $6/dada/dada_sample_inference.R $1 $2 $3 $4 $5`;
/cvmfs/soft.computecanada.ca/easybuild/software/2017/avx2/Compiler/intel2016.4/r/3.4.3/bin/Rscript dada_sample_inference.R ${1} ${2} ${3} ${4} ${5};

exit 0;
