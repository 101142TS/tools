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
    in_annotation = False
    while line:
        words = line.split(' ')
        #print(words)
        st = -1
        for i in range(0, len(words)):
            if len(words[i]) > 0:
                st = i
                break;
        if len(words) == 1 and words[0] == '\n':
            st = -1
        # print(st)

        if st != -1:
            if words[st] == '.annotation':
                in_annotation = True;
            
            skip_line = False
            method_def = False
            if words[st].startswith("#"):
                skip_line = True;

            if (words[st] != ".class" and
                words[st] != ".super" and
                words[st] != ".source" and 
                words[st] != ".implements" and
                words[st] != ".method"):
                if words[st][0] == '.' and (words[st] != ".end" 
                                        or words[st + 1].startswith("method") == False):
                    skip_line = True;
            #把 native标签都处理掉
            if words[st] == ".method":
                method_def = True
                
            if in_annotation == False and skip_line == False:
                for word in words:
                    if word.endswith('\n'):
                        word = word.strip('\n')

                    #if word != "native" or method_def == False:
                    fp2.write(' ')
                    if word.startswith(':cond_'):
                        fp2.write(':cond_')
                    elif word.startswith(':goto_'):
                        fp2.write(':goto_')
                    elif word.startswith(':pswitch_'):
                        fp2.write(':pswitch_')
                    elif word.startswith(':try_start_'):
                        fp2.write(':try_start_')
                    elif word.startswith('{:try_start_'):
                        fp2.write('{:try_start_')
                    elif word.startswith(':try_end_') and word.endswith('}'):
                        fp2.write(':try_end_}')
                    elif word.startswith(':try_end_'):
                        fp2.write(':try_end_')
                    elif word.startswith(':sswitch_data_'):
                        fp2.write(':sswitch_data_')
                    elif word.startswith(':sswitch_'):
                        fp2.write(':sswitch_')
                    elif word.startswith(':array_'):
                        fp2.write(':array_')
                    elif word.startswith(':catchall_'):
                        fp2.write(':catchall_')
                    elif word.startswith(':catch_'):
                        fp2.write(':catch_')
                    else:
                        fp2.write(word)
                fp2.write('\n')
            
            if len(words) > 1 and words[st] == '.end' and words[st + 1] == 'annotation\n':
                in_annotation = False;

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
        print("no folder")
    
    search(sys.argv[1])
if __name__=="__main__": main()