#!/bin/bash
echo "processing pcap files ........"

# Method 1:
# calculate packet loss as retransmissions (packet loss rate = retransmissions / total packets)


# Basic-Forwarding
# FULL BANDWIDTH (NO queueing)
# python3 pcap_reader.py --sender ./client_pcaps_basic/client_rtt60s_tcp20s_fullbandwidth_1.pcap,./client_pcaps_basic/client_rtt60s_tcp20s_fullbandwidth_2.pcap,./client_pcaps_basic/client_rtt60s_tcp20s_fullbandwidth_3.pcap,./client_pcaps_basic/client_rtt60s_tcp20s_fullbandwidth_4.pcap
# CLIENT 1 with queueing
# python3 pcap_reader.py --sender ./client_pcaps_basic/client1_rtt60s_tcp20s_qrate10_qdepth100_1.pcap,./client_pcaps_basic/client1_rtt60s_tcp20s_qrate10_qdepth100_2.pcap,./client_pcaps_basic/client1_rtt60s_tcp20s_qrate10_qdepth100_3.pcap,./client_pcaps_basic/client1_rtt60s_tcp20s_qrate10_qdepth100_4.pcap,./client_pcaps_basic/client1_rtt60s_tcp20s_qrate10_qdepth100_5.pcap
# SWITCH 1 with queueing
# python3 pcap_reader.py --sender ./client_pcaps_basic/switch1_rtt60s_tcp20s_qrate10_qdepth100_1.pcap,./client_pcaps_basic/switch1_rtt60s_tcp20s_qrate10_qdepth100_2.pcap,./client_pcaps_basic/switch1_rtt60s_tcp20s_qrate10_qdepth100_3.pcap,./client_pcaps_basic/switch1_rtt60s_tcp20s_qrate10_qdepth100_4.pcap,./client_pcaps_basic/switch1_rtt60s_tcp20s_qrate10_qdepth100_5.pcap


# CREDIT-Forwarding

# CLIENT1
python3 pcap_reader.py --sender ./client_pcaps_credits/client1_rtt60s_tcp20s_qrate10_qdepth100_credits_1.pcap,./client_pcaps_credits/client1_rtt60s_tcp20s_qrate10_qdepth100_credits_2.pcap,./client_pcaps_credits/client1_rtt60s_tcp20s_qrate10_qdepth100_credits_3.pcap,./client_pcaps_credits/client1_rtt60s_tcp20s_qrate10_qdepth100_credits_4.pcap,./client_pcaps_credits/client1_rtt60s_tcp20s_qrate10_qdepth100_credits_5.pcap

# SWITCH 1
python3 pcap_reader.py --sender ./client_pcaps_credits/switch1_rtt60s_tcp20s_qrate10_qdepth100_credits_1.pcap,./client_pcaps_credits/switch1_rtt60s_tcp20s_qrate10_qdepth100_credits_2.pcap,./client_pcaps_credits/switch1_rtt60s_tcp20s_qrate10_qdepth100_credits_3.pcap,./client_pcaps_credits/switch1_rtt60s_tcp20s_qrate10_qdepth100_credits_4.pcap,./client_pcaps_credits/switch1_rtt60s_tcp20s_qrate10_qdepth100_credits_5.pcap

# CLIENT 3 
python3 pcap_reader.py --sender ./client_pcaps_credits/client3_rtt60s_tcp20s_qrate10_qdepth100_credits_1.pcap,./client_pcaps_credits/client3_rtt60s_tcp20s_qrate10_qdepth100_credits_2.pcap,./client_pcaps_credits/client3_rtt60s_tcp20s_qrate10_qdepth100_credits_3.pcap,./client_pcaps_credits/client3_rtt60s_tcp20s_qrate10_qdepth100_credits_4.pcap,./client_pcaps_credits/client3_rtt60s_tcp20s_qrate10_qdepth100_credits_5.pcap


# Method 2:
# calculate difference in packets between sender and receiver
# python raw_pcap_reader.py --sender ./pcaps/client_rtt60s_tcp20s_1.pcap,./pcaps/client_rtt60s_tcp20s_2.pcap,./pcaps/client_rtt60s_tcp20s_3.pcap,./pcaps/client_rtt60s_tcp20s_4.pcap \
#                           --server ./pcaps/server_rtt60s_tcp20s_1.pcap,./pcaps/server_rtt60s_tcp20s_2.pcap,./pcaps/server_rtt60s_tcp20s_3.pcap,./pcaps/server_rtt60s_tcp20s_4.pcap \