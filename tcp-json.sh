#!/bin/sh
#

pipe=/tmp/testpipe

kill_tcpdump() {
	pid=`ps -ef|grep tcpdump|head -n 1|awk '{print $2}'`
	echo $pid
	sudo kill -9 $pid
	rm -rf $pipe
	exit
}


#如果存在名字叫做pipe的命名管道
if [ ! -p $pipe ];then
	mkfifo $pipe;
	sudo tcpdump &>/dev/null -i lo0 'ip[2:2] > 52' and port 8889 -Annvv -l > $pipe &
fi

while True;do
	trap 'kill_tcpdump' SIGINT
	if read line < $pipe;then
		if [[ `echo $line|grep Flags` =~ 'Flags' ]];then
			echo ">>>>>"$line|awk -F'Flags' '{print $1}'
			echo 
		elif [[ `echo $line|cut -b 9` == '{' ]];then
			echo $line|cut -b 9-|jq .
			#echo ++++++++++++++++++++++++++++++++++++++
		fi
	fi
done
	
