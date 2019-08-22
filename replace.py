#!/usr/bin/python3
# -*- coding: utf-8 -*- 

import os 
import os,sys 
import hashlib
import shutil
import re
from collections import OrderedDict


def Replace(f1, f2):
    #f1 形如 FormatUtil.smali
    #f2 形如 FormatUtil.smalix

    fp = open(f1, 'r')
    fp2 = open(f2, 'w')
    line = fp.readline();

    inmethod = 0
    while line:
        if re.match('\\.method.*', line):
            inmethod = 1

        if inmethod == 1:
            if not (re.match('    \\.line.*', line) or re.match('    \\.locals.*', line) or re.match('    \\.registers.*', line) or line == "\n"):
                fp2.write(line)

        if re.match('\\.end method.*', line):
            inmethod = 0;
        line = fp.readline();

    fp.close()
    fp2.close()
    #print(f1)
    os.remove(f1)
def search(folder):
    #print(folder)

    for name in os.listdir(folder): 
        nxt = os.path.join(folder, name) 
        #print(nxt)

        if os.path.isdir(nxt): 
            search(nxt)
        else:
            if nxt.endswith("smali"):
                Replace(nxt, nxt + "x")
def main():
    
    if len(sys.argv) != 2:
        print("not folder")
    
    search(sys.argv[1])
if __name__=="__main__": main()