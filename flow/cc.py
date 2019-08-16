#!/usr/bin/python3.6
#
import gol
import band
import threading

gol._init()

t = threading.Thread(target=band.main, args=())
t.start()
