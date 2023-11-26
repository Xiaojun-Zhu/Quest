# Quest Implementation

This project contains key source files for a paper submission. 

## Objective
The source files are for a particular task, student check-in, where student IDs are known in advance. They how we collect students IDs (as one particular questionnaire example) from a Wi-Fi network name 'QuestAP', by letting students connect to the Wi-Fi with their IDs as password.

## Hardware Requirements
Need the following equipments
- A laptop computer running these code.
- An external Wi-Fi antenna able to run in AP mode. (A built-in one is also fine, as long as it supports AP mode.)

## Software Requirments
Need the following software on the laptop.
- hostapd 2.6
- Python 3.6.9
- Scapy 2.4.4
Other versions have not been checked.

## Steps to use Quest
- Prepare a questionnaire, and create a dictionary containing all possible inputs. In this example, we assume student IDs are given in a file named `stulist`.
- Run `script_create_29StuIDlib.py` to create a password-PSK library named `29StuID.p`
- Configure the wireless card to run in AP mode.
- Run hostapd to create a Wi-Fi network with name `QuestAP`. A sample configuration file is provided as `hostapd.conf`
- Run `script_check_in.py` to start sniffing the handshake frames and cracking. This script also prints out the cracked results on the screen.

  

