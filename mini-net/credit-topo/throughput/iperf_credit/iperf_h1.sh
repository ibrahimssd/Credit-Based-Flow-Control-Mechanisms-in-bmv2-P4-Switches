#!/bin/bash


echo "Starting iperf traffic from h1(client1) to h2(server) ..."
iperf3 -c h2 -t 20 > iperf_client1_20s_qrate10_qdepth100_credit_1.txt 
echo "iperf traffic from h1(client1) to h2(server) finished"

sleep 5

echo "Starting iperf traffic from h1(client1) to h2(server) ..."
iperf3 -c h2 -t 20 > iperf_client1_20s_qrate10_qdepth100_credit_2.txt
echo "iperf traffic from h1(client1) to h2(server) finished"

sleep 5

echo "Starting iperf traffic from h1(client1) to h2(server) ..."
iperf3 -c h2 -t 20 > iperf_client1_20s_qrate10_qdepth100_credit_3.txt
echo "iperf traffic from h1(client1) to h2(server) finished"

sleep 5

echo "Starting iperf traffic from h1(client1) to h2(server) ..."
iperf3 -c h2 -t 20 > iperf_client1_20s_qrate10_qdepth100_credit_4.txt 
echo "iperf traffic from h1(client1) to h2(server) finished"

