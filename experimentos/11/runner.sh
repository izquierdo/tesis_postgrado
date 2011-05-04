#!/bin/bash

INDIR=casos
OUTFILE=plot1.raw

echo '########' | tee -a ${OUTFILE}

TIME="/usr/bin/time -apo ${OUTFILE}"
PROGRAM=/home/daniel/tesis_postgrado/src/ssdsat/driver.py

for vistas in `seq 10 10 100`; do
    for pasos in `seq 2 5`; do
        VIEWSFILE=${INDIR}/views-${vistas}-${pasos}.txt
        QUERYFILE=${INDIR}/query-${vistas}-${pasos}.txt

        echo ${vistas} ${pasos} | tee -a ${OUTFILE}

        for i in `seq 1`; do #n times to get average
            ${TIME} ${PROGRAM} -t COMPILE -v ${VIEWSFILE} -q ${QUERYFILE}
        done
    done
done
