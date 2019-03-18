#!/usr/bin/python3
# -*- coding: utf-8 -*- 

import os 
import os,sys 
import hashlib
import shutil
import time
def main():
    #变成root模式
    os.system('adb root')
    time.sleep(2)

    #删除rebuildlog, 新开启logcat并把信息储存到本地
    os.system('rm rebuildlog.txt')
    os.system('adb logcat | grep "101142ts" > rebuildlog.txt &')

    #读取unpack.txt
    os.system('adb pull /data/local/tmp/unpack.txt ./unpack.txt')
    fp = open('./unpack.txt', 'r')
    packagename = fp.readline(); packagename = packagename.strip()
    fp.readline();
    WaitingTime = fp.readline(); WaitingTime = int(WaitingTime);
    Mode = fp.readline();        Mode = int(Mode)
    fp.close()

    if Mode == 0:
        os.system('rm -rf ./jr')
        os.system('mkdir ./jr')
        dir = "/data/data/" + packagename  + "/jr"
        print("jr")
    else:
        dir = "/data/data/" + packagename  + "/101142ts"
        print("101142ts")

    tidpath = dir + "/tid.txt"

    sum = 0
    os.system('adb shell am force-stop %s' % packagename)
    while 1:
        #输出次数
        sum = sum + 1
        print("第%d次dump " % sum)

        #让应用运行并且等待
        os.system('adb shell monkey -p %s -c android.intent.category.LAUNCHER 1 > /dev/null' % packagename)
        time.sleep(WaitingTime)

        #读取tid
        os.system('adb pull %s ./tid.txt' % tidpath)
        fp = open('./tid.txt', 'r')
        tid = fp.readline();       tid = int(tid)
        print("线程号 %d " % tid)
        fp.close()
        
        #查看线程tid是否存活，并一直等待直到这个线程死亡
        while 1:
            os.system('adb shell ps -t | awk \'{print $2}\' > tmp.txt')

            alive = 0;
            fp = open('./tmp.txt', 'r')
            x = fp.readline()  #读取第一行PID
            x = fp.readline()
            while x:
                x = int(x)
                if x == tid:
                    alive = 1;
                    break;
                x = fp.readline()
            fp.close()

            if alive == 0:
                break;
            time.sleep(1)
        
        #强制杀死应用
        os.system('adb shell am force-stop %s' % packagename)

        #看是否dump完
        alldone = 1
        if Mode == 0:
            dexDIR = "./jr/dex/"
        else:
            dexDIR = "./101142ts/dex/"

        os.system('rm -rf %s' % dexDIR)
        os.system('mkdir %s' % dexDIR)
        PhonedexDIR = dir + "/dex"
        os.system('adb pull %s %s 2>null' % (PhonedexDIR, dexDIR))
        for num in os.listdir(dexDIR): 
            nowDir = os.path.join(dexDIR, num) 

            if not os.path.exists(nowDir + "/isdone"):
                alldone = 0
                break
        if alldone == 1:
            break
        print()
    print("dump已完成，准备取出code文件夹")
    #将后台的记录日志关掉
    os.system('ps > tmp.txt')
    os.system('cat tmp.txt | grep "adb" | awk \'{print $1}\' > ./result.txt')

    fp = open('./result.txt', 'r')
    x = fp.readline()
    while x:
        os.system('kill -9 %s' % x)
        x = fp.readline()
    fp.close()

    
    if Mode == 0:
        nowdir = dir + "/code"
        os.system('adb pull %s ./jr/code 2>null' % nowdir)

        
if __name__=="__main__": main()

 