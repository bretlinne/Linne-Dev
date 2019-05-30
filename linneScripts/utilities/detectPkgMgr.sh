#!/bin/bash

## in .bash_profile
if [ -n "$(which apt 2>/dev/null)" ]; then
  printf "apt exists\n"
elif [ -n "$(which yum 2>/dev/null)" ]; then
  printf "yum exists\n"
fi
