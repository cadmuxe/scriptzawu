#!/bin/bash
echo "IP=$IP"

while true; do 
    RES=$(curl -s $IP)
    if [[ ${RES} != *"hostname"* ]]; then
      echo "$(date) Fail: $RES" >>  error_record.ig.txt 
    fi
    echo $RES

done
