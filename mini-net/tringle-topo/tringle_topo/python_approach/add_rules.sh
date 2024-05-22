#!/bin/bash

echo "Adding rules for s1 ..."
simple_switch_CLI --thrift-ip 10.10.1.101  --thrift-port 9091 < s1-commands.txt

