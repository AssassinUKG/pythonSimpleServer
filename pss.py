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
from types import BuiltinFunctionType
from colorama import Fore, Back, Style
from signal import signal, SIGINT
from sys import exit
import argparse


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

    ban="""
  _______ __                _______                  
 |   _   |__.--------.-----|   _   .-----.----.--.--.
 |   $___|  |        |  _  |   $___|  -__|   _|  |  |
 |____   |__|__|__|__|   __|____   |_____|__|  \___/ 
 |:  $   |           |__|  |:  $   |                 
 |::.. . |                 |::.. . |                 
 `-------'                 `-------'                 
                                                     """

    print(SB+GN+ ban +RS)
    print(SB+WT+ "Created by "+SB+CY+ "Ac1D" + RS + "\n")

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


def ShowMenu(CheckedIP):
    print("-" * 10 + SB+GN +" IP SELECTION " + RS + "-" * 10)
    selection = 0
    for ip in CheckedIP:
        print(f"{selection +1}: {str(ip).strip()}")
        selection +=1
    print("-" * 33)
    
    while True:        
        try:
            Choice = input(f"Select ip in range (1, {selection})\n" + SB+GN + "$ " + RS)
            Choice = int(Choice)
            return CheckedIP[Choice -1]
        except:
            print(RD+ "Invalid Choice, Try again!" + RS)

def getdirpath():
    return os.path.dirname(os.path.realpath(__file__))

def runserv(port, dir):
  
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=dir)
    socketserver.TCPServer.allow_reuse_address = True
    global httpd 
    httpd = socketserver.TCPServer(("", int(port)), handler)
    try:            
    #global httpd
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

def RunServer(ip,dir):
    Banner()
    if dir is None or dir is '':
        dir = getdirpath()
    files = os.listdir(dir)
    portSel = input(SB+WT+"Enter port (Press Enter for default: 8080): "+RS)
    method = ""
    while True:
        wgetOrCurl = input(SB+WT+"Method: Wget / Curl (press Enter Default (wget) or 'c' for curl: "+RS)
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
    #print("\n")
    print(SB+CY+ f"\nServing files..." + RS)
    runserv(portSel, dir)


if __name__ == '__main__':
    signal(SIGINT, handler)
    Banner()
    IPADDRESS = IPChoice()
    ap_parser = argparse.ArgumentParser()
    ap_parser.add_argument("-d", "--dir", help="directory to serve files from.", type=str)
    par = ap_parser.parse_args()
    if par.dir:
        dir = par.dir
    else:
        dir = ""
    RunServer(IPADDRESS,dir)







