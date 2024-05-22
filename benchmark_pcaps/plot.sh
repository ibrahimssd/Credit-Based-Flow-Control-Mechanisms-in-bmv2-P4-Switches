#!/bin/bash
echo "processing pcap files ........"
echo "connection type " $1

if [ $1 -eq 6 ]
then
    python3 pcap_process.py --sender sender_tcp_15s_1.pcap,sender_tcp_15s_2.pcap,sender_tcp_15s_3.pcap,sender_tcp_15s_4.pcap,sender_tcp_15s_5.pcap,sender_tcp_15s_6.pcap   --server server_tcp_15s_1.pcap,server_tcp_15s_2.pcap,server_tcp_15s_3.pcap,server_tcp_15s_4.pcap,server_tcp_15s_5.pcap,server_tcp_15s_6.pcap

elif [ $1 -eq 17 ]
then
    python3  pcap_process.py --sender sender_tcp_15s_1.pcap,sender_tcp_15s_2.pcap,sender_tcp_15s_3.pcap,sender_tcp_15s_4.pcap,sender_tcp_15s_5.pcap,sender_tcp_15s_6.pcap   --server server_udp_20s_1.pcap,server_udp_20s_2.pcap,server_udp_20s_3.pcap,server_udp_20s_4.pcap,server_udp_20s_5.pcap,server_udp_20s_6.pcap
fi