#!/bin/bash

#SBATCH --time=03:00:00
#SBATCH --job-name=P2IRC

python "$3"/primer_removal/adapter_removal.py -a "$1" -b "$3" -f "$2"

exit 0
