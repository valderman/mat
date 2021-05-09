#!/bin/bash
while true ; do
    ./build-site.sh
    mv menu.html /usr/share/nginx/html/index.html
    sleep 30m
done
