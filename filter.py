#!/usr/bin/python3
# -*- coding: utf-8 -*- 

import os 
import os,sys 
import hashlib
import shutil
Mode = 0
tot_method = 0
abone = 0
def Test2(rootDir, targetDir): 
    global Mode;
    global tot_method;
    global abone;
    os.makedirs(targetDir)

    most_bottom = 1
    for lists in os.listdir(rootDir): 
        NXTrootDir = os.path.join(rootDir, lists) 

         
        if os.path.isdir(NXTrootDir): 
            NXTtargetDir = os.path.join(targetDir, lists)
            Test2(NXTrootDir, NXTtargetDir)
            most_bottom = 0
        
    if most_bottom == 1:

        for lists in os.listdir(rootDir): 
            if Mode == 0:
                tot_method = tot_method + 1
            
            NXTrootDir = os.path.join(rootDir, lists) 
            #print(NXTrootDir)
            os.listdir(rootDir)
            NXTtargetDir = os.path.join(targetDir, lists)
            #print(NXTtargetDir)
            #print()

            #print(NXTrootDir)
            #print(NXTtargetDir)

            os.system(r'./trans '+ "\'" + NXTrootDir + "\' " + "\'" + NXTtargetDir + "\'")
        if len(os.listdir(rootDir)) > 1:
            print(rootDir)
            abone = abone + 1
def main():
    global Mode;
    global tot_method;
    global abone;

    if len(sys.argv) != 2:
        print("argc error")
    else:
        
        if sys.argv[1] == "1":
            name = "101142ts"
            Mode = 1
            abone = 0
        else:
            name = "jr"
            Mode = 0
            tot_method = 0

        print(name)

        if os.path.exists("./" + name + "/translated/"):
            shutil.rmtree("./" + name + "/translated/")
        Test2(os.getcwd() + "/" + name + "/code/", "./" + name + "/translated/")

        if Mode == 0:
            print("总共有 %d 个方法" % tot_method)
        else:
            print("有 %d 个方法包含了两个以上不同的bytecode文件" % abone)

if __name__=="__main__": main()

 