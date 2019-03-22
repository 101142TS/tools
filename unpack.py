#!/usr/bin/python3
# -*- coding: utf-8 -*- 

import os 
import os,sys 
import hashlib
import shutil
import time
import datetime

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

def getTID():
    global tidpath
    global phoneID

    os.system('rm ./tid.txt 2>/dev/null')
    os.system('adb -s %s pull %s ./tid.txt 2>/dev/null' % (phoneID, tidpath))
    fp = open('./tid.txt', 'r')
    tid = fp.readline();
    fp.close()
    return tid
def main():
    global tidpath
    global phoneID

    if len(sys.argv) != 2:
        print("未输入手机的ID")
        return; 

    phoneID = trans_ID(int(sys.argv[1]))

    #变成root模式
    os.system('adb -s %s root' % phoneID)
    time.sleep(2)
    
    #删除该删的东西
    os.system('rm -rf ./101142ts 2>/dev/null')

    #删除adblogcat, 新开启logcat并把信息储存到本地
    os.system('rm adblogcat.txt 2>/dev/null')
    os.system('adb -s %s logcat | grep "101142ts" > adblogcat.txt &' % phoneID)
    
    #读取unpack.txt
    os.system('rm ./unpack.txt 2>/dev/null')
    os.system('adb -s %s pull /data/local/tmp/unpack.txt ./unpack.txt' % phoneID)
    fp = open('./unpack.txt', 'r')
    packagename = fp.readline(); packagename = packagename.strip()
    fp.readline();
    WaitingTime = fp.readline(); WaitingTime = int(WaitingTime);
    fp.close()

    dir = "/data/data/" + packagename + "/101142ts"
    sche = dir + "/sche.txt"
    tidpath = dir + "/tid.txt"

    sum = 0
    os.system('adb -s %s shell am force-stop %s' % (phoneID, packagename))
    while 1:
        #输出次数
        sum = sum + 1
        print("第%d次dump " % sum)
        #输出时间
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        #判断是否已经结束dump
        okpath = dir + "/OK.txt"
        os.system('rm ./OK.txt 2>/dev/null')
        os.system('adb -s %s pull %s ./OK.txt 2>/dev/null' % (phoneID, okpath))
        if os.path.exists("./OK.txt"):
            break

        #看app中的sche.txt是否有足够的内容,如果有，更新文件夹下的last_sche，如果没有，使用last_sche.txt更新app中的sche.txt
        os.system('rm ./now_sche.txt 2>/dev/null')
        os.system('adb -s %s pull %s ./now_sche.txt 2>/dev/null' % (phoneID, sche))

        output = os.popen('./check')
        num = output.read();
        num = int(num)
        print(num)
        if num == 3:
            os.system('mv now_sche.txt last_sche.txt')
        else:
            os.system('adb -s %s push ./last_sche.txt %s' % (phoneID, sche))

        os.system('adb -s %s shell cat %s' % (phoneID, sche))
        print()
        #让应用运行并且等待
        os.system('adb -s %s shell monkey -p %s -c android.intent.category.LAUNCHER 1 > /dev/null' % (phoneID, packagename))
        print("应用已启动")

        #等待一段时间
        if sum == 1:
            #如果是第一次运行的话，则要运行makeup步骤
            while 1:
                makeuppath = dir + "/makeup"
                os.system('rm ./makeup 2>/dev/null')
                os.system('adb -s %s pull %s ./makeup 2>/dev/null' % (phoneID, makeuppath))
                if os.path.exists("./makeup"):
                    break
                time.sleep(5)
        else:
            time.sleep(WaitingTime)

        #这里的lastTID可能是空的
        lastTID = getTID();

        #判断
        #cnt = 0
        while 1:
            #等待10s
            time.sleep(10)
            nowTID = getTID();
            print(nowTID)
            if nowTID != lastTID:
                lastTID = nowTID
                continue;
            else:
                break;
            '''
            #查看线程tid是否存活
            os.system('rm ./tmp.txt 2>/dev/null')
            os.system('adb shell ps -t | awk \'{print $2}\' > ./tmp.txt')
            
            alive = 0;
            fp = open('./tmp.txt', 'r')
            x = fp.readline()  #读取第一行PID
            x = fp.readline()
            while x:
                if x == nowTID:
                    alive = 1;
                    break;
                x = fp.readline()
            fp.close()

            if alive == 0:
                break;
                time.sleep(0.2)
                cnt = cnt + 1
            
            #容忍4s，不行就退出
            if cnt == 20:
                break;
            '''
        print("准备停止")
        os.system('adb -s %s shell am force-stop %s' % (phoneID, packagename))
        

    print("dump已完成，准备取出101142ts文件夹")
    #将后台的记录日志关掉
    os.system('ps > tmp.txt')
    os.system('cat tmp.txt | grep "adb" | awk \'{print $1}\' > ./result.txt')

    fp = open('./result.txt', 'r')
    x = fp.readline()
    while x:
        os.system('kill -9 %s' % x)
        x = fp.readline()
    fp.close()

    #取出101142ts
    os.system('adb -s %s pull %s ./101142ts 2>/dev/null' % (phoneID, dir))

    
if __name__=="__main__": main()

 