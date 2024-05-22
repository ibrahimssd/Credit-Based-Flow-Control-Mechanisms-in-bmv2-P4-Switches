#!/bin/bash

echo "Adding rules for s1 ..."
simple_switch_CLI --thrift-ip 10.10.1.101 --thrift-port 9091 < topology/s1-basic-rules.txt


# echo "Adding rules for s2 ..."
# simple_switch_CLI --thrift-ip 10.10.1.102 --thrift-port 9092 < topology/s2-basic-rules.txt

# echo "Adding rules for s3 ..."
# simple_switch_CLI --thrift-ip 10.10.1.103 --thrift-port 9093 < topology/s3-basic-rules.txt

# echo "Adding rules for s4 ..."
# simple_switch_CLI --thrift-ip 10.10.1.104 --thrift-port 9094 < topology/s4-basic-rules.txt

