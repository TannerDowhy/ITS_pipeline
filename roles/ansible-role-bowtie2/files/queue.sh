#!/bin/bash

while true
do
    if ["$(squeue -u "$1" | wc -l)" == "1"]
    then
        break;
    fi
    sleep 10;
done

exit 0;
