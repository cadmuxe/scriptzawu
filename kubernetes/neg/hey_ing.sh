#!/bin/bash

while true; do
  date >> hey_log.txt
  hey -n 3000 http://35.244.151.92 >>  hey_log.txt
done

