#!/bin/bash

for i in $(seq 41 60); do
  sed "s/VAR_SEQ/$i/" pod.tmp.yaml > pod.ig.yaml
  echo "$(date):  hostname-$i pod created"
  kubectl apply -f pod.ig.yaml
  if [ $(expr $i % 10) = "0" ]
  then
    if [ $(kubectl get pods | wc -l) -gt "20" ]
    then
      echo "sleep 5s"
      sleep 5s
    fi
  fi
done

