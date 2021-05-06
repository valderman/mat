#!/bin/sh
./mat.py -mv | pandoc -f markdown -t html -H templates/head.html -A templates/suffix.html -B templates/prefix.html > menu.html
