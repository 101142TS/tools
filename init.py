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
def main():
    global tidpath
    global phoneID

    if len(sys.argv) != 3:
        print("未输入手机的ID,包名")
        return; 

    phoneID = trans_ID(int(sys.argv[1]))
    packagename = sys.argv[2]

    os.system('adb -s %s shell mkdir /data/data/%s/101142ts/' % (phoneID, packagename))
    #将last_sche.txt放进去
    os.system('adb -s %s push ./last_sche.txt /data/data/%s/101142ts/sche.txt' % (phoneID, packagename))

    #将dvmName.txt放进去
    os.system('adb -s %s push ./dvmName.txt /data/data/%s/101142ts/dvmName.txt' % (phoneID, packagename))
    
if __name__=="__main__": main()

 