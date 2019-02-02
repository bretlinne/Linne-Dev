#! /bin/bash

RED='\033[0;31m'
LT_RED='\033[1;31m'
LT_GREEN='\033[1;32m'
YELLOW='\033[1;33m'
LT_BLUE='\033[1;36m'
NC='\033[0m' # NO COLOR

source ./DetectOS.sh

APP_NAME=$1

function CreateAppEnvVar(){
	if [ ! -n "$APP_LNK" ]; then
		printf "${LT_GREEN} => Creating APP_LNK env var.\n${NC}"
		APP_LNK=$HOME/Desktop
	else
		printf "${LT_RED} => APP_LNK already exits.\n${NC}"
	fi
}

function InstallGeanyAndDependencies(){
	case ${OS_TYPE} in
	"CentOS Linux")
	    printf "${LT_GREEN} Detected OS is: ${LT_BLUE}${OS_TYPE}${NC}\n"
		# check if epel-release is installed
		#repoquery --nvr epel-release # alternate method using repoquery
		if [ ! -f /etc/yum.repos.d/epel.repo ]; then
			printf "${LT_GREEN} => installing Epel (Extended Packages for Enterprise-Linux).${NC}\n"
			yum -y install epel-release
		else
			printf "${LT_BLUE} => Epel.repo (Extended Packages for Enterprise-Linux) already installed!${NC}\n"
		fi
		
		#refresh the yum repolist
		printf "${LT_GREEN} => refreshing yum repolist.${NC}\n"
		#yum -q repolist`
		yum repolist -q | tr "\n" "#" | sed -e 's/# / /g' | tr "#" "\n" #| grep "epel*"
	    ;;
	"Ubuntu")
		printf "${LT_GREEN} Detected OS is: ${LT_BLUE}${OS_TYPE}${NC}\n"
	    ;;
	esac

	if [ ! -f /usr/bin/${APP_NAME} ]; then
		echo "doesn't exist"
	fi
	
}

function CreateAppDesktopIcon(){
	printf "${LT_GREEN} => Creating Desktop Icon for ${APP_NAME}.${NC}\n"
	touch ${APP_LNK}/${APP_NAME}.desktop
	echo "[Desktop Entry]" >> ${APP_LNK}/${APP_NAME}.desktop
	echo "Type=Application" >> ${APP_LNK}/${APP_NAME}.desktop
	echo "Version=1.0" >> ${APP_LNK}/${APP_NAME}.desktop
	echo "Name=${APP_NAME}" >> ${APP_LNK}/${APP_NAME}.desktop
	echo "GenericName=" >> ${APP_LNK}/${APP_NAME}.desktop
	echo "Comment=" >> ${APP_LNK}/${APP_NAME}.desktop
	echo "Exec=${APP_NAME} %F" >> ${APP_LNK}/${APP_NAME}.desktop
	echo "Icon=${APP_NAME}" >> ${APP_LNK}/${APP_NAME}.desktop
	echo "Terminal=false" >> ${APP_LNK}/${APP_NAME}.desktop
	echo "Categories=" >> ${APP_LNK}/${APP_NAME}.desktop
	echo "MimeType=text/plain;text/x-chdr;text/x-csrc;text/x-c++hdr;text/x-c++src;text/x-java;text/x-dsrc;text/x-pascal;text/x-perl;text/x-python;application/x-php;application/x-httpd-php3;application/x-httpd-php4;application/x-httpd-php5;application/xml;text/html;text/css;text/x-sql;text/x-diff;" >> ${APP_LNK}/${APP_NAME}.desktop
	echo "StartupNotify=true" >> ${APP_LNK}/${APP_NAME}.desktop
	echo "Keywords=" >> ${APP_LNK}/${APP_NAME}.desktop
	echo "X-Desktop-File-Install-Version=0.22" >> ${APP_LNK}/${APP_NAME}.desktop
	chmod 755 ${APP_LNK}/${APP_NAME}.desktop
}

#GetOSType

printf "${LT_GREEN}Setup Desktop Shortcut on ${OS_TYPE}\n${NC}"
printf "${LT_GREEN}*********************************${NC}\n"

CreateAppEnvVar

#Check if Desktop icon alread exists
if [ ! -f ${APP_LNK}/${APP_NAME}.desktop ]; then
    CreateAppDesktopIcon    
else
    printf "${LT_BLUE} => ${APP_NAME} shortcut already exists!\n${NC}"
fi

#printf "${LT_BLUE}\n=> Look in CentOS' 'Applications' tab, under 'Programming'.${NC}\n"
