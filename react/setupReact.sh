#! /bin/bash

#PKG_MGR_YUM=False
#PKG_MGR_APT=False

function checkPkgMgr(){
	if [ -n "$(command -v yum)" ]; then
	  #PKG_MGR_YUM=true
	  printf "yum\n"
	fi
	if [ -n "$(command -v apt-get)" ]; then
	  #PKG_MGR_APT=true
	  printf "apt\n"
	fi
}

#if [ "$PKG_MGR_YUM" = true ]; then
	#printf "yum\n"
	#yum install -y gcc c++ make
#fi
#if [ "$PKG_MGR_APT" = true ]; then
	#printf "apt\n"
	#apt install -y gcc c++ make
#fi
