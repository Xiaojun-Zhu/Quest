# Quest Implementation

This project contains key source files for the following paper.

> Xiaojun Zhu, Hao Han. “Quest: Instant Questionnaire Collection from Handshake Messages using WLAN.” Wireless Networks, to appear.

## Background: A Story
In Fall 2014, I taught Computational Thinking for first-year students in NUAA. When it comes to the topic of networking, I designed an in-class experiment, where I set up a WLAN, students connect, opens a browser, and submits their student IDs. That is, first use networking for collecting student IDs, and then explain the underlying concepts (wirless network, webpage, http, IP address, etc.). It sounds to be a wonderful idea for teaching, and I still think so.  I spent a couple of days setting up the WLAN environment,  writing a webpage and deploying it on IIS. I even tested it several times, and the system worked well.

It failed in class.  After telling the students what to do, we all starred at the sceen to see the progress of students check-ins. Soon some students complained that they cannot connect to the WLAN, and then more and more students complained. There were around 110+ students, and only a dozen submitted their IDs successfully. I sniffed the wireless traffic, and found many unneccessary frames. In that class, I changed my topic to  why WLAN can only support a limited number of clients. The class was very active. Students got excited probably because the teacher failed. I was also excited because nobody got asleep. The experiment failed, but the class was successful, I think. If you are one of the students at that time, please tell me.

Why do we need a stable connection for collecting only very little information?  How can we collect a small piece of information from a large amount of users, without relying on Internet access? 

The answer is this project and the published paper. 

Other than using the software for collecting data, I think it is also a good project for courses including topics such as Wireless Networks, Wireless Security, Password Cracking, etc. Please let me know if you find the software/idea helpful.

## Objective
The source files are for a particular task, student check-in (in Section 9.2 of the paper), where student IDs are known in advance. These files show how we collect students IDs (as one particular questionnaire example) from a Wi-Fi network name 'QuestAP', by letting students connect to the Wi-Fi with their IDs as password.

## Hardware Requirements
Need the following equipments
- A laptop computer running these code.
- An external Wi-Fi antenna able to run in AP mode. (A built-in one is also fine, as long as it supports AP mode.)

## Software Requirments
Need the following software on the laptop.
- hostapd 2.6
- Python 3.6.9
- Scapy 2.4.4
  
Other versions have not been tested.

## Steps to use Quest
- Prepare a questionnaire, and create a dictionary containing all possible inputs. In this example, we assume student IDs are given in a file named `stulist`.
- Run `script_create_29StuIDlib.py` to create a password-PSK library named `29StuID.p`
- Configure the wireless card to run in AP mode.
- Run hostapd to create a Wi-Fi network with name `QuestAP`. A sample configuration file is provided as `hostapd.conf`
- Run `script_check_in.py` to start sniffing the handshake frames and cracking. This script also prints out the cracked results on the screen.
- Let students connect to the Wi-Fi with their IDs as passwords. They will observe wrong password prompt, and at the same time the laptop will show their IDs on the screen.

  

