#! /bin/bash

sudo ip route add 160.16.11.0/24  via  10.10.10.3 dev  controller-eth1
sudo ip route add 160.16.31.0/24  via  10.10.10.4 dev  controller-eth2
