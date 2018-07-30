#!/bin/bash

while true
do
    if ["$(squeue -u "$1" | grep "$2" | wc -l)" == "0"]
    then
        break;
    fi
    sleep 10;
done

exit 0;
