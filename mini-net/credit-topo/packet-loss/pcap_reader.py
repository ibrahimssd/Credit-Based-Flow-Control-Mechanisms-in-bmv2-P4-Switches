 
import tkinter
import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scapy.utils import RawPcapReader , PcapReader
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP
import argparse
import os
import sys
from datetime import datetime
from itertools import groupby
import logging
# set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
 
def process_pcaps(ingress_pcap_file,egress_pcap_file=None):
    aggr_dict = {}
    ROWS = 256
    COLUMNS = 256
    sport_grid = []
    sys.stdout.flush()
    proto_dict = {17:'UDP', 6:'TCP'}
    ip_dports = {}
    packet_loss_count = 0
    num_sender_packets= 0
    
        
    start_time = None
    end_time = None
    for row in range(ROWS):
        sport_grid.append([])
        for column in range(COLUMNS):
            sport_grid[row].append(0)

    dport_grid = []
    for row in range(ROWS):
        dport_grid.append([])
        for column in range(COLUMNS):
            dport_grid[row].append(0)
    
    # execute only if there are two arguments(server files exist)
    if egress_pcap_file is not None:
        logger.info(f'Reading egress pcap files {egress_pcap_file}.....')

        
        # Read the egress pcap file
        egr_sequence =[]
        with PcapReader(egress_pcap_file) as egress_packets:            
                for packet in egress_packets:
                    try:  
                        proto_name = proto_dict[packet.proto]
                        l3 = packet['IP']
                        l4 = packet[proto_name] 
                        
                        # print(packet.seq, packet.id)
                        if packet.proto != 6:
                            continue
                        #Filter source and destination
                        if not ((l3.src=='160.16.11.100' and l3.dst=='160.16.31.100') or (l3.src=='160.16.12.100' and l3.dst=='160.16.31.100')) :
                            continue        
                        egr_sequence.append(packet.seq)
                        
                    except:
                        pass  
                egr_sequence = set(egr_sequence)
        
    
    logger.info(f'Reading ingress pcap files {ingress_pcap_file}.....')
    ingress_sequences = []
    unique_ing_sequence = set()    
    with PcapReader(ingress_pcap_file) as ingress_packets:
        for packet in ingress_packets:
                try:
                    proto_name = proto_dict[packet.proto]
                    l3 = packet['IP']
                    l4 = packet[proto_name]                     
                    # # Ignore non-TCP packet
                    if packet.proto != 6:
                            logger.info(f'Not TCP packet')
                            continue  
                    if not ((l3.src=='160.16.11.100' and l3.dst=='160.16.31.100') or (l3.src=='160.16.12.100' and l3.dst=='160.16.31.100')) :
                            logger.info(f'following ips are not in the flow {l3.src} {l3.dst}')
                            continue      
                    #add all sent packets        
                    num_sender_packets+=1 
                    ingress_sequences.append(packet.seq)
                    # count retransmissions 
                    if packet.seq in unique_ing_sequence:
                        packet_loss_count+=1
                    else :                        
                        unique_ing_sequence.add(packet.seq)                                                                          
                except:
                    # packet failed to parse, skipping
                    pass
    
    # calculate retranmited packets
    # Use a dictionary to count the occurrences of each number
    counts = {}
    for seq in ingress_sequences:
        if seq in counts:
            counts[seq] += 1
        else:
            counts[seq] = 1

    # Initialize variables to store the total count and sum of redundancies
    redundancy_count = 0
    redundancy_sum = 0

    # Iterate through the dictionary to find redundancies
    for seq, count in counts.items():
        if count > 1:
            redundancy_count += count - 1
            redundancy_sum += seq * (count - 1)

    logger.info(f'Sum of redundancies: {redundancy_sum}')
    logger.info(f'number of packets sent: {num_sender_packets}')
    logger.info(f'Count of redundancies: {redundancy_count}')
    logger.info(f'packet loss count: {packet_loss_count}')
    logger.info(f'number of packets sent: {num_sender_packets}')
    logger.info(f'length of ingress sequence: {len(ingress_sequences)}')
    logger.info(f'length of unique ingress sequence: {len(unique_ing_sequence)}')
    logger.info(f'item sum : {sum(counts.values())}')
    print("done")

    return packet_loss_count,num_sender_packets,len(unique_ing_sequence)

