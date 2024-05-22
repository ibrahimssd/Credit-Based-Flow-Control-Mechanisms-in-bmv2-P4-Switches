#!/bin/bash

echo "Adding rules for s1 ..."
simple_switch_CLI  --thrift-port 9091 < switch_rules/s1-basic-rules.txt

echo "Adding rules for s2 ..."
simple_switch_CLI  --thrift-port 9092 < switch_rules/s2-basic-rules.txt




