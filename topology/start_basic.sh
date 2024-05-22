#!/bin/sh

echo "Starting S1 ..."
vagrant ssh s1 -c 'sudo simple_switch --device-id 1 -i 1@enp0s16 -i 2@enp0s17 -i 3@enp0s9 -i 4@enp0s10 --thrift-port 9091  /vagrant/packets-clone/build/basic.json ' &

# echo "Starting S2 ..."
# vagrant ssh s2 -c 'sudo simple_switch --device-id 2 -i 1@enp0s16 -i 2@enp0s10 -i 3@enp0s9 --thrift-port 9092 --notifications-addr tcp://10.10.1.101:10001 --log-console >/vagrant/packets-clone/logs/s2  /vagrant/packets-clone/build/basic.json &' &

# echo "Starting S3 ..."
# vagrant ssh s3 -c 'sudo simple_switch --device-id 3 -i 1@enp0s16 -i 2@enp0s17 -i 3@enp0s9 -i 4@enp0s10  --thrift-port 9093 --notifications-addr tcp://10.10.1.101:10001 --log-console >/vagrant/packets-clone/logs/s3  /vagrant/packets-clone/build/basic.json &' &

# echo "Starting S4 ..."
# vagrant ssh s4 -c 'sudo simple_switch --device-id 4 -i 1@enp0s16 -i 2@enp0s10 -i 3@enp0s9 --thrift-port 9094 --notifications-addr tcp://10.10.1.101:10001 --log-console >/vagrant/packets-clone/logs/s4  /vagrant/packets-clone/build/basic.json &' &

# echo "Adding the routing rules ..."
# vagrant ssh h11 -c 'sudo ip route add 172.16.12.0/24 via 172.16.11.100 dev enp0s8; sudo ip route add 172.16.20.0/24 via 172.16.11.100 dev enp0s8; sudo ip route add 172.16.31.0/24 via 172.16.11.100 dev enp0s8; sudo ip route add 172.16.32.0/24 via 172.16.11.100 dev enp0s8; sudo ip route add 172.16.40.0/24 via 172.16.11.100 dev enp0s8'
# vagrant ssh h12 -c 'sudo ip route add 172.16.11.0/24 via 172.16.12.100 dev enp0s8; sudo ip route add 172.16.20.0/24 via 172.16.12.100 dev enp0s8; sudo ip route add 172.16.31.0/24 via 172.16.12.100 dev enp0s8; sudo ip route add 172.16.32.0/24 via 172.16.12.100 dev enp0s8; sudo ip route add 172.16.40.0/24 via 172.16.12.100 dev enp0s8'
# vagrant ssh h2 -c 'sudo ip route add 172.16.11.0/24 via 172.16.20.100 dev enp0s8; sudo ip route add 172.16.12.0/24 via 172.16.20.100 dev enp0s8; sudo ip route add 172.16.31.0/24 via 172.16.20.100 dev enp0s8; sudo ip route add 172.16.32.0/24 via 172.16.20.100 dev enp0s8; sudo ip route add 172.16.40.0/24 via 172.16.20.100 dev enp0s8'
# vagrant ssh h31 -c 'sudo ip route add 172.16.11.0/24 via 172.16.31.100 dev enp0s8; sudo ip route add 172.16.12.0/24 via 172.16.31.100 dev enp0s8; sudo ip route add 172.16.20.0/24 via 172.16.31.100 dev enp0s8; sudo ip route add 172.16.32.0/24 via 172.16.31.100 dev enp0s8; sudo ip route add 172.16.40.0/24 via 172.16.31.100 dev enp0s8'
# vagrant ssh h32 -c 'sudo ip route add 172.16.11.0/24 via 172.16.32.100 dev enp0s8; sudo ip route add 172.16.12.0/24 via 172.16.32.100 dev enp0s8; sudo ip route add 172.16.31.0/24 via 172.16.32.100 dev enp0s8; sudo ip route add 172.16.20.0/24 via 172.16.32.100 dev enp0s8; sudo ip route add 172.16.40.0/24 via 172.16.32.100 dev enp0s8'
# vagrant ssh h4 -c 'sudo ip route add 172.16.11.0/24 via 172.16.40.100 dev enp0s8; sudo ip route add 172.16.12.0/24 via 172.16.40.100 dev enp0s8; sudo ip route add 172.16.31.0/24 via 172.16.40.100 dev enp0s8; sudo ip route add 172.16.32.0/24 via 172.16.40.100 dev enp0s8; sudo ip route add 172.16.20.0/24 via 172.16.40.100 dev enp0s8'

