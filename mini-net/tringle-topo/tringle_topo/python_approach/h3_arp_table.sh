#! /bin/bash
sudo ip route add 160.16.31.0/24  via  160.16.12.100 dev  h3-eth3
sudo ip route add 160.16.11.0/24 via 160.16.12.100 dev h3-eth3

