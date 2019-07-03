#!/bin/bash
#
cd /root/
arr=(1 5 10 20 25 28 30 40)
for i in ${arr[@]};do
	bash loss.sh start $i
	echo "start test loss rate $i"
	sleep 10m
	bash loss.sh stop
	echo "stop test loss rate $i"
	sleep 1m
done
