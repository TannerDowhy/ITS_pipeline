#!/bin/bash

# Get the size of Undeterminded files
# undeterminded="$(ls -1 "$1"/Undetermined* | wc -l)";
# if ("$undetermined" != 0):
#   echo "WARNING: There exists "$undetermined" undetermined files. The size(s) are: stat --printf="%s " "$1"/Undetermined*"

# Counts the number of files at each stage in the pipeline
files_in="$(ls -1 "$1"/*fastq.gz | wc -l)";
r1_files_in="$(ls -1 "$1"/*_R1*fastq.gz | wc -l)";
r2_files_in="$(ls -1 "$1"/*_R2*fastq.gz | wc -l)";

files_cut="$(ls -1 "$1"/primer_removal/output/*fastq.gz | wc -l)";
r1_files_cut="$(ls -1 "$1"/primer_removal/output/*_R1*fastq.gz | wc -l)";
r2_files_cut="$(ls -1 "$1"/primer_removal/output/*_R2*fastq.gz | wc -l)";

files_merge="$(ls -1 "$1"/merging/output/*extendedFrags.fastq | wc -l)";
files_contam="$(ls -1 "$1"/bowtie2/output/*.fastq | wc -l)";

# Make sure right number of files at each level
if ("$files_cut" != "$files_in")
then
  echo "Error at primer removal step. Wrong number of output files." >> "$1"/pipeline_check/pipeline.out
  exit 1;
fi
if ("$files_merge" != "$files_in" / 2)
then
  echo "Error at merging step. Wrong number of output files." >> "$1"/pipeline_check/pipeline.out
  exit 1;
fi
if ("$files_contam" != "$files_merge" / 2)
then
  echo "Error at contaminant detection step. Wrong number of output files." >> "$1"/pipeline_check/pipeline.out
  exit 1;
fi

# Count the molecules at each level
declare -1 total_in;
total_in=0;
for file in "$1"/*.fastq.gz;
do
  declare -i temp
  temp=$(zcat $file | wc -l)
  temp=$temp/4
  total_in=$(($total_in+$temp))
done
echo "${total_in} total initial molecules." >> "$1"/pipeline_check/pipeline.out

declare -i r1_in;
r1_in=0;
for file in "$1"/*_R1*.fastq.gz;
do
  declare -i temp
  temp=$(zcat $file | wc -l)
  temp=$temp/4
  r1_in=$(($r1_in+$temp))
done
echo "${r1_in} initial forward molecules." >> "$1"/pipeline_check/pipeline.out

declare -1 r2_in;
r2_in=0;
for file in "$1"/*_R2*.fastq.gz;
do
  declare -i temp
  temp=$(zcat $file | wc -l)
  temp=$temp/4
  r2_in=$(($r2_in+$temp))
done
echo "${r2_in} initial reverse molecules." >> "$1"/pipeline_check/pipeline.out

declare -i post_cut;
post_cut=0;
for file in "$1"/primer_removal/output/*.fastq.gz;
do
  declare -i temp
  temp=$(zcat $file | wc -l)
  temp=$temp/4
  post_cut=$(($post_cut+$temp))
done
echo "${post_cut} molecules after primer removal." >> "$1"/pipeline_check/pipeline.out

declare -i post_cut_r1;
post_cut_r1=0;
for file in "$1"/primer_removal/output/*_R1*.fastq.gz;
do
  declare -i temp
  temp=$(zcat $file | wc -l)
  temp=$temp/4
  post_cut_r1=$(($post_cut_r1+$temp))
done
echo "${post_cut_r1} reads post primer removal." >> "$1"/pipeline_check/pipeline.out

declare -i post_merge;
post_merge=0;
for file in "$1"/merging/output/*extendedFrags.fastq;
do
  declare -i temp
  temp=$(cat $file | wc -l)
  temp=$temp/4
  post_merge=$(($post_merge+$temp))
done
echo "${post_merge} reads post merging." >> "$1"/pipeline_check/pipeline.out

declare -i post_contam;
post_contam=0;
for file in "$1"/bowtie2/output/*.fastq;
do
  declare -i temp
  temp=$(cat $file | wc -l)
  temp=$temp/4
  post_contam=$(($post_contam+$temp))
done
echo "${post_merge} reads post contaminant removal." >> "$1"/pipeline_check/pipeline.out


exit 0;
