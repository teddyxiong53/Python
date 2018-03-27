#!/usr/bin/python

#encoding: utf-8

import sys,os,re

tools="arm-linux-gnueabi-addr2line     arm-linux-gnueabi-elfedit       arm-linux-gnueabi-gcc-ranlib    arm-linux-gnueabi-ld            arm-linux-gnueabi-readelf \
arm-linux-gnueabi-ar            arm-linux-gnueabi-gcc           arm-linux-gnueabi-gcc-ranlib-5  arm-linux-gnueabi-ld.bfd        arm-linux-gnueabi-size \
arm-linux-gnueabi-as            arm-linux-gnueabi-gcc-5         arm-linux-gnueabi-gcov          arm-linux-gnueabi-ld.gold       arm-linux-gnueabi-strings \
arm-linux-gnueabi-c++filt       arm-linux-gnueabi-gcc-ar        arm-linux-gnueabi-gcov-5        arm-linux-gnueabi-nm            arm-linux-gnueabi-strip \
arm-linux-gnueabi-cpp           arm-linux-gnueabi-gcc-ar-5      arm-linux-gnueabi-gcov-tool     arm-linux-gnueabi-objcopy       \
arm-linux-gnueabi-cpp-5         arm-linux-gnueabi-gcc-nm        arm-linux-gnueabi-gcov-tool-5   arm-linux-gnueabi-objdump       \
arm-linux-gnueabi-dwp           arm-linux-gnueabi-gcc-nm-5      arm-linux-gnueabi-gprof         arm-linux-gnueabi-ranlib   "

tools_list = tools.split(" ")

def main():
    i =0
    for name in tools_list:
        if name != '':
            #print name
            tip = name[name.rfind('-')+1:]
            if tip.__len__() >= 2:
                print tip
                cmd = "ln -s " + name +  " arm-linux-" + tip
                print cmd
                os.system(cmd)

main()