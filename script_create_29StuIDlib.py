#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create a password-PSK lib for students with IDs in file 'stulist', for Wi-Fi network named 'QuestAP'
"""

import time
import pickle
from hashlib import pbkdf2_hmac as pbkdf2

start_time=time.time()
psklib=dict()
with open('stulist','r') as f:
    for line in f:
        print(line)
        strs=line.split()
        c_pass=strs[0]
        psk=pbkdf2('sha1',bytes(c_pass,'utf-8'),bytes('QuestAP','utf-8'),4096,256/8)
        psklib[c_pass]=psk
second_time=time.time()    
file=open('29StuID.p','wb')
pickle.dump(psklib,file,protocol=pickle.HIGHEST_PROTOCOL)
file.close()
third_time=time.time()
print("construct time: ",second_time-start_time,third_time-second_time,third_time-start_time)
# to load
# f=open(filename,'rb')
# t=pickle.load(f)    



