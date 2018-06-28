#!/bin/bash

FILE=/mnt/demo.dat
if [ ! -f "$FILE" ]; then
  touch $FILE
  echo 0 > $FILE
fi
ARGS=$@
ARGS+=" --host $HOST_IP --pod $POD_IP"
/app.py $ARGS 
