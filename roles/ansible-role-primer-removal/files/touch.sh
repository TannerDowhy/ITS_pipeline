#!/bin/bash


for file in "$1"/*.fastq.gz;
do
  inp="$file";
  file_name=${inp##*/};
  base=${file_name%.fastq.gz};
  touch $1/primer_removal/output/$base.cutadapted.fastq.gz;
done

exit 0;
