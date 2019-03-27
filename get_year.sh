#!/bin/bash -e

YEAR=$1
TO=$2
let TO=TO+1

COUNTER=1
while [ $COUNTER -lt $TO ]; do
  python main.py -y $YEAR -n $COUNTER -o "${YEAR}_${COUNTER}.json"
  let COUNTER=COUNTER+1 
done