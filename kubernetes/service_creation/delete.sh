#!/bin/bash

for i in $(seq 197 1000000); do
  echo "$(date):  hostname-$i svc deleted"
  kubectl delete svc hostname-$i

  if [ $(expr $i % 10) = "0" ] 
  then
    if [ $(kubectl get svc | wc -l) -lt "11" ]  
    then
       echo "sleep 5s"
       sleep 5s
    fi
  fi
done