def box_plot(lost_packets , packets_sent, file_name):  
    #get curren time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    # lost_packets = list(np.subtract(np.array(sender_packets),np.array(server_packets)))#sender_packets-server_packets
    relative_packet_loss = [(i*100)/ j for i, j in zip(lost_packets, packets_sent)]    
    logger.info(f'relative packet loss for each experiment: {relative_packet_loss}')
    avergae_packet_loss = sum(relative_packet_loss)/len(relative_packet_loss)
    logger.info(f'average packet loss: {avergae_packet_loss}')
    # print avegare packet loss in % in the plot
    logger.info(f'average packet loss in %: {avergae_packet_loss}')
    fig = plt.figure(figsize =(10, 7))
    fig.suptitle(file_name, fontsize=14, fontweight='bold')
    # plt.xticks([1],["25s tcp iperf"], rotation='vertical')
    plt.xlabel("Iperf_TCP")
    plt.ylabel("Loss Rate % ")
    # show average packet loss in in the plot
    plt.text(1.1, 0.5, "average packet loss in %: {:.2f}%".format(avergae_packet_loss), fontsize=12)
    plt.legend()
    # Creating plot
    boxes=plt.boxplot(relative_packet_loss,patch_artist=True)
    # change outline color
    for box in boxes['boxes']:
      # change outline color
      box.set(color='brown', linewidth=2)
      # change fill color
      box.set(facecolor = 'lightblue')
      # change hatch
      box.set(hatch = '/')
    # show legend
    plt.legend()
    # show average packet loss in in the plot
    plt.text(1.1, 0.5, "average packet loss in %: {:.2f}%".format(avergae_packet_loss), fontsize=12)
    # show plot
    file_path = f'./plots/{file_name}_.png'
    plt.savefig(file_path)
    # plt.show()


def calculate_packet_loss(ingress_pcap_files,egress_pcap_files):
     packet_loss_count=[]
     total_packets=[]
     un_sent_packets = []
     for file_index in range(len(ingress_pcap_files)):
         
         if len(egress_pcap_files)==0:
             
            loss_counter, num_sender_packets,num_unique_sender_packets= process_pcaps(ingress_pcap_files[file_index])
         else:
            loss_counter, num_sender_packets,num_unique_sender_packets= process_pcaps(ingress_pcap_files[file_index], egress_pcap_files[file_index])
         
         packet_loss_count.append(loss_counter)
         total_packets.append(num_sender_packets)
         un_sent_packets.append(num_unique_sender_packets)
         
     return packet_loss_count , total_packets , un_sent_packets 



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PCAP reader')
    parser.add_argument('--sender', metavar='<pcap file name>', type=str,
                        help='pcap file to parse', required=True)
    
    parser.add_argument('--server', metavar='<pcap file name>', type=str,
                        help='pcap file to parse', required=False)
    
    args = parser.parse_args()    
    sender_pcap_files = [str(item) for item in args.sender.split(',')]
    
    # check if server pcap files are provided
    if args.server is not None:
            server_pcap_files = [str(item) for item in args.server.split(',')]
            files= sender_pcap_files+server_pcap_files
            
    else :
            files= sender_pcap_files
            server_pcap_files=[]          
    for file in files:
            if not os.path.isfile(file):
                print('"{}" does not exist'.format(file), file=sys.stderr)
                sys.exit(-1)
    
    
    lost_packets , total_packets, unique_sender_packets= calculate_packet_loss(sender_pcap_files , server_pcap_files)
    
    logger.info(f'lost packets in each experiment: {lost_packets}')
    logger.info(f'total packets sent in each experiment: {total_packets}')
    logger.info(f'unique packets sent in each experiment: {unique_sender_packets}')
    
    #visualize packet loss
    file_name= sender_pcap_files[0].split('/')[-1]
    file_name=file_name[:-6]
    logger.info(f'file name: {file_name}')
    box_plot(lost_packets , total_packets, file_name)
    sys.exit(0)
    
    