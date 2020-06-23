#!/bin/bash

for i in $(seq 1 1000000); do
  kubectl delete pod -n kube-system -l k8s-app=calico-node
  sleep 10s;

done

