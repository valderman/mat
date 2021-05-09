#!/bin/sh
export DATETIME=`date +'%Y-%m-%d, %H:%M:%S'`

case `date +%a` in
Mon)
    export WEEKDAY="Måndag"
    ;;
Tue)
    export WEEKDAY="Tisdag"
    ;;
Wed)
    export WEEKDAY="Onsdag"
    ;;
Thu)
    export WEEKDAY="Torsdag"
    ;;
Fri)
    export WEEKDAY="Fredag"
    ;;
esac

cat templates/head.html | envsubst > _head.html
cat templates/suffix.html | envsubst > _suffix.html
cat templates/prefix.html | envsubst > _prefix.html

../mat.py -mvp ../plugins | \
    pandoc -f markdown -t html \
        -V pagetitle:"Lunchdags!" \
        -H _head.html \
        -A _suffix.html \
        -B _prefix.html \
        > menu.html

rm _head.html _suffix.html _prefix.html