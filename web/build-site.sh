#!/bin/sh
../mat.py -mvp ../plugins | \
    pandoc -f markdown -t html \
        -V pagetitle:"Lunchdags!" \
        -H templates/head.html \
        -A templates/suffix.html \
        -B templates/prefix.html \
        > menu.html
