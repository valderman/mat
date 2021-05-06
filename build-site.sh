#!/bin/sh
./mat.py -mv | \
    pandoc -f markdown -t html \
        -V pagetitle:"Lunchdags!" \
        -H templates/head.html \
        -A templates/suffix.html \
        -B templates/prefix.html \
        > menu.html
