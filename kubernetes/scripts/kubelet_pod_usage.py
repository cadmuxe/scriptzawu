#!/usr/bin/env python
# get pods cpu/memory usage from kubelet
# ref:
# https://github.com/kubernetes/kubernetes/blob/master/pkg/kubelet/apis/stats/v1alpha1/types.go
# CPU sample window: around 15 seconds
# https://github.com/kubernetes/kubernetes/blob/release-1.14/pkg/kubelet/cadvisor/cadvisor_linux.go#L50


import urllib2
import json
import time
import argparse
from datetime import datetime
import subprocess
import psutil
import os

parser = argparse.ArgumentParser()
parser.add_argument("pods", help="pod names seperate by comma")
parser.add_argument('--nodeproc', help="node proc path, this is need to get node resrouce usageinfo.")
parser.add_argument("--output", default="./", help="output path")


args = parser.parse_args()
pods = args.pods.split(",")
nodeproc = args.nodeproc
outputpath = args.output
default_window = 2

files = {}
all_file = open(os.path.join( outputpath,"all-usage.txt"), "w", buffering=1)
all_header = "Time"
mpstat_file = None

for p in pods:
  f = open( os.path.join( outputpath,"%s-usage.txt" % p), "w", buffering=1)
  files[p] = f
  header = " \t workingSetMBs-{pod} \t usageMBs-{pod} \t usageMillisecondCores-{pod} \t usageCoreMilliseconds-{pod}".format(pod=p)
  out = "Time" + header + " \n"
  all_header += header
  f.write(out)

if nodeproc:
  psutil.PROCFS_PATH = nodeproc
  mpstat_file = open(os.path.join( outputpath, "mpstat-usage.txt"), "w", buffering=1)
  header = " \t %cpu_total \t mem_used \t mem_buf \t mem_cache"
  out = "Time" + header + " \n"
  all_header += header
  mpstat_file.write(out)

all_file.write(all_header + " \n")

# blocking and get the cpu usage for [seconds] seconds.
def get_mpstat(seconds):
  cpu_total = psutil.cpu_percent(seconds)
  memory = psutil.virtual_memory()
  # cpu_total, mem_used, mem_buf, mem_cache
  return cpu_total, memory.used/1024/1024, memory.buffers/1024/1024, memory.cached/1024/1024 

while True:
  summary = urllib2.urlopen("http://localhost:10255/stats/summary").read()
  data = json.loads(summary)
  all = str(datetime.now())
  pod_dict = {}
  for pod in data["pods"]:
    pname = pod["podRef"]["name"]
    for targetName in pods:
      if pname.startswith(targetName):
        pod_dict[targetName] = pod

  for targetName in pods:
    pod = pod_dict[targetName]
    usage = " \t %fMbs \t %fMbs \t %sms \t %sms" % (float(pod["memory"]["workingSetBytes"])/1024/1024, 
                                                      float(pod["memory"]["usageBytes"])/1024/1024, 
                                                      float(pod["cpu"]["usageNanoCores"])/1000000, 
                                                      float(pod["cpu"]["usageCoreNanoSeconds"])/1000000)
    out = pod["memory"]["time"] + usage + " \n"
    all += usage
    files[targetName].write(out)

  if nodeproc:
    node_usage = get_mpstat(default_window)
    usage = " \t %s \t %s \t %s \t %s" %(node_usage)
    out = str(datetime.now()) + usage + " \n"
    all += usage
    mpstat_file.write(out)
  else:
    time.sleep(default_window)
  all_file.write(all + " \n")
