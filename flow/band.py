#!/usr/bin/env python3.6
#
import subprocess
import time
from collections import deque
from functools import reduce
import gol

last = [0,0]
#gol._init()

def bandwidth():
    """
    获取到特定ip的流量，bytes，返回一个数组，进入的bytes数，发出的bytes数；[234.11,2233.33]
    """
    cmd = "iptables -nvxL|grep 192.168.50.67|awk '{print $2}'"
    out = subprocess.getstatusoutput(cmd)
    if not out[0]:
        st = map(lambda x: int(x) * 8 / 1000, out[1].split())
        #print(st)
        return list(st)

def calc(after, last):
    """

    """
    time.sleep(1)
    new_last = after()
    result = list(map(lambda x, y: x-y, new_last, last))
    #print(result)
    return result, new_last

def data_queue(calc, a, b):
    dq = deque(maxlen=10)
    while True:
        #print('this is %s' % b)
        result, b = calc(a, b)
        dq.append(result)
        yield dq

def add(x, y):
    return list(map(lambda a, b: a+b, x,y))

def get_network_status():
    out = subprocess.getstatusoutput("ping 192.168.50.67 -f -c 100")
    #print(out)
    if not out[0]:
        re = out[1].split(',')[2:]
        gol.set_value("packet loss", re[0].split()[0])
        gol.set_value(re[1].split(' = ')[0].split('\n')[1], re[1].split(' = ')[1])
        #print(gol._global_dict)


def main():
    for dq in data_queue(calc, bandwidth, last):
        tmp_list = list(dq)
        #print(tmp_list)
        avg10 = list(map(lambda x: round(x / 10, 2), reduce(add, tmp_list)))
        avg2 = list(map(lambda x: round(x / 2, 2), reduce(add, tmp_list[-2:])))
        avg5 = list(map(lambda x: round(x / 5, 2), reduce(add, tmp_list[-5:])))
        get_network_status()
        gol.set_value('avg10', avg10)
        gol.set_value('avg2', avg2)
        gol.set_value('avg5', avg5)
        print(gol._global_dict)


if __name__ == "__main__":
    main()       

