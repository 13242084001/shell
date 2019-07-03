#!/usr/bin/python3.6
#
from pyroute2 import IPRoute
import socket
import getopt
import sys
import os
import netifaces
import ipaddress
from IPy import IP


def usage():
    print('Usage: -h help \n'
            '       -i ip address\n'
            '       -r rate bitrate\n'
            )

def args(usage):
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:r:", ['help', 'ip=', 'rate='])
        options_dict = {}
        for k, v in opts:
            if k in ('-h', '--help'):
                usage()
                os._exit(0)
            elif k in ('-i', '--ip'):
                options_dict["dst_ip"] = v
            elif k in ('-r', "--rate"):
                options_dict["rate"] = v
        return options_dict
    except Exception as e:
        usage()
        os._exit(0)
    
def v4_hex(dst_ip):
    try:
        dst_ip_str = IP(dst_ip).strNormal(2) if len(dst_ip.split('/')) > 1 else dst_ip + '/255.255.255.255'
        #dst_net, mask = dst_ip_str.split('/')
        print(dst_ip_str)
        try:
            keys = ['/'.join([str(hex(int(ipaddress.IPv4Address(i)))) for i in dst_ip_str.split('/')]) + '+16']
            print('this is key %s' % keys)

        except Exception as e:
            print("ip is not available!")
            os._exit(0)
        return keys
    except Exception as e:
        print(str(e))
        os._exit(0)

def tc_exec(dst_ip=None, rate='1000kbit'):
    
    def __init__():

    ip = IPRoute()
    eth0 = ip.link_lookup(ifname='eth0')[0]
    dst_ip = ip.get_addr(label='eth0')[0].get('attrs')[0][1] if not dst_ip else dst_ip
    print(dst_ip, rate)
    keys = v4_hex(dst_ip)
    print(keys)
    print(eth0)

    ip.tc('add', 'htb', eth0, 0x10000, default=0x200000)
    ip.tc('add-class', 'htb', eth0, 0x10001, parent=0x10000, rate='100mbit', burst=1024 * 6, prio=3)
    ip.tc('add-class', 'htb', eth0, 0x10010, parent=0x10001, rate=rate+'kbit', burst=1024 * 6, prio=1)
    ip.tc('add-class', 'htb', eth0, 0x10020, parent=0x10001, rate='700mbit', burst=1024 * 6, prio=2)
    ip.tc('add', 'tbf', eth0, 0x100000, parent=0x10010, burst=1024 * 6, rate=rate+'kbit', latency='200ms')
    ip.tc('add', 'sfq', eth0, 0x200000, parent=0x10020, burst=1024 * 6, rate='70mbps', perturb=10)
    ip.tc('add-filter', 'u32', eth0, parent=0x10000, prio=1, protocol=socket.AF_INET, target=0x10010, keys=keys)


if __name__ == "__main__":
    options_dict = args(usage)
    print(options_dict)
    tc_exec(**options_dict)
