FROM ubuntu:18.04

RUN apt-get update && apt-get install -y curl iptables libcap2-bin iproute2 net-tools

ADD ipv6mitm /usr/local/bin/ipv6mitm

ENTRYPOINT ["/bin/sleep", "99999h"]
