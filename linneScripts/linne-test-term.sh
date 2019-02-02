#!/bin/bash
colour=0
if tput Co > /dev/null 2>&1
then
    test "`tput Co`" -gt 2 && colour=1
elif tput colors > /dev/null 2>&1
then
    test "`tput colors`" -gt 2 && colour=1
fi
