#!/usr/bin/env python3.6
#
#引入linux内核inotify功能，用于监视文件系统增删改查，事件驱动
import pyinotify
import time
import os
import subprocess
from pynput.mouse import Button, Controller
from threading import Thread
import psutil
import logging


configFile = './config.txt'
path = "/tmp"
logger = logging.getLogger('processMonitor')
logHandle = logging.FileHandler('./test.log')
formats = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')
logHandle.setFormatter(formats)
logger.addHandler(logHandle)
logger.setLevel(logging.DEBUG)


class EventHandler(pyinotify.ProcessEvent):
    #新增文件事件后处理函数
    def process_IN_CREATE(self, event):
        if "hduapp.service" in event.name:
            logger.warning('hduapp prcess started...')

    #删除文件事件后的处理函数
    def process_IN_DELETE(self, event):
        if "hduapp.service" in event.name:
            logger.warning('hduapp prcess stoped...')
            logger.warning("停止测试...")
            os._exit(0)


class Mouse(object):

    __instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.mouse = Controller()

    def action(self, x=0, y=0, delay=0.5):
        self.mouse.position = (int(x), int(y))
        self.mouse.click(Button.left, count=1)
        time.sleep(float(delay))

def mouse_action():
    try:
        with open(configFile, 'r') as f:
            lines = f.read().splitlines()
    except FileNotFoundError as e:
        logger.error(e)
        os._exit(0)
        
    mouse = Mouse()
    while 1:
        for i in lines:
            args = i.split()
            mouse.action(*args)
        time.sleep(5)
     

#创建并运行监视器
def run_watcher():
    mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, EventHandler())
    wm.add_watch(path, mask, rec=True)
    notifier.loop()         

def sys_usage(pid):
    while 1:
        sys_info = {}
        process = psutil.Process(pid)
        sys_info['hdupp_rss'] = str(process.memory_info().rss / 1024) + "KB"
        sys_info['total_used'] = str(psutil.virtual_memory()[3] / 1024) + "KB"
        sys_info['cache'] = str(psutil.virtual_memory()[-1] / 1024) + "kB"
        logger.info("{!r}".format(sys_info))
        time.sleep(3)
    

if __name__ == "__main__":
    flag = 1
    #判断tmp下是否有hduapp.service的同名目录；systemd为服务在tmp下创建了同名目录，服务启动创建，服务停止或崩溃删除；以此来判断hdupp是否在运行或奔溃；奔溃立即停止测试
    for i in os.listdir('/tmp'):
        if "hduapp.service" in i:
            flag = 0
            hduapp_pid = subprocess.getstatusoutput("pidof HDUApp")[1]
            Thread(target=sys_usage, args=(int(hduapp_pid),)).start()
            Thread(target=mouse_action, args=()).start()
            logger.info('开始测试...')
            run_watcher()
    if flag:
        logger.warning("hduapp is not running...")
