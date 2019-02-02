#!/bin/bash

BG_DEFAULT=49
BG_LOWBIT_RANGESTART=40
BG_LOWBIT_RANGEEND=47
BG_HIGHBIT_RANGESTART=100
BG_HIGHBIT_RANGEEND=107
FG_DEFAULT=39
FG_LOWBIT_RANGESTART=30
FG_LOWBIT_RANGEEND=37
FG_HIGHBIT_RANGESTART=90
FG_HIGHBIT_RANGEEND=97

COUNT=0
DELIMITER=1
MAX_COL=18
for clbg in {40..47} {100..107} ${BG_DEFAULT} ; do
        for clfg in {30..37} {90..97} ${FG_DEFAULT} ; do
                for attr in 0 1 2 4 5 7 ; do
                        echo -en "\e[${attr};${clbg};${clfg}m Foo\e[0m"
                        ((COUNT++))

                if [ $(((COUNT + 1) % ${MAX_COL})) == ${DELIMITER} ] ; then
                   echo
                fi
                done
        done
done

exit 0
