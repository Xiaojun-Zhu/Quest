from scapy.all import *
import time
import queue
import crack
import pickle

f=open('29StuID.p','rb')
psk_dict=pickle.load(f)

#tasks=queue.Queue() #each task is a 2-element tuple
submitted_anounces=list()
cached_EAPOL1=dict()#a dictionary caching received EAPOL packets indexed by anonce


packets=queue.Queue()

names=dict()
checkedTime=dict()
checkedMac=dict()
unchecked=list()

with open('stulist','r') as f:
    for line in f:
        strs=line.split()
        names[strs[0]]=strs[1]
        checkedTime[strs[0]]=-1
        checkedMac[strs[0]]=None
        unchecked.append(strs[0])

def print_status():
    
    print("checked students list:")
    count=0
    for i,name in names.items():
        if checkedTime[i]>=0:     
            count+=1
            print(f'{i} {name}')
    print(f"summary of checked:{count}\n")
    print("unchecked students:")
    count=0
    for i,name in names.items():
        if checkedTime[i]<0:
            count+=1
            print(f'{i} {name}')
    print(f'summary of unchecked: {count}')

def write_file():
    with open('results2.txt','w+') as f:
        for i,t in checkedTime.items():
            f.write(f'{i} {t} {checkedMac[i]}\n')

def cracking_thread():  
    STOP=False
    while not STOP:
        p=packets.get()
        if len(p)==113:# EAPOL 1
            anounce=p[31:31+32]
            anounce_str=''.join('%02x'%i for i in anounce)
            client_mac=p[:6]#EAPOL 1's destination is clientreuse packet  space
            client_mac_str=''.join('%02x'%i for i in client_mac)
            if client_mac_str+anounce_str not in submitted_anounces:
                cached_EAPOL1[client_mac_str]=p
        elif len(p)==135:#EAPOL 2
            client_mac=p[6:12]
            client_mac_str=''.join('%02x'%i for i in client_mac)
            p1=cached_EAPOL1.pop(client_mac_str,None)
            if p1 is not None:# we have a EAPOL 1 packet
            #check whether the two has matching replay counter           
                if p1[30]==p[30]:                    
#                    tasks.put((p1,p))#yes, we can now submit a task
                    #mark the handshake as complete
                    anounce=p1[31:31+32]
                    anounce_str=''.join('%02x'%i for i in anounce)
                    submitted_anounces.append(client_mac_str+anounce_str)  
 #                   (key1,key2)=tasks.get() #automatically blocks
  #                  start_time=time.time()
                    psw=crack.crack_pass2(psk_dict,p1,p)
                    if psw is None:
                        print(f'invalid stu ID from mac: {client_mac_str}\n')
                        continue
                    checkedTime[psw]=time.time()   
                    checkedMac[psw]=client_mac_str
                    if psw in unchecked:
                        unchecked.remove(psw)
                    print('student check in: ',psw,names[psw],'; remaining ',len(unchecked))
                    
                    if len(unchecked)==0:
                        #all have been checked
                        write_file()
                        STOP=True
                    

def ap_pkts(pkt):
    #first check 
    p=raw(pkt)
    if len(p)==113 or len(p)==135:
        packets.put(p)
        
      
     
worker=threading.Thread(target=cracking_thread,daemon=False)
worker.start()

t=AsyncSniffer(iface="wlxe84e0628afa3",prn=ap_pkts,store=True)
t.start()
t.join()
#%%

results=t.results
wrpcap('results.pcap',results)