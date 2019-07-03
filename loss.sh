#!/bin/bash
#

flush_iprule(){
	iptables -t nat -F
	iptables -t mangle -F
}
if [ 0 -le 2 ];then
	case $1 in 
	start)
#iptables -t nat -A POSTROUTING -s 192.168.99.176/32 -o eth0 -j MASQUERADE
		iptables -t mangle -A POSTROUTING -d 172.30.50.82/32 -j MARK --set-mark 11
		iptables -t mangle -A POSTROUTING -d 172.30.50.112/32 -j MARK --set-mark 11
#iptables -t nat -A PREROUTING -s 192.168.50.92/32 -p udp -j DNAT --to 192.168.99.176
		if [ $2 -le 100 ];then
			tc qdisc add dev eth0 root handle 1: htb default 30
			tc class add dev eth0 parent 1: classid 1:1 htb rate 1000mbit
			tc class add dev eth0 parent 1:1 classid 1:11 htb rate 100mbit
			tc class add dev eth0 parent 1:1 classid 1:30 htb rate 900mbit
			tc qdisc add dev eth0 parent 1:11 netem loss $2%
			tc filter add dev eth0 protocol ip handle 0xb fw classid 1:11
		else
			echo 123
			flush_iprule
			exit 0
		fi
		;;
	stop)
		flush_iprule
		tc qdisc delete dev eth0 root
		;;
	show)
		tc qdisc show dev eth0
		;;
	*)
		iptables-save
		exit 0
		;;
	esac
else
	exit 0
fi
