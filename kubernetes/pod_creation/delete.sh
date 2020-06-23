#!/bin/bash

for i in $(seq 8000 1000000); do
  echo "$(date):  hostname-$i pod deleted"
  kubectl delete pod hostname-$i

  if [ $(expr $i % 10) = "0" ] 
  then
    if [ $(kubectl get pods | wc -l) -lt "10" ]  
    then
       echo "sleep 5s"
       sleep 5s
    fi
  fi
done

