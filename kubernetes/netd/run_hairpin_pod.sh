#!/bin/bash

SERVICE_IP=$(kubectl get services netd-test-hairpin -o jsonpath={.spec.clusterIP})
sed "s/SERVER_IP/${SERVICE_IP}/" hairpin-pod.temp.yaml > hairpin-pod.ig.yaml
