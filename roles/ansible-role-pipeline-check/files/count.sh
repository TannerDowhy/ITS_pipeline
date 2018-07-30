#!/bin/bash

declare -i count
count=0

for file in ./*.fastq.gz;
do
        declare -i temp
        temp=$(zcat $file | wc -l)
        temp=$temp/4
        count=$count+$temp
done

echo "$count"

exit 0
