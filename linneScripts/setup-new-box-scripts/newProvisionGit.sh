#! /usr/bin/env bash

LT_RED='\033[1;31m'
LT_GREEN='\033[1;32m'
YELLOW='\033[1;33m'
LT_BLUE='\033[1;36m'
NC='\033[0m' # NO COLOR

OS_TYPE=''
VERSION=''
function GetOSType(){
	if [ -f /etc/os-release ]; then
		# freedesktop.org & systemd
		. /etc/os-release
		OS_TYPE=$NAME
		VERSION=$VERSION_ID
	elif type lsb_release >/dev/null 2>$1; then
		# linuxbase.org
		OS_TYPE=$(lsb_release -si)
		VERSION=$(lsb_release -sr)    
	fi
}

function GitInstall(){
	CheckGit $BOOLFalse
	# evaluate if git is NOT installed
	if [ ${GIT_INSTALLED} -ne 0 ];then	
		printf "${LT_GREEN} Detected OS is: ${LT_BLUE}${OS_TYPE}${NC}\n"
			
		if [ -z ${PASSWORD} ]; then
			GetCredentials
		fi
		CheckGitDir
		case ${OS_TYPE} in
		"CentOS Linux")
			printf "${LT_GREEN} => Installing git on CentOS...\n${NC}"
			echo ${PASSWORD} | sudo -S yum install git -y
			;;
		"Ubuntu")
			printf "${LT_GREEN} => apt updating...\n${NC}"
			echo ${PASSWORD} | sudo -S apt update
			printf "${LT_GREEN} => Installing git on ubuntu...\n${NC}"
			echo ${PASSWORD} | sudo -S apt install git -y
			;;
    "Amazon Linux AMI")
      printf "${LT_GREEN} => yum updating...\n${NC}"
      echo ${PASSWORD} | sudo -S yum update
      printf "${LT_GREEN} => Installing git on ${OS_TYPE}...\n${NC}"
      echo ${PASSWORD} | sudo -S yum install git -y
      ;;
		* ) 
			printf "${LT_RED} CASE NEEDED FOR ${OS_TYPE}\n.${NC}"
			;;
		esac
		git --version
		printf "${LT_BLUE} Git install COMPLETE!\n${NC}"
	else
		printf "${YELLOW} GIT ALREADY INSTALLED!\n${NC}"
	fi
}

function GitUninstallAndClean() {
	CheckGit $BOOLFalse
	# Evaluate if git IS installed
	if [ ${GIT_INSTALLED} -eq 0 ];then	
		if [ -z ${PASSWORD} ]; then
			GetCredentials
		fi
		case ${OS_TYPE} in
		"CentOS Linux")
			printf "${LT_GREEN} => Removing git from CentOS...\n${NC}"
			echo ${PASSWORD} | sudo -S yum remove git -y
			printf "${LT_GREEN} => Clean all...\n${NC}"
			echo ${PASSWORD} | sudo -S yum clean all -y
			;;
		"Ubuntu")
			printf "${LT_GREEN} => Removing git from Ubuntu...\n${NC}"
			echo ${PASSWORD} | sudo -S apt remove git -y
			printf "${LT_GREEN} => Clean all...\n${NC}"
			echo ${PASSWORD} | sudo -S apt clean all -y
			;;	
		* ) 
			printf "${LT_RED} CASE NEEDED FOR ${OS_TYPE}\n.${NC}"
			;;
		esac
		printf "${LT_BLUE} Git uninstall & clean COMPLETE\n${NC}"
	else
		printf "${LT_RED} GIT CURRENTLY NOT INSTALLED!\n${NC}"
	fi
}

function Help(){
	printf " *****************************************************************************\n"
	printf " * ${LT_BLUE}Install Git: ${NC}a clean install.                                             *\n"
	printf " * ${LT_BLUE}Uninstall Git and Clean:${NC}                                                  *\n"
	printf " *   Take off and nuke the site from orbit; It's the only way to be sure.    *\n"
	printf " *   Sometimes bad copies are cached in the local filesystem and are re-used *\n"
	printf " *   when merely re-installing.                                              *\n"
	printf " * ${LT_BLUE}Re-Install Git: ${NC}Downloads the package, uncompresses it and re-installs it.*\n"
	printf " *****************************************************************************\n"
}

function GitReinstall(){	
	CheckGit ${BOOLFalse}
	# Evaluate if git IS installed
	if [ ${GIT_INSTALLED} -eq 0 ];then	
		if [ -z ${PASSWORD} ]; then
			GetCredentials
		fi
		CheckGitDir	
	
		case ${OS_TYPE} in
		"CentOS Linux")
			printf "${LT_GREEN} => Re-installing git on CentOS...\n${NC}"
			echo ${PASSWORD} | sudo -S yum reinstall git -y
			;;
		"Ubuntu")
			printf "${LT_GREEN} => Re-installing git on Ubuntu...\n${NC}"
			echo ${PASSWORD} | sudo -S apt reinstall git -y
			;;
		* ) 
			printf "${LT_RED} CASE NEEDED FOR ${OS_TYPE}\n.${NC}"
			;;	
		esac
		printf "${LT_BLUE} Git Re-Installation COMPLETE\n${NC}"
	else
		#Give notice that Git is not installed and call install routine
		printf "${YELLOW} Git not installed--INSTALLING NOW...\n${NC}"
		GitInstall
	fi
}

function GetCredentials () {
	read -p " Enter your sudo password: " PASSWORD
}

function CheckGit() {
	VERBOSE_MODE=$1
	
    if git --version >/dev/null 2>&1; then
		GIT_INSTALLED=$?
	    if [ "$VERBOSE_MODE" == true ]; then
			printf "${LT_BLUE} GIT IS CURRENTLY INSTALLED.\n"
		fi
	else
		GIT_INSTALLED=$?
		if [ "$VERBOSE_MODE" == true ]; then
			printf "${LT_RED} GIT IS NOT INSTALLED.\n"
		fi
	fi
}

function CheckGitDir (){
	if [ ! -d ~/Git ]; then
		printf "${LT_GREEN} => Making ~/Git directory\n${NC}"
		mkdir ~/Git
	else
		printf "${YELLOW} => ~/Git directory already exists...\n${NC}"
	fi
}

BOOLTrue=true
BOOLFalse=false
while true; do
	printf "${LT_BLUE} Menu\n"
	printf " ***********************************************\n"
	printf "${LT_GREEN} a) Install git.\n"
	printf "${LT_GREEN} b) Uninstall git and full clean.\n"
	printf "${LT_GREEN} c) Re-Install git.\n"
	printf "${LT_GREEN} d) Check git.\n"
	printf "${LT_GREEN} e) Check OS.\n"
	printf "${LT_GREEN} h) Help.\n"
	printf "${LT_RED} x) Exit.\n"
	printf "\n${NC}"
	
	read -p " Please make a selection: " eotuyx
	case $eotuyx in
		[Aa]* ) GitInstall; continue;;
		[Bb]* ) GitUninstallAndClean; continue;;
		[Cc]* ) GitReinstall; continue;;
		[Dd]* ) CheckGit $BOOLTrue; continue;;
		[Ee]* ) GetOSType;
                        printf "${LT_BLUE} OS: ${OS_TYPE}\n${NC}"
            		printf "${LT_BLUE} DIR: ${DIR}\n${NC}"; continue;;
		[Hh]* ) Help; continue;;
		[XxQq]* ) break;;
		* ) printf "\n${NC} Please answer with a, b, c, d, x(or q).";;
	esac
done
