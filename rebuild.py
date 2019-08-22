#!/usr/bin/python3
# -*- coding: utf-8 -*- 

import os 
import os,sys 
import hashlib
import shutil
import time

#输入ID，返回设备名
def trans_ID(ID):
    fp = open('/home/b/Desktop/tools/dev.txt', 'r')
    
    cnt = 0;
    name = fp.readline();   
    while name:
        name = name.strip()
        if cnt == ID:
            break;
        
        cnt = cnt + 1;
        name = fp.readline()    

    fp.close()
    return name

def main():
    if len(sys.argv) != 2:
        print("未输入手机的ID")
        return; 

    phoneID = trans_ID(int(sys.argv[1]))
    
    #变成root模式
    os.system('adb -s %s root' % phoneID)
    time.sleep(2)

    #删除rebuildlog, 新开启logcat并把信息储存到本地
    os.system('rm rebuildlog.txt')
    os.system('adb -s %s logcat | grep -a "101142ts" > rebuildlog.txt &' % phoneID)

    #读取unpack.txt
    os.system('adb -s %s pull /data/local/tmp/unpack.txt ./unpack.txt 2>/dev/null' % phoneID)
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
        os.system('rm -rf ./dex')
        dir = "/data/data/" + packagename  + "/101142ts"
        print("101142ts")

    tidpath = dir + "/tid.txt"

    sum = 0
    os.system('adb -s %s shell am force-stop %s' % (phoneID, packagename))
    while 1:
        #输出次数
        sum = sum + 1
        print("第%d次dump " % sum)

        #让应用运行并且等待
        os.system('adb -s %s shell monkey -p %s -c android.intent.category.LAUNCHER 1 > /dev/null' % (phoneID, packagename))
        time.sleep(WaitingTime)

        #读取tid
        os.system('adb -s %s pull %s ./tid.txt 2>/dev/null' % (phoneID, tidpath))
        fp = open('./tid.txt', 'r')
        tid = fp.readline();       tid = int(tid)
        print("线程号 %d " % tid)
        fp.close()
        
        #查看线程tid是否存活，并一直等待直到这个线程死亡
        while 1:
            os.system('adb -s %s shell ps -t | awk \'{print $2}\' > tmp.txt' % phoneID)

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
        os.system('adb -s %s shell am force-stop %s' % (phoneID, packagename))

        #看是否dump完
        okfile = dir + "/rebuild_OK.txt"
        os.system('rm ./rebuild_OK.txt')
        os.system('adb -s %s pull %s ./rebuild_OK.txt 2>null' % (phoneID, okfile))
        if os.path.exists("./rebuild_OK.txt"):
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
        #nowdir = dir + "/code"
        os.system('adb -s %s pull %s ./jr/ 2>null' % (phoneID, dir))
        print("已成功取出")
    elif Mode == 1:
        dir = dir + "/dex/"
        os.system('adb -s %s pull %s ./dex/ 2>null' % (phoneID, dir))
        print("已成功取出")

        
if __name__=="__main__": main()

 