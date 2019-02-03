#!/usr/bin/env bash


#This script is supposed to add anything in here to the existing .gitignore
#file.  Idempotent script.
#- if gitignore doesn't exist, create it and write all this content
#- if gitignore exists, add anything not included here.
#- if gitignore exists and has everything here, do nothing.

# read from git gist containing the gitignores
# select from multiple options for basic, or a host of languages
# each selection of language/framework adds the gitignore types idempotently

RED='\033[0;31m'
LT_RED='\033[1;31m'
LT_GREEN='\033[1;32m'
YELLOW='\033[1;33m'
LT_BLUE='\033[1;36m'
NC='\033[0m' # NO COLOR

REPOROOT=`git rev-parse --show-toplevel`
REPOROOT="$REPOROOT/foo-delete-me/"

function checkIfGitIgnoreExistsCreateIfNot(){
    if [ -a "$REPOROOT.gitignore" ]; then
      echo "exists"
    else
      printf "${YELLOW} => .gitignore doesn't exist.\n${NC}"
      cp /dev/null "${REPOROOT}.gitignore"
      RESULT=$?
      if [ $RESULT -eq 0 ] && [ -a "$REPOROOT.gitignore" ]; then
        printf "${LT_BLUE} => Creating .gitignore in repo root:\n${REPOROOT}\n${NC}"
      else
        printf "${YELLOW} Error: We require more vespene gas.\n${NC}"
      fi
    fi
}

function 
#if grep -a -q "foo" ".gitignore"; then
#  echo "found foo"
#else
#  echo "not found"
#fi

while true; do
    printf "${BLUE} Menu\t\t      IP Addr: ${LT_GREEN}${LOCAL_IP}${BLUE}\n"    
    echo " *********************************************"
    printf "${LT_GREEN} a) Check Ports 30025-30040\n"
    printf "${LT_GREEN} b) Check Ports 1-1023\n"
    printf "${YELLOW} c) Check Ports 1-30024 ${LT_RED}(this may take awhile) \n"
    printf "${LT_RED} x) Exit\n"
    printf "\n$NC"
    read -p " Please make a selection: " userInput
    case $userInput in
        [Aa]* ) checkPorts false; continue;;
        [Bb]* ) checkPortRange 1 1023; continue;;
        [Cc]* ) checkPortRange 1 30024; continue;;
        [XxQq]* ) break;;
        *) echo -e "\n$NC" + "Please answer with a, b, c, or x.";;
    esac
done

