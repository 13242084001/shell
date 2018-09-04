#!/bin/bash
#
#公网上有两台服务器A：183.xxx.xx.70	B：183.xxx.xx.71，现在希望服务器B请求的https流量全部经过A转发，他们共同的网关是183.xxx.xx.94
#记录服务器B与网关的mac地址先
mac_70=`arp |grep '183.xxx.xx.70'|awk '{print $3}'`
mac_gw=`arp |grep '183.xxx.xx.94'|awk '{print $3}'`

#服务器B配置，开启内核转发，在output链匹配目的端口443的报文，打上mark标记10，新建一张路由表table 10，匹配mark标记10的报文优先查询table 10
if [ `cat /proc/sys/net/ipv4/ip_forward` -eq 0 ];then
	echo 1 > /proc/sys/net/ipv4/ip_forward
fi
	
iptables -t mangle -A OUTPUT -i p2p2 -p tcp --dport 443 -j MARK --set-mark 10
ip route add table 10 via 183.xxx.xx.70 dev p2p2
ip rule fwmark 10 table 10

#服务器A设置，收到服务器B的443报文后，报文的源ip地址仍是B的地址183.xxx.xx.70,然后根据目的地址查询路由表转发出去，下一跳是网关，报文回来的时候，我们也希望经过服务器A，然而现在报文的源地址是仍是B的地址，网关会直接把报文转发给B，所以在A转发之前就要把报文的源地址改成自己的地址
passwd=123456
/bin/expect <<-EOF
spawn ssh -p 22051 root@183.xxx.xx.70
set time 5
expect "*password*"
send "$passwd\n"
expext "*#"
send "echo 1 > /proc/sys/net/ipv4/ip_forward\n"
expect "*#"
send "iptables -t nat -A POSTROUTING -s 183.xxx.xx.71 -p tcp --dport 443 -j SNAT --to 183.xxx.xx.70\n"
interact
expect eof
EOF

#测试是否符合预期
baidu_ip=`ping www.baidu.com -c 1|grep 'from'|awk '{print $4}'|cut -d: -f1`
tcpdump -i p2p2 -nn -e host $baidu_ip port 443 -c 10 > test.txt &
curl https://$baidu_ip/
wait

if [[ `cat test.txt|grep '> $baidu_ip.443'|awk '{print $3}'|cut -d',' -f1` == $mac_70 && `cat test.txt|grep '$baidu_ip.443'`|awk '{print $2}' == $mac_70 ]];then
	echo 'host B port_proxy is succ'
fi
rm -rf text.txt

