#! /bin/bash

# This script finds the OS Type and Version by looking either at the
# /etc/os-release file (available on many systems, or invoking 'lsb_release'
# to get the info, which is also available on many systems.  More cases 
# may be added to increase the robustness of the script.  

# usage: in any script needing OS_TYPE and VERSION, add this as long as 
# file's in same directory.
# source ./DetectOS.sh

function GetOSType(){
	#OLDER, UGLIER WAY OF DOING THINGS:
	#----------------------------------
	#Get the os-release file's first line.  Couldn't get this to work
	#without it spitting out the first key of the next line
	#OS_TYPE=$(awk -F= '/^NAME/{print $2}' /etc/os-release)

	#Get the os-release file's first line
	# OS_TYPE=$(awk "NR==1{print;exit}" /etc/os-release)
	# OS_TYPE_PREFIX='NAME='
	# OS_TYPE=${OS_TYPE#$OS_TYPE_PREFIX} 	#string out NAME=

	#string out the "s
	# OS_TYPE=${OS_TYPE#\"}
	# OS_TYPE=${OS_TYPE%\"}
	#This line removes the quotes on one step, but may be less portable between shells
	#OS_TYPE=${OS_TYPE//\"/} 			
	
	#BETTER WAY:
	#----------------------------------
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
GetOSType
export OS_TYPE
export VERSION
