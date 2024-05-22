



# RTT and BA for FLOW 1
ping -w 60  h2 > ping_basic_h1_h2_qrate10_qdepth5000_RTT60.txt
iperf -c h2 -u -t 60 > iperf_basic_h1_h2_qrate10_qdepth5000.txt


# RTT and BA for FLOW 2
ping -w 60  h2 > ping_clone_h3_h2_qrate10_qdepth5000_RTT60.txt
iperf -c h2 -u -t 60 > iperf_clone_h3_h2_qrate10_qdepth5000.txt