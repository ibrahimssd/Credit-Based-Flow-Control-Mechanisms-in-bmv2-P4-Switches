#!/bin/sh

echo "killing simple_switch process on  s1 ..."
vagrant ssh s1 -c 'sudo pkill -9 -x simple_switch'


echo "killing simple_switch process on  s2 ..."
vagrant ssh s2 -c 'sudo pkill -9 -x simple_switch'



echo "killing simple_switch process on  s3 ..."
vagrant ssh s3 -c 'sudo pkill -9 -x simple_switch'


echo "killing simple_switch process on  s4 ..."
vagrant ssh s4 -c 'sudo pkill -9 -x simple_switch'



#vagrant ssh controller -c 'python /vagrant/controller/database.py clear'

rm /root/credit-mininet/packets-clone/logs/*
