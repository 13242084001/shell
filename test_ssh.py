#coding:utf-8
from settings import *
import os
import time
try:
    import paramiko
except ImportError as e:
    print("没有安装paramiko,正在安装paramiko...,请稍等")
    os.popen("pip3 install paramiko")
    import paramiko
try:
    import threading
except ImportError as e:
    print("没有安装threading，正在安装threading...,请稍等")
    os.popen("pip3 install threading")
    import threading


def tunction(ip,username,password,command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip,username= username,password=password)
    stdin,stdout,stdeer = client.exec_command(command)
    #print(stdout.read())
    if not stdeer.read():
        print("#"*30)
        print("\033[1;36;40m设备%s执行成功, %s\033[0m" % (ip, ",".join(stdout)))
        #print("#"*30)
    else:
        print("\033[1;31;40m设备%s执行失败, %s\033[0m" % (ip, ",".join(stdeer)))
    client.close()
def main(host_list,command):
    thread_list = []
    for ip,username,password in host_list:
        t = threading.Thread(target = tunction,args = (ip,username,password,command))
        thread_list.append(t)
    for th in thread_list:
        th.start()
    for th in thread_list:
        th.join()

if __name__ == "__main__":
    start_time = time.time()
    m = threading.Thread(target = main,args = (host_list,command)) 
    m.setDaemon(True)
    m.start()
    m.join()
    end_time = time.time()
    chg_time = str(start_time - end_time) + "s"
print(chg_time)
