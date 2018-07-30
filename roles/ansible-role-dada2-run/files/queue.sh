#!/bin/bash

while true
do
    command=`squeue -u $1 | wc -l`
    if [ $command = "1" ];
    then
        break;
    fi
    sleep 10;
done

exit 0;
