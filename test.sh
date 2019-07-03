#!/bin/bash
#
case $1 in
start)
	tc qdisc add dev eth0 root handle 1: htb default 20
	tc class add dev eth0 parent 1: classid 1:1 htb rate 100mbps ceil 120mbps prio 3
	tc class add dev eth0 parent 1:1 classid 1:10 htb rate $2kbps ceil $2kbps prio 2
	tc class add dev eth0 parent 1:1 classid 1:20 htb rate 70mbps ceil 70mbps prio 1
	tc qdisc add dev eth0 parent 1:10 handle 10: tbf rate $2kbps burst 15k latency 200ms
	tc qdisc add dev eth0 parent 1:20 handle 20: sfq perturb 10
	tc filter add dev eth0 parent 1: protocol ip prio 2 u32 match ip dst 172.30.50.82 flowid 1:10
	;;
stop)
	tc qdisc delete dev eth0 root
	;;
*)
	exit 0
	;;
esac

