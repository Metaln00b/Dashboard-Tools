#!/bin/bash

for j in {0..2047..1}
do
    for i in {0..240..1}
    do
        #echo $(printf "%x %x" $j $i)
        cansend can0 $(printf "%03x#82%02xf110891C" $j $i)
    done
done
##22 read data by identifier
##2e 

#7e oder 7f bei fehler oderso

#02 3e 00 und den rest mit 0 