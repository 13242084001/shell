#!/bin/bash
#
trap '' 2
port=`grep rtmp config.json |head -1|cut -d '"' -f4|cut -d : -f2`
port_num () {
	netstat -anp|grep -w $port|wc -l
}
if [ `port_num` -gt 0 ];then
	pid=`netstat -anp|grep -w $port|grep -i listen |awk '{print $7}'|cut -d '/' -f1`
	#echo "----------"
	#echo $pid
	#echo "----------"
	process=`ps -aux|grep $pid|awk '{print $11}'|head -1`
	#echo "---------"
	#echo $process
	#echo "---------"
	kill -9 $pid
	rm -rf nohup.out log/*
	sleep 3
	if [ `port_num` -eq 0 ];then
		nohup $process -d debug&
	fi
	sleep 3
	if [ `port_num` -gt 0 ];then
		echo "$process reboot succ"
	fi
else
	process_name=`ls -alt grtm*|tail -1 |awk '{print $9}'`
	#echo "-----"
	#echo $process_name
	#echo "-----"
	rm -rf nohup.out log/*
	nohup ./$process_name -d debug&
	sleep 3
	if [ `port_num` -gt 0 ];then
		echo "$process start succ"
        fi
fi
