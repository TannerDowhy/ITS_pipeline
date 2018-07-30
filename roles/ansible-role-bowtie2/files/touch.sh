#!/bin/bash


for file in "$1"/*_R1*.fastq.gz
# for file in "$1"/*.fastq.gz
do
  inp="$file";
  file_name=${inp##*/};
  base=${file_name%_R1*};
  touch $1/bowtie2/output/$file_name.fastq;
done

exit 0;
