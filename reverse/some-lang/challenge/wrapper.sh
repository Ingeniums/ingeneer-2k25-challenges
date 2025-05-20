#!/bin/sh


timeout 60 sh -c '
    echo -n "Enter code: "
    read  code
    stdbuf -o0 ./rev "$code"
    echo -n "Good programmer, but not good enough\n"
    exit
'
