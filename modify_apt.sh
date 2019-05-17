#!/bin/bash
#
# date :
# description :

version_str=`lsb_release -a 2>/dev/null|grep Codename|awk '{print $2}'`
deb_1="deb http://mirrors.163.com/ubuntu/ $version_str main restricted universe multiverse"
deb_2="deb http://mirrors.163.com/ubuntu/ $version_str-security main restricted universe multiverse"
deb_3="deb http://mirrors.163.com/ubuntu/ $version_str-updates main restricted universe multiverse"
deb_4="deb http://mirrors.163.com/ubuntu/ $version_str-proposed main restricted universe multiverse"
deb_5="deb http://mirrors.163.com/ubuntu/ $version_str-backports main restricted universe multiverse"
deb_src1="deb-src http://mirrors.163.com/ubuntu/ $version_str main restricted universe multiverse"
deb_src2="deb-src http://mirrors.163.com/ubuntu/ $version_str-security main restricted universe multiverse"
deb_src3="deb-src http://mirrors.163.com/ubuntu/ $version_str-updates main restricted universe multiverse"
deb_src4="deb-src http://mirrors.163.com/ubuntu/ $version_str-proposed main restricted universe multiverse"
deb_src5="deb-src http://mirrors.163.com/ubuntu/ $version_str-backports main restricted universe multiverse"
DEB_SOURCE="${deb_1}\n${deb_2}\n${deb_3}\n${deb_4}\n${deb_5}\n${deb_src1}\n${deb_src2}\n${deb_src3}\n${deb_src4}\n${deb_src5}\n"

APT_FILE="/etc/apt/sources.list"
version_str=`lsb_release -a 2>/dev/null|grep Codename|awk '{print $2}'`

[ -f ${APT_FILE} ] && mv ${APT_FILE}{,.bak}
printf "${DEB_SOURCE}" >> ${APT_FILE} && apt-get update -qq && apt --fix-broken install -qq && echo "update apt succuss !"
install_list=(python-pip)
for tool in ${install_list[@]};do
	[ `apt-get install -qq -y $tool` ] && echo "install $tool succuss !"
done
wait

echo "All tool was be installed !"

