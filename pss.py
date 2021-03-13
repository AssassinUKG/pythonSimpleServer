#!/usr/bin/python3
import http.server
import socketserver
import threading
from functools import partial
import sys
import time


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
    if os.name is 'nt':
        os.system("cls")
    else:
        os.system("clear")
    print(SB+GN+"Python FileServer" +RS)
    print(WT+ "Created by "+SB+CY+ "Ac1D" + RS + "\n")

def GetHostInfo():
    if (os.name is 'nt'):
        #win
        cmd = ["cmd.exe", "/c","ipconfig"]
        HOSTNAME=subprocess.run(cmd, stdout=subprocess.PIPE)
        return HOSTNAME      
    else:
        #unix
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
    print("-" * 10 + SB+GN +" IP SELECTION " + RS + "-" * 10 + "\n")
    selection = 0
    for ip in CheckedIP:
        print(f"{selection +1}: {str(ip).strip()}")
        selection +=1
    print("-" * 33)
    
    while True:
        Choice = input(f"Select ip in range (1, {selection})\n" + SB+RD + "$ " + RS)
        Choice = int(Choice)
        try:
                
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
        except:
            print(RD+ "Invalid Choice, Try again!" + RS)

def runserv(port, dir):
    try:
            
        handler = partial(http.server.SimpleHTTPRequestHandler, directory=dir)
        socketserver.TCPServer.allow_reuse_address = True
        httpd = socketserver.TCPServer(("", port), handler)
        t = threading.Thread(target=httpd.serve_forever)
        t.daemon = True
        t.start()
        while True:
            time.sleep(1)
        
    except:
        httpd.shutdown()
        t.join()
        sys.exit

def IPChoice():
    Hostname= GetHostInfo()
    HostnameSplits= Hostname.stdout.decode().split(" ")
    checkedIP = []
    for ip in HostnameSplits:
        res = re.match("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip.strip())
        if res:
            if "255.255.255.0" in res.string : continue
            checkedIP.append(ip.strip())      
    

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
    print(SB+CY+ "\nCopy Links...\n" + RS)
    for file in files:        
        if not file.startswith(".") and not os.path.isdir(file):
            if method == "wget":
                print(GN + SB+ f"\t{method} http://{''.join(ip)}:{portSel}/{file}" + RS)
            else:
                print(GN + SB+ f"\t{method} http://{''.join(ip)}:{portSel}/{file} --output {file}" + RS)
    #HostFiles()
    print("\n")
    print(SB+GN+ "Starting Server" + RS)
     # os.system(f"sudo python3 -m http.server {portSel}")
    runserv(portSel, "/tmp")
    
    
  



if __name__ == '__main__':
    signal(SIGINT, handler)
    Banner()
    IPADDRESS = IPChoice()
    RunServer(IPADDRESS)







