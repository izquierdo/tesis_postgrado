#!/bin/bash

INDIR=casos
OUTFILE=plot3.raw

echo '########' | tee -a ${OUTFILE}

TIME="/usr/bin/time -apo ${OUTFILE}"
PROGRAM=/home/daniel/tesis_postgrado/src/ssdsat/driver.py

#for nviews in `seq 10 5 80`; do
for nviews in `seq 80 5 80`; do
    for nview_sos in `seq 2 5`; do
        VIEWSFILE=${INDIR}/views-$nviews-$nview_sos-6-10-10-3-0.5.txt
        QUERYFILE=${INDIR}/query-$nviews-$nview_sos-6-10-10-3-0.5.txt

        echo ${nviews} ${nview_sos} 6 10 10 3 0.5 | tee -a ${OUTFILE}

        for i in `seq 1`; do #n times to get average
            ${TIME} ${PROGRAM} -t COMPILE -v ${VIEWSFILE} -q ${QUERYFILE}
        done
    done
done
