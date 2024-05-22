#! /bin/bash
sudo ip route add 160.16.31.0/24  via  160.16.11.100 dev  h1-eth1
sudo ip route add 160.16.12.0/24 via 160.16.11.100 dev h1-eth1
