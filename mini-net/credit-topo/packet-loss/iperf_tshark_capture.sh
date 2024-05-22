#!/bin/bash
echo " capturing packets ........"

# tshark 
# -i: interface
# -w: write to file
# -F: output file format
# -f: filter
# -a: autostop condition
# -b: ring buffer
# -B: buffer size
# -c: packet count
# -s: snap length
# -S: absolute timestamp
# -t: timestamp format
# -T: output format
# -x: hex and ASCII dump
# -X: hex dump
# -V: verbose output
# -e: field to print


# # Define the file names for full bandwidth
# file_names=("client_rtt60s_tcp20s_fullbandwidth_1.pcap"
#             "client_rtt60s_tcp20s_fullbandwidth_2.pcap"
#             "client_rtt60s_tcp20s_fullbandwidth_3.pcap"
#             "client_rtt60s_tcp20s_fullbandwidth_4.pcap")

# # Run iperf and tshark for each file name
# for ((i=0; i<${#file_names[@]}; i++))
# do
#     # Run iperf traffic
#     echo "running iperf3 for 20 seconds"
#     iperf3 -c h2 -t 20  &
#     # Start capturing packets
#     echo "running tshark for 20 seconds"
#     sudo tshark -i h1-eth0 -w "client_pcaps_basic/${file_names[i]}" -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100" &

#     # Wait for iperf and tshark to complete
#     echo "sleeping for 25 seconds"
#     sleep 25

#     # Stop capturing packets
#     echo "stopping tshark"
#     sudo pkill tshark
# done


# # define the file names for queue rate 10 and queue depth 100
# file_names=("client_rtt60s_tcp20s_qrate10_qdepth100_1.pcap"
#             "client_rtt60s_tcp20s_qrate10_qdepth100_2.pcap"
#             "client_rtt60s_tcp20s_qrate10_qdepth100_3.pcap"
#             "client_rtt60s_tcp20s_qrate10_qdepth100_4.pcap")
# # Run iperf and tshark for each file name
# for ((i=0; i<${#file_names[@]}; i++))
# do
#     # Run iperf traffic
#     echo "Running iperf3 for 20 seconds"
#     iperf3 -c h2 -t 10 &

#     # Start capturing packets
#     echo "Running tshark for 20 seconds"
#     sudo tshark -i h1-eth0 -w "client_pcaps_basic/${file_names[i]}" -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100" &

    
#     # Wait for iperf and tshark to complete
#     sleep 15

#     # Stop capturing packets
#     echo "Stopping tshark"
#     sudo pkill tshark

#     # Wait for a few seconds before the next iteration
#     sleep 5
# done




# capture filter (capture filters are used to selectively capture specific packets during the capture process itself)
# FULL BANDWIDTH (sniffing on h1) (NO QUEUEING)
# sudo tshark -i h1-eth0 -w client_pcaps_basic/client_rtt60s_tcp20s_fullbandwidth_1.pcap  -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100"
# sudo tshark -i h1-eth0 -w client_pcaps_basic/client_rtt60s_tcp20s_fullbandwidth_2.pcap  -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100"
# sudo tshark -i h1-eth0 -w client_pcaps_basic/client_rtt60s_tcp20s_fullbandwidth_3.pcap  -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100"
# sudo tshark -i h1-eth0 -w client_pcaps_basic/client_rtt60s_tcp20s_fullbandwidth_4.pcap  -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100"



# BASIC FORWARDING
# ( queue rate 10 and queue depth 100 sniffing on h1 )
# sudo tshark -i h1-eth0 -w client_pcaps_basic/client1_rtt60s_tcp20s_qrate10_qdepth100_1.pcap  -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100" 
# sudo tshark -i h1-eth0 -w client_pcaps_basic/client1_rtt60s_tcp20s_qrate10_qdepth100_2.pcap  -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100" 
# sudo tshark -i h1-eth0 -w client_pcaps_basic/client1_rtt60s_tcp20s_qrate10_qdepth100_3.pcap  -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100" 
# sudo tshark -i h1-eth0 -w client_pcaps_basic/client1_rtt60s_tcp20s_qrate10_qdepth100_4.pcap  -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100" 
# sudo tshark -i h1-eth0 -w client_pcaps_basic/client1_rtt60s_tcp20s_qrate10_qdepth100_5.pcap  -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100" 

