#!/bin/bash

OUTDIR="output/"

echo "Using python version: $(which python3)"
echo "Using Rscript version: $(which Rscript)"

python3 reader.py

if [ ! -d $OUTDIR ]; then
    mkdir $OUTDIR
fi

Rscript calc.R $OUTDIR
