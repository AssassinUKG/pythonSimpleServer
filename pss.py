#!/usr/bin/python3
import re
import subprocess
import os
from colorama import Fore, Back, Style
from signal import signal, SIGINT
from sys import exit

SB = Style.BRIGHT
RS = Style.RESET_ALL

GN = Fore.GREEN
RD = Fore.RED
CY = Fore.CYAN
BL = Fore.BLUE
YW = Fore.YELLOW
WT = Fore.WHITE


def handler(signal_received, frame):
    #Usage: signal(SIGINT, handler)
    print(RD+ '\nCtrl + C detected, Closing application gracefully.' + RS)
    exit(0)
   

def Banner():
    os.system("clear")
    print(SB+GN+"Python FileServer" +RS)
    print(WT+ "Created by "+SB+CY+ "Ac1D" + RS + "\n")

def GetHostInfo():
    cmd = ["/bin/bash", "-c","hostname -I"]
    HOSTNAME=subprocess.run(cmd, stdout=subprocess.PIPE)
    return HOSTNAME


def HostFiles():
    #1. List files, Add to list files
    #2. Start python server for files
    #os.system("cd $pwd")
    print(BL+SB+ "\nCurrent Directory...\n" + RS)
    os.system("ls -lh --color")



def ShowMenu(CheckedIP):
    print("-" * 10 + SB+GN +" IP SELECTION " + RS + "-" * 10)
    selection = 0
    for ip in CheckedIP:
        print(f"{selection +1}: {ip}")
        selection +=1
    print("-" * 33)
    
    while True:
        Choice = input(f"Select ip in range (1, {selection})\n" + SB+RD + "$ " + RS)
        Choice = int(Choice)
        if Choice == 1:
            return CheckedIP[Choice -1]
        elif Choice == 2:
            return CheckedIP[Choice -1]
        elif Choice == 3:
            return CheckedIP[Choice -1]
        elif Choice == 4:
            return CheckedIP[Choice -1]
        elif Choice == 5:
            return CheckedIP[Choice -1]
        else:
            print(RD+ "Invalid Choice, Try again!" + RS)
    
  
def IPChoice():
    Hostname= GetHostInfo()
    HostnameSplits= Hostname.stdout.decode().split(" ")
    checkedIP = []
    for ip in HostnameSplits:
        res = re.match("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip)
        if res:
            checkedIP.append(ip)      
    

    if len(checkedIP) <= 1:
        return checkedIP
    else:
        return ShowMenu(checkedIP)

def RunServer(ip):
    Banner()
    files = os.listdir('.')
    portSel = input("Enter port for Python server (Press Enter for default: 8080): ")
    method = ""
    while True:
        
        wgetOrCurl = input("Method: Wget / Curl (press Enter Default (wget) or 'c' for curl: ")
        if wgetOrCurl == "c":
            method = "curl"
            break
        elif wgetOrCurl == "w":
            method = "wget"
            break 
        else:
            method = "wget"
            break
            

    if not portSel: portSel = 8080
    print(BL+SB+ "\nCopy Links...\n" + RS)
    for file in files:        
        if not file.startswith(".") and not os.path.isdir(file):
            if method == "wget":
                print(GN + SB+ f"\t{method} http://{''.join(ip)}:{portSel}/{file}" + RS)
            else:
                print(GN + SB+ f"\t{method} http://{''.join(ip)}:{portSel}/{file} --output {file}" + RS)
    HostFiles()
    print("\n")
    print(SB+GN+ "Starting Server" + RS)
    
    
    
    os.system(f"sudo python3 -m http.server {portSel}")


if __name__ == '__main__':
    signal(SIGINT, handler)
    Banner()
    IPADDRESS = IPChoice()
    RunServer(IPADDRESS)
