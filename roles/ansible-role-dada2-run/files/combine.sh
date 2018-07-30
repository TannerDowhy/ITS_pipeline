#!/bin/bash

# touch "$1"/dada/combined.fastq;
cat "$1"/bowtie2/output/*.fastq > "$1"/dada/combined.fastq;

exit 0;
