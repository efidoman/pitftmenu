#!/bin/bash

source /root/.bash_profile
cd /root/src/pitftmenu

COUNTER=0
while [  $COUNTER -lt 10 ]; do
  sleep 30
  ps aux | grep -v grep | grep -q 'menu_openaps.py' || /usr/bin/python ./menu_openaps.py | tee -a /var/log/openaps/menu-openaps.log
done
