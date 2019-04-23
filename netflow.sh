#!/bin/bash

nic=(`cat /proc/net/dev|grep :|awk '{print $1}'`)
for i in ${nic[@]};do
	echo $i
done

while true;do
	sleep 1
	arr=()
	cat /proc/net/dev|grep :|while read line;do
		arr+=(`echo $line|awk '{print $2" "$10}'`)
	done
	echo ${arr[@]}
	for nic in ${nic[@]};do
		
		echo "$nic\t${arr[1]}"
	done
done
