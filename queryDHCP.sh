#!/bin/bash

pid=$$

while read i
do
        echo $i | egrep -qi '^lease|hardware|starts|ends|hostname' || continue
        if [[ $i =~ [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3} ]]; then
                ip=$(echo $i | awk '{print $2}')
                printf "IP Address: " > /root/$ip.$pid
                echo $ip >> /root/$ip.$pid
        elif [[ $i =~ starts ]]; then
                printf "\tLease start: " >> /root/$ip.$pid
                echo $i | awk '{print $3,$4}' | tr -d ';' >> /root/$ip.$pid
        elif [[ $i =~ ends ]]; then
                printf "\tLease ends: " >> /root/$ip.$pid
                echo $i | awk '{print $3,$4}' | tr -d ';' >> /root/$ip.$pid
        elif [[ $i =~ ethernet ]]; then
                mac=$(echo -n $i | awk '{print $3}' | tr -d ';')
                oui=$(echo -n $mac | tr ':' '-' | cut -c1-8)

                printf "\tMAC Address: " >> /root/$ip.$pid
                echo $mac >> /root/$ip.$pid
                printf "\tManufacturer: " >> /root/$ip.$pid
                grep -i $oui /usr/share/hwdata/oui.txt | awk '{print $3,$4,$5,$6}' >> /root/$ip.$pid
                printf "\n" >> /root/$ip.$pid
        elif [[ $i =~ hostname ]]; then
                printf "\tHostname: " >> /root/$ip.$pid
                echo $i | awk '{print $2}' | tr -d ';' >> /root/$ip.$pid
        fi

done < /var/lib/dhcpd/dhcpd.leases

cat /root/*.$pid
echo "Total leased: $(ls -l /root/*.$pid | wc -l)"
rm -rf /root/*.$pid
