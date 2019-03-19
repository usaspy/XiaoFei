#!/bin/bash

count=0
times=0
res=0
while [ 1 ]; do
      count=`ping 61.139.2.69 -c 1 -s 1 -W 1 | grep " 0% packet loss" | wc -l`
      if [ ${count} != 1 ]; then
           times=$((times+1))

           if [ ${times} == 5 ]; then
                echo "start reconnect"
                ppp call gprs &
                ip a | grep ppp0 &> /dev/null
                if [ $? == 0 ]; then
                   route del default dev ppp0
                   route add default dev ppp0
                   if [ $? == 0 ]; then
                      echo "set default route success!"
                   else
                      echo "set default route fail!"
                   fi
                else
                   echo "net card ppp0 is not found!"
                fi
                times=0
           fi
      else
           sleep 1
      fi
      echo $times
done