FROM ubuntu
USER root
RUN apt-get update
RUN apt-get install -y python python-pip 
RUN pip install psutil

COPY ./kubelet_pod_usage.py ./