# BASIC FORWARDING
# ( queue rate 10 and queue depth 100 sniffing on switch1 )
# sudo tshark -i s1-eth2 -w client_pcaps_basic/switch1_rtt60s_tcp20s_qrate10_qdepth100_1.pcap  -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100" 
# sudo tshark -i s1-eth2 -w client_pcaps_basic/switch1_rtt60s_tcp20s_qrate10_qdepth100_2.pcap  -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100" 
# sudo tshark -i s1-eth2 -w client_pcaps_basic/switch1_rtt60s_tcp20s_qrate10_qdepth100_3.pcap  -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100" 
# sudo tshark -i s1-eth2 -w client_pcaps_basic/switch1_rtt60s_tcp20s_qrate10_qdepth100_4.pcap  -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100" 
# sudo tshark -i s1-eth2 -w client_pcaps_basic/switch1_rtt60s_tcp20s_qrate10_qdepth100_5.pcap  -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100" 





# Credi set up (sniffing on h1) 
# sudo tshark -i h1-eth0 -w client_pcaps_credits/client1_rtt60s_tcp20s_qrate10_qdepth100_credits_1.pcap  -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100" 
# sudo tshark -i h1-eth0 -w client_pcaps_credits/client1_rtt60s_tcp20s_qrate10_qdepth100_credits_2.pcap  -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100"
# sudo tshark -i h1-eth0 -w client_pcaps_credits/client1_rtt60s_tcp20s_qrate10_qdepth100_credits_3.pcap  -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100"
# sudo tshark -i h1-eth0 -w client_pcaps_credits/client1_rtt60s_tcp20s_qrate10_qdepth100_credits_4.pcap  -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100"
# sudo tshark -i h1-eth0 -w client_pcaps_credits/client1_rtt60s_tcp20s_qrate10_qdepth100_credits_5.pcap  -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100"



# Credi set up (sniffing on S1 switch)
# sudo tshark -i s1-eth2 -w client_pcaps_credits/switch1_rtt60s_tcp20s_qrate10_qdepth100_credits_1.pcap  -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100"
# sudo tshark -i s1-eth2 -w client_pcaps_credits/switch1_rtt60s_tcp20s_qrate10_qdepth100_credits_2.pcap  -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100"
# sudo tshark -i s1-eth2 -w client_pcaps_credits/switch1_rtt60s_tcp20s_qrate10_qdepth100_credits_3.pcap  -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100"
# sudo tshark -i s1-eth2 -w client_pcaps_credits/switch1_rtt60s_tcp20s_qrate10_qdepth100_credits_4.pcap  -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100"
sudo tshark -i s1-eth2 -w client_pcaps_credits/switch1_rtt60s_tcp20s_qrate10_qdepth100_credits_5.pcap  -f "tcp and src host 160.16.11.100 and dst host 160.16.31.100"




# Credit set up (sniffing on h3)
# sudo tshark -i h3-eth0 -w client_pcaps_credits/client3_rtt60s_tcp20s_qrate10_qdepth100_credits_1.pcap  -f "tcp and src host 160.16.12.100 and dst host 160.16.31.100"
# sudo tshark -i h3-eth0 -w client_pcaps_credits/client3_rtt60s_tcp20s_qrate10_qdepth100_credits_2.pcap  -f "tcp and src host 160.16.12.100 and dst host 160.16.31.100" 
# sudo tshark -i h3-eth0 -w client_pcaps_credits/client3_rtt60s_tcp20s_qrate10_qdepth100_credits_3.pcap  -f "tcp and src host 160.16.12.100 and dst host 160.16.31.100" 
# sudo tshark -i h3-eth0 -w client_pcaps_credits/client3_rtt60s_tcp20s_qrate10_qdepth100_credits_4.pcap  -f "tcp and src host 160.16.12.100 and dst host 160.16.31.100"
# sudo tshark -i h3-eth0 -w client_pcaps_credits/client3_rtt60s_tcp20s_qrate10_qdepth100_credits_5.pcap  -f "tcp and src host 160.16.12.100 and dst host 160.16.31.100" 
# sudo tshark -i h3-eth0 -w client_pcaps_credits/client3_rtt60s_tcp20s_qrate10_qdepth100_credits_6.pcap  -f "tcp and src host 160.16.12.100 and dst host 160.16.31.100"


