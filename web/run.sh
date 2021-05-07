#!/bin/sh
./update-menu.sh &
nginx -g 'daemon off;'
