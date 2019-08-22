#!/usr/bin/python3
# -*- coding: utf-8 -*- 

import os 
import os,sys 
import hashlib
import shutil
import re
def main():
    global Mode;
    global tot_method;
    global abone;
    global dic;
    if len(sys.argv) != 2:
        print("argc error")

    fp = open(sys.argv[1], 'r')
    fout = open('./result.txt', 'w')
    line = fp.readline()
    while line:

        if not (re.match('.     .*:goto_.*', line) or 
                re.match('.     .*:cond_.*', line) or
                re.match('.     \\#.*', line) or 
                re.match('.*:pswitch_.*', line)):
                fout.write(line)
        #print(line)
        line = fp.readline()
    fp.close()
    fout.close()
if __name__=="__main__": main()

 