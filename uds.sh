#!/bin/bash

for i in {0..2046..1}
do
    echo $(printf "%x" $i)
    cansend can0 $(printf "%03x#023e000000000000" $i)
    sleep .05
done

##22 read data by identifier
##2e 

#7e oder 7f bei fehler oderso

#02 3e 00 und den rest mit 0 