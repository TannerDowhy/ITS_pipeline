#!/bin/bash

#SBATCH --time=02:30:00
#SBATCH --job-name=P2IRC
#SBATCH --mem=2G

inp="$1";
file=${inp##*/};
base=${file%_R*.*};
post=${file/_R1/_R2};
two=${base%1_001.*};
path=$(dirname "${1}")

~/bin/flash2 -M 1000 -o $base -d "$2"/merging/output "$1" "$path/$post" > "$2"/merging/stdout/"$base".out;

exit 0;
