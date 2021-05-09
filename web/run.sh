#!/bin/bash
./update-menu.sh &
nginx -g 'daemon off;'
