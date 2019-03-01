#!/bin/bash
#公司有个httpdns代理服务器，接受http请求，要求性能测试，利用shell脚本实现请求高并发将响应重定向到log文件中，统计响应的时间并排序
trap "" 2
thread=16
tempfifo="my_temp_fifo"
mkfifo $tempfifo
exec 1000<>$tempfifo
rm -rf $tempfifo

for i in `seq 1 $thread`;do
	{	
		echo 
	}
done >&1000
start_time=$[$(date +%s%N)/1000000]
for x in `seq 1 500000`;do
	{
		read -u1000
		{
			#curl -s "http://httpdns.yfcloud.com/zhanqi?host=yfhdl.cdn.zhanqi.tv&app=live&stream=live_9918434_9559396&clientIp=27.17.1.5" >> req.log
			curl -s -o /dev/null -w "%{http_code}:%{time_total}\n" "http://127.0.0.1:8090/admin?username=lelsie&passwd=123" >> req.log
			echo >&1000
			#echo $x
		} &
	}
done

wait
end_time=$[$(date +%s%N)/1000000]
let time=end_time-start_time
echo $time
exec 1000>&-

echo ---------------------------
cat req.log |awk -F: '{print $1}'|sort |uniq -c
echo ---------------------------
cat req.log |awk -F: '{print $2}'|sort |uniq -c
