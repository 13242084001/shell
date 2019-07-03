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
    
class tc_handle(object):
    
    def __init__(self, dst_ip=None, rate='1000kbit'):
        self.ip = IPRoute()
        self.rate = rate
        self.eth0 = self.ip.link_lookup(ifname='eth0')[0]
        self.dst_ip = self.ip.get_addr(label='eth0')[0].get('attrs')[0][1] if not dst_ip else dst_ip
        print(self.dst_ip, self.rate)
        self.keys = self.v4_hex(self.dst_ip)
        print(self.keys)
        print(self.eth0)

    def v4_hex(self, dst_ip):
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
    
    def __call__(self):
        self.ip.tc('add', 'htb', self.eth0, 0x10000, default=0x200000)
        self.ip.tc('add-class', 'htb', self.eth0, 0x10001, parent=0x10000, rate='100mbit', burst=1024 * 6, prio=3)
        self.ip.tc('add-class', 'htb', self.eth0, 0x10010, parent=0x10001, rate=self.rate+'kbit', burst=1024 * 6, prio=1)
        self.ip.tc('add-class', 'htb', self.eth0, 0x10020, parent=0x10001, rate='700mbit', burst=1024 * 6, prio=2)
        self.ip.tc('add', 'tbf', self.eth0, 0x100000, parent=0x10010, burst=1024 * 6, rate=self.rate+'kbit', latency='200ms')
        self.ip.tc('add', 'sfq', self.eth0, 0x200000, parent=0x10020, burst=1024 * 6, rate='70mbps', perturb=10)
        self.ip.tc('add-filter', 'u32', self.eth0, parent=0x10000, prio=1, protocol=socket.AF_INET, target=0x10010, keys=self.keys)


if __name__ == "__main__":
    options_dict = args(usage)
    print(options_dict)
    tc_handle(**options_dict)()
