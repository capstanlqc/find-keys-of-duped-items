#!/bin/env bash

for f in $(find source/0?_QQ?_N -name "*.xml")
do
    id=$(echo $(basename $f) | cut -d"_" -f4 | cut -d"-" -f1)
    echo $id
    echo $f
    grep -Poh --color '(?<=<label key=")[^"]+(?=")' $f > $id.txt
done

for f in $(find source/07_COS_XYZ_N -name "PISA_2025FT_QQ_*.xml")
do
    id=$(echo $(basename $f) | cut -d"_" -f4 | cut -d"-" -f1)
    echo $id
    echo $f
    grep -Poh --color '(?<=<label key=")[^"]+(?=")' $f > $id.txt
done