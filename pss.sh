#!/bin/bash

GN="\e[32m"
RES="\e[0m"
CYAN="\e[1;36m"

echo -e "\n$CYAN""Python FileServer$RES"
echo -e "Created By$GN Ac1d $RES\n"

HN="hostname -I"
res=$(eval $HN)
arrIN=(${res// / })
IP=""

if [ ${#arrIN[@]} -gt 1 ]; then
        PS3='	Which Ip address, 1 or 2?: '
        options=("Option 1: ${arrIN[0]}" "Option 2: ${arrIN[1]}" "Quit")
        select opt in "${options[@]}"
        do
        case $opt in
                "Option 1: ${arrIN[0]}")
                        IP="${arrIN[0]}"
                        #echo "you chose choice 1"
                        break
                ;;

                "Option 2: ${arrIN[1]}")
                        IP="${arrIN[1]}"
                        #echo "you chose choice 2"
                        break
                ;;
                "Quit")
                break
                ;;
                *) echo "invalid option $REPLY";;
        esac
        done
else
       IP=$arrIN

fi
echo "IP: "$IP
echo -e "File links...\n"
for entry in `ls`;do
	if  [  ! -d $entry  ];then
		wgetCmd=$(echo "wget ${IP##*( )}/$entry" | xargs)
		echo -e "\t$GN$wgetCmd$RES"
	fi
done
echo -e "\nCurrent Directory Content...\n"
ls --color $PWD
echo -e "\nStarting Server"
sudo python3 -m http.server 80  -d .
