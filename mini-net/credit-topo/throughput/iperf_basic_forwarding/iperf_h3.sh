#!/bin/bash




echo "Starting iperf traffic from h3(client2) to h2(server) ..."
iperf3 -c h2 -t 20 > iperf_client2_20s_1.txt
echo "iperf traffic from h3(client2) to h2(server) finished"

echo "Starting iperf traffic from h3(client2) to h2(server) ..."
iperf3 -c h2 -t 20 > iperf_client2_20s_2.txt
echo "iperf traffic from h3(client2) to h2(server) finished"

echo "Starting iperf traffic from h3(client2) to h2(server) ..."
iperf3 -c h2 -t 20 > iperf_client2_20s_3.txt
echo "iperf traffic from h3(client2) to h2(server) finished"

echo "Starting iperf traffic from h3(client2) to h2(server) ..."
iperf3 -c h2 -t 20 > iperf_client2_20s_4.txt
echo "iperf traffic from h3(client2) to h2(server) finished"

# echo "Starting iperf traffic from h3(client2) to h2(server) ..."
# iperf3 -c h2 -t 20 > iperf_client2_20s_qrate10_qdepth100_1.txt 
# echo "iperf traffic from h3(client2) to h2(server) finished"

# echo "Starting iperf traffic from h3(client2) to h2(server) ..."
# iperf3 -c h2 -t 20 > iperf_client2_20s_qrate10_qdepth100_2.txt 
# echo "iperf traffic from h3(client2) to h2(server) finished"

# echo "Starting iperf traffic from h3(client2) to h2(server) ..."
# iperf3 -c h2 -t 20 > iperf_client2_20s_qrate10_qdepth100_3.txt 
# echo "iperf traffic from h3(client2) to h2(server) finished"

# echo "Starting iperf traffic from h3(client2) to h2(server) ..."
# iperf3 -c h2 -t 20 > iperf_client2_20s_qrate10_qdepth100_4.txt 
# echo "iperf traffic from h3(client2) to h2(server) finished"
