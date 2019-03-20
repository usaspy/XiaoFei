#!/bin/bash

#sed -i 's/\r$//' internet.sh
count=0
times=0
res=0
while [ 1 ]; do
      count=`ping 61.139.2.69 -c 1 -s 1 -W 1 | grep " 0% packet loss" | wc -l`
      if [ ${count} != 1 ]; then
           times=$((times+1))

           if [ ${times} == 5 ]; then
                echo "start reconnect" > /internet.log
                pppd call gprs & >> /internet.log
                ip a | grep ppp0 &> /dev/null
                if [ $? == 0 ]; then
                   route del default dev ppp0
                   route add default dev ppp0
                   if [ $? == 0 ]; then
                      echo "set default route success!" >> /internet.log
                   else
                      echo "set default route fail!" >> /internet.log
                   fi
                else
                   echo "net card ppp0 is not found!" >> /internet.log
                fi
                times=0
           fi
      else
           times=0
           sleep 1
      fi
      echo $times >> /internet.log
done