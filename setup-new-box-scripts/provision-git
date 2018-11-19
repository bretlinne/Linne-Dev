#! /usr/bin/env bash

LT_RED='\033[1;31m'
LT_GREEN='\033[1;32m'
YELLOW='\033[1;33m'
LT_BLUE='\033[1;36m'
NC='\033[0m' # NO COLOR

#DIR="${BASH_SOURCE%/*}"

#if [[ ! -d "$DIR" ]]; then 
#	DIR="$PWD"; 
#fi
#printf "${LT_BLUE} ?: ${?}\n${NC}"

#source . "$DIR/DetectOS.sh"
#. "$DIR/main.sh"

# "OS_TYPE" & VERSION variable comes from here:
source ./DetectOS.sh

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
	#printf "GIT_INSTALLED (inside check): ${GIT_INSTALLED}\n"
	#-------------------------------------------------------------------
	#exec 3>&2			# link file desc 3 w/ stderr
	#exec 2> /dev/null
	
	#SILENT_MODE=$1
	
    #if [[ ! $(git --version) ]]; then
	    #if [ SILENT_MODE ]; then
			#printf "${LT_RED} GIT IS NOT INSTALLED.\n"
		#fi
		#continue
	#else
		#if [ SILENT_MODE ]; then
			#printf "${LT_BLUE} GIT IS CURRENTLY INSTALLED.\n"
		#fi
		#continue
	#fi
	#GIT_INSTALLED=$?
	##turn back on the stderr notifications
	#exec 2>&3 3>&-      # Restore stdout and close file descriptor #3
	
	# critique of this commented-out code.  The bottom "2>&3 3>&-" is not 
	# executing because of the continues.  the continues cause an immediate return from
	# the function to the main loop, as well as a return to the while-true loop
	
	# my logic on SILENT_MODE is backwards.  "if SILENT_MODE is true, report extra information"
	# it's suggested to either go with "if [ "$SILENT_MODE" = false ]" or call the var 
	# VERBOSE_MODE
	
	# "if [ SILENT_MODE ]" always evals to 'true' it's really testing whether the string is
	# non-null.  I seem to want "if [ "$SILENT_MODE" ]"
	
	# But this may be fooling myself. If I invoke the function as 'CheckGit false' (as I did
	# with the true version) then the test will still eval to true, because it's still testing
	# for non-null
	
	# $? is very ephemeral.  It is the result of the very last command issued.  The way I have 
	# it structured has it picking up the result of the printf statement, not the if test.  I need to
	# set the status of GIT_INSTALLED earlier if I want that.	 
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
		[Ee]* ) printf "${LT_BLUE} OS: ${OS_TYPE}\n${NC}"
				printf "${LT_BLUE} DIR: ${DIR}\n${NC}"; continue;;
		[Hh]* ) Help; continue;;
		[XxQq]* ) break;;
		* ) printf "\n${NC} Please answer with a, b, c, d, x(or q).";;
	esac
done
