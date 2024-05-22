# Import libraries

import matplotlib.pyplot as plt
import numpy as np
from scapy.utils import RawPcapReader
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP
import argparse
import os
import sys
from datetime import datetime


sender_packets =[]
server_packets=[]

def process_pcap(files_name, packets):
    
    for file_name in files_name:
    
            print('Opening {}...'.format(file_name))
            
            client_ip='172.16.11.100'
            server_ip='172.16.31.100'
            count = 0
            interesting_packet_count=0
            
            for (pkt_data, pkt_metadata,) in RawPcapReader(file_name):
                count += 1
                
                ether_pkt = Ether(pkt_data)
                # print(ether_pkt[IP])
                ip_pkt = ether_pkt[TCP]
                
                
                if ip_pkt.proto != 6:
                 # Ignore non-TCP packet
                   continue
               
                # if (ip_pkt.src != client_ip):
                #   # Uninteresting source IP address
                #    continue
        
                # if (ip_pkt.dst != server_ip):
                #    # Uninteresting destination IP address
                #    continue
            
                interesting_packet_count+=1
                
            packets.append(interesting_packet_count)
            print('{} contains {} packets  and {} tcp packets'.format(file_name, count, interesting_packet_count))
            return packets
            
def box_plot(sender_packets, server_packets):
    
    #get curren time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    

    lost_packets = list(np.subtract(np.array(sender_packets),np.array(server_packets)))#sender_packets-server_packets
    
    relative_packet_loss = [i / j for i, j in zip(lost_packets, sender_packets)]

    
    fig = plt.figure(figsize =(10, 7))
    fig.suptitle('udp iperf test for 20 seconds ', fontsize=14, fontweight='bold')
    plt.xticks([1],['20 seconds'])
    # Creating plot
    boxes=plt.boxplot(relative_packet_loss,patch_artist=True)
    
    
    for box in boxes['boxes']:
      # change outline color
      box.set(color='brown', linewidth=2)
      # change fill color
      box.set(facecolor = 'lightblue')
      # change hatch
      box.set(hatch = '/')

    
    # show plot
    plt.savefig('packet_loss_plots/udp_20s_'+str(current_time)+'.png')
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PCAP reader')
    parser.add_argument('--sender', metavar='<pcap file name>', type=str,
                        help='pcap file to parse', required=True)
    
    parser.add_argument('--server', metavar='<pcap file name>', type=str,
                        help='pcap file to parse', required=True)
    
    args = parser.parse_args()
    
    sender_files = [str(item) for item in args.sender.split(',')]
    server_files = [str(item) for item in args.server.split(',')]
    
    files= sender_files+server_files
    for file in files:
            if not os.path.isfile(file):
                print('"{}" does not exist'.format(file), file=sys.stderr)
                sys.exit(-1)
    
    # counting packets
    print(sender_packets)
    sender_packets = process_pcap(sender_files, sender_packets)
    print(sender_packets)
    server_packets = process_pcap(server_files,server_packets)
    
    #visualize packet loss
    box_plot(sender_packets,server_packets)
    sys.exit(0)
    
    


