#!/usr/bin/env python3.6
#
from scapy.all import *
import json
from prettyprinter import cpprint

def eth2json(eth):
    if eth:
        print(eth)
        eth = eth.encode().decode('unicode_escape').encode('raw_unicode_escape').decode()
        #a = b"\xe8\xaf\xad\xe6\x96\x87"
        #print(str(a, "utf-8"))
        try:
            eth = json.loads(eth, encoding="utf-8")
            return cpprint(eth)
        except Exception as e:
            print(e)
    return ''

#a = sniff(filter="icmp", count=3, timeout=5, prn=lambda x:x.summary())
#a=sniff(filter="tcp port 3600",prn=lambda x: x.sprintf("%IP.src%:%TCP.sport% -> %IP.dst%:%TCP.dport%  %2s,TCP.flags% : %TCP.payload%"))
#a=sniff(filter="tcp port 3600",prn=lambda x: x.sprintf("%IP.src%:%TCP.sport% -> %IP.dst%:%TCP.dport%  %2s,TCP.flags% : %TCP.payload%"))
#a=sniff(filter="tcp port 3600", prn=lambda x: eth2json(x.sprintf("%TCP.payload%")[x.sprintf("%TCP.payload%").find("{"):-1]))
a=sniff(filter="tcp port 3600", prn=lambda x: eth2json(x.sprintf("%TCP.payload%")[x.sprintf("%TCP.payload%").find("{"):-1]))
