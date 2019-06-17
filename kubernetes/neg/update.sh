#!/bin/bash
echo "IP=$IP"

for i in $(seq 1 10000); do
  sed "s/VAR_TIME/$(date)/" rc.yaml > rc_update.ig.yaml  
  echo "$(date):  $i update"
  kubectl apply -f rc_update.ig.yaml
  
  echo "sleep 30mins"
  sleep 30m

  echo "#################Counting unique responses"
   for i in `seq 1 100`; do curl --connect-timeout 1 -s ${IP} && echo;  done  |sort | uniq -c
  



done

