#!/usr/bin/python3
# -*- coding: utf-8 -*- 

import os 
import os,sys 
import hashlib
import shutil
from collections import OrderedDict
def main():
    global Mode;
    global tot_method;
    global abone;
    global dic;

    nowpath = os.getcwd() + "/dex/";
    for num in os.listdir(nowpath): 
        numdir = os.path.join(nowpath, num) 
        
        dexfile = numdir + "/whole.dex"
        os.system('java -jar /usr/local/bin/baksmali-2.1.1.jar -x %s -d ~/Desktop/framework -o ./dex/result' % dexfile)
        print(dexfile)

    os.system("./replace.py ./dex/result")
if __name__=="__main__": main()

 