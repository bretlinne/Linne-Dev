#!/bin/bash

RED='\033[0;31m'
LT_RED='\033[1;31m'
LT_GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;36m'
NC='\033[0m'  # NO COLOR

RUN_ONCE=false

function aptUpdate(){
	if ! ${RUN_ONCE}; then
		yes y | sudo apt update
		#sudo apt upgrade
		${RUN_ONCE}=true
	else
		printf "\n${YELLOW} Update already run!\n"
	fi
}

function installShutter(){
    if [ ! -f /usr/bin/shutter ]; then
		yes y | sudo apt install shutter
		printf "${LT_GREEN} => installing Shutter.${NC}\n"
    else
        printf "${LT_BLUE} => Shutter already installed!${NC}\n"
    fi
}

function installPythonPip(){
	if [ ! -f /usr/bin/pip ]; then
		yes y | sudo apt install python-pip
		printf "${LT_GREEN} => installing python-pip.${NC}\n"
	else
		printf "${LT_BLUE} => Pip already installed!${NC}\n"
		pip -V
		pip install --upgrade pip
		printf "${LT_BLUE} => Upgrading Pip...${NC}\n"
		pip -V
	fi
}

function installNetTools(){
	if [ ! -f /usr/bin/pip ]; then
		yes y | sudo apt install net-tools
		printf "${LT_GREEN} => installing net-tools.${NC}\n"
	else
		printf "${LT_BLUE} => net-tools already installed!${NC}\n"
		#pip -V
		#pip install --upgrade pip
		printf "${LT_BLUE} => Upgrading net-tools...${NC}\n"
		#pip -V
	fi
}

#yes y | sudo apt install idle2
#printf "${LT_GREEN} => installing idle2.${NC}\n"
while true; do
    printf "${BLUE} Menu\t\t      IP Addr: ${LT_GREEN}${LOCAL_IP}${BLUE}\n"    
    echo " *********************************************"
    printf "${LT_GREEN} z) apt update\n"
    printf "${LT_GREEN} a) Install Shutter (a screen capture tool)\n"
    printf "${LT_GREEN} b) Install Pip (python library manager)\n"
    printf "${LT_GREEN} c) Install Net-tools (basic Linux networking toolkit) \n"
    printf "\n${LT_GREEN} d) Install All\n"
    printf "${LT_RED} x) Exit\n"
    printf "\n$NC"
    read -p " Please make a selection: " userInput
    case $userInput in
        [Zz]* ) aptUpdate; continue;;
        [Aa]* ) installShutter; continue;;
        [Bb]* ) installPythonPip; continue;;
        [Cc]* ) installNetTools; continue;;
        [XxQq]* ) break;;
        *) echo -e "\n$NC" + "Please answer with a, b, c, or x.";;
    esac
done
