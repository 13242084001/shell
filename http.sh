#!/bin/bash
#监控服务器上http请求头部大小分布，记录头部字段都有哪些
lt_500=0
http500_to_800=0
http800_to_1500=0
gt_1500=0

for i in `seq 1 100`;do
	#这里用tcpdump抓包，我们知道tcp头部可选部分通常为空，那么头部大小固定为20字节，tcp[20:2]表示从tcp报文第20个字节开始的后两个字节，0x4745代表GET，0x504f代表POST,0x4854代表HTTP
	tcpdump -i p2p2 -A "tcp[20:2]=0x4745" -c 1 |sed 's/.*GET/GET/'|sed 'N;/\nGET/!P;D' > test1.txt
	cat test1.txt >>  test2.txt
	len_num=`cat test1.txt|sed 's/^/flag/g'|grep -A100 'GET'|grep -B100 'flag'|grep -v 'flag'|wc -c`
	echo $len_num
	if [ $len_num -lt 500 ];then
		let lt_500++
	elif [ $len_num -lt 800 ];then
		let http500_to_800++
	elif [ $len_num -lt 1500 ];then
		let http800_to_1500++
	else
		let gt_1500++
	fi
done > count_result.txt

echo $lt_500
echo ${http500_to_800}
echo ${http800_to_1500}
echo ${gt_1500}
