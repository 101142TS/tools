#!/usr/bin/python3
# -*- coding: utf-8 -*- 

import os 
import os,sys 
import hashlib
import shutil
import re
from collections import OrderedDict

method_cnt = 0
native_method_cnt = 0;
dict = {}
empty_list = []
def getData(f1, clazzname):

    #f1 形如 FormatUtil.smalix
    global dict;
    global method_cnt;
    global native_method_cnt;
    global empty_list;
    fp = open(f1, 'r')
    line = fp.readline();

    in_method = False;
    useful_code = 0
    now_method_name = ""
    abstract_label = False;
    native_label = False;
    while line:
        line = line.strip('\n')
        words = line.split(' ')

        for i in range(0, len(words)):
            if len(words[i]) > 0:
                st = i;
                break;

        if words[st].startswith('.method'):
            in_method = True
            now_method_name = words[len(words) - 1];
            useful_code = 0
            abstract_label = False;
            native_label = False;
            for i in range(0, len(words)):
                if words[i] == "abstract":
                    abstract_label = True
                if words[i] == "native":
                    native_label = True;
        
        if len(words) > 1 and words[st] == '.end' and words[st + 1] == 'method':
            if useful_code == 1 and abstract_label == False:
                empty_list.append(clazzname + "->" + now_method_name)
                if native_label == True:
                    native_method_cnt = native_method_cnt + 1;
                method_cnt = method_cnt + 1;
            in_method = False
        
        useful_code = useful_code + 1
        if words[st].startswith('invoke-'):

            mid = words[len(words) - 1].split('->')

            #print(mid)
            clazz = mid[0];
            method = mid[1]

            target = clazz + "->" + method
            now_cnt = dict.get(target, 0)
            dict[target] = now_cnt + 1;
        line = fp.readline();

    fp.close()


    r = os.popen("pcregrep -M -r \"     nop\\n     nop\\n     nop\\n\" '%s'" % f1);
    info = r.readlines() 
    if (len(info) > 1):
        print(f1)
    r.close();

def search(folder, clazzname):

    for name in os.listdir(folder): 
        nxt = os.path.join(folder, name) 
        #print(nxt)

        if os.path.isdir(nxt): 
            search(nxt, clazzname + name + "/")
        else:
            if nxt.endswith("smalix"):
                getData(nxt, clazzname + name[0 : len(name) - 7] + ";")
def main():
    
    if len(sys.argv) != 2:
        print("no folder")
    
    global dict;
    global method_cnt;
    global empty_list;
    global native_method_cnt;
    os.system("grep -r \"end method\" %s | wc -l" % sys.argv[1]);
    search(sys.argv[1], "L")
    print("native 方法数目: %d" % native_method_cnt)                    #没有函数体的native方法
    print("java   方法数目: %d" % (method_cnt - native_method_cnt))     #没有函数体的java方法（非abstract）

    #print(empty_list)

    DICT = {}
    for i in empty_list:
        if i in dict:
            DICT[i] = dict[i];

    sorted_dict = sorted(DICT.items(), key = lambda item:item[1], reverse=True)


    cnt = 0;
    for i in sorted_dict:
        cnt = cnt + 1
        print(i)
        if cnt > 100:
            break;
if __name__=="__main__": main()