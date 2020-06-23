#!/bin/bash

for i in $(seq 1 1000000); do
  sed "s/VAR_SEQ/$i/" svc.tmp.yaml > svc.ig.yaml
  echo "$(date):  hostname-$i svc created"
  kubectl apply -f svc.ig.yaml
  sleep 2s;

done

