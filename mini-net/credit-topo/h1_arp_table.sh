#! /bin/bash
sudo ip route add 160.16.31.0/24  via  160.16.11.100 dev  h1-eth0
sudo ip route add 10.10.10.0/24  via  160.16.11.100 dev  h1-eth0
sudo ip route add 160.16.12.0/24 via 160.16.11.100 dev h1-eth0
