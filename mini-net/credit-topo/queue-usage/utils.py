
import re
import numpy as np
import matplotlib.pyplot as plt
import logging
import os
import argparse
from datetime import datetime, timedelta
import shutil
# set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


########### METHOD 1 #############


def extract_qdepth_from_log(log_file):

    #  a0100b64 : 160.16.11.100  --> src
    #  a0100c64: 160.16.12.100  --> src
    #  a0101f64: 160.16.31.100  --> dst
    # 1 : ICMP (Internet Control Message Protocol)
    # 11 : UDP (User Datagram Protocol)
    # 6 : TCP (Transmission Control Protocol)

    host_ips = {'h1': '160.16.11.100', 'h2': '160.16.31.100', 'h3': '160.16.12.100'}
    src_ips = [host_ips['h1'], host_ips['h3']]
    dst_ips = [host_ips['h2']]
    udp = 11


    logger.info(f' PROCESSING APPROACH 1:')
    # global_timestamp_pattern = r'\*\s+standard_metadata\.egress_global_timestamp:\s+([0-9a-fA-F]+)'
    queue_usage_pattern = r'\*\s+standard_metadata\.deq_qdepth\s{5,}:\s+(\d+)'
    flow_id_pattern = r'\*\s+meta\.flowID\s{5,}:\s+(\d+)'
    protocol_pattern = r'\*\s+hdr\.ipv4\.protocol\s{5,}:\s+(\d+)'
    src_ip_pattern =   r'\*\s+hdr\.ipv4\.srcAddr\s{5,}:\s+([0-9a-fA-F]+)'
    dst_ip_pattern =   r'\*\s+hdr\.ipv4\.dstAddr\s{5,}:\s+([0-9a-fA-F]+)'
    
    # Initialize an empty list to store the extracted values
    qdepth_values = []
    flow_ids = []
    with open(log_file, 'r') as file:
        for line in file:
            flow_id_match = re.search(flow_id_pattern, line)
            queu_usage_match = re.search(queue_usage_pattern, line)
            protocol_match = re.search(protocol_pattern, line)
            src_ip_match = re.search(src_ip_pattern, line)
            dst_ip_match = re.search(dst_ip_pattern, line)
            
            if flow_id_match:
                   # Extract the value as an integer
                    flow_id = int(flow_id_match.group(1))
                    # print("Flow ID:", flow_id)
                    flow_ids.append(flow_id) 
            elif queu_usage_match:
                    # Extract the value as an integer
                    deq_qdepth = int(queu_usage_match.group(1))
                    # print("Dequeue Queue Depth:", deq_qdepth)
                    qdepth_values.append(deq_qdepth)
            else:
                # logger.info(f'NO MATCH: {line}')
                continue

    logger.info(f'qdepth_values length before removing zero flow ids : {len(qdepth_values)}')
    logger.info(f'flow_ids length before removing zero flow ids : {len(flow_ids)}')
    # keep qdepth values for non-zero flow ids
    qdepth_values = [qdepth_values[i] for i in range(len(qdepth_values)) if flow_ids[i] != 0]
    flow_ids = [flow_ids[i] for i in range(len(flow_ids)) if flow_ids[i] != 0]
    logger.info(f'qdepth_values length after removing zero flow ids : {len(qdepth_values)}')
    logger.info(f'flow_ids length after removing zero flow ids : {len(flow_ids)}')

    # RAISE ERROR IF FLOW IDS has values of 0 
    if 0 in flow_ids:
        rasing_error_message = 'Flow IDs should not have values of 0. Check if the log file contains the correct flow ids.'
        raise ValueError(rasing_error_message)
    
    # separate qdepth values for each flow id
    unique_flow_ids = list(set(flow_ids))
    logger.info(f'length of flow_ids: {len(flow_ids)}')
    qdepth_values_per_flow = []
    for flow_id in unique_flow_ids:
        qdepth_values_per_flow.append([qdepth_values[i] for i in range(len(qdepth_values)) if flow_ids[i] == flow_id])
    

    logger.info(f'length of unique flow_ids: {len(unique_flow_ids)}')
    # logg length of each flow queue depth
    for i in range(len(qdepth_values_per_flow)):
        logger.info(f'flow_id: {unique_flow_ids[i]} has {len(qdepth_values_per_flow[i])} queue depths, max queue depth: {max(qdepth_values_per_flow[i])}')
    
    # return as dictionary
    qdepth_values_per_flow_dict = {}
    for i in range(len(unique_flow_ids)):
        qdepth_values_per_flow_dict[unique_flow_ids[i]] = qdepth_values_per_flow[i]
    
    if qdepth_values_per_flow_dict == {}:
        rasing_error_message = 'qdepth_values_per_flow_dict is empty. Check if the log file contains the correct flow ids.'
        raise ValueError(rasing_error_message)
    
    return qdepth_values_per_flow_dict



def plot_qdepth_from_log(args, qdepth_values_per_flow, plot_name , path, downsample_rate=10):
    """
    Plots the queue consumption behavior for multiple flows.

    Args:
        qdepth_values_per_flow (dict): Dictionary where keys are flow IDs and values are lists of queue depth values.
        ... other arguments ...
        downsample_rate (int): The rate at which data should be downsampled. Default is 10.
    """
    max_length = max(len(qdepth_values) for qdepth_values in qdepth_values_per_flow.values())
    time_series = range(0, max_length, downsample_rate)
    
    plt.figure(figsize=(15, 8))  # Increase the figure size
    
    colors = ['blue', 'red', 'green', 'purple', 'orange']
    line_styles = ['-', '--', '-.', ':']  # Add more line styles for differentiation

    for flow_id, qdepth_values in qdepth_values_per_flow.items():
        if len(qdepth_values) < max_length:
            placeholder_value = 0
            qdepth_values = np.pad(qdepth_values, (0, max_length - len(qdepth_values)), 'constant', constant_values=placeholder_value)
        
        # Downsample the data points for better visibility
        downsampled_qdepth_values = qdepth_values[::downsample_rate]

        plt.plot(time_series, downsampled_qdepth_values, label=f'Flow {flow_id}', color=colors[flow_id % len(colors)], linestyle=line_styles[flow_id % len(line_styles)], linewidth=2.5)  # Increase linewidth
    
    # anotate queu capacity 
    queue_capacity = int(args.full_queue_depth.split('packets')[0])
    # plt.axhline(y=queue_capacity, color='r', linestyle='--', linewidth=2)

    # add avergae usage line for each flow
    for flow_id, qdepth_values in qdepth_values_per_flow.items():
        avg_qdepth = np.mean(qdepth_values)
        plt.axhline(y=avg_qdepth, color=colors[flow_id % len(colors)], linestyle=':', linewidth=2)
    

    flow1 ='h1-h2'
    flow2 ='h3-h2'
    plt.xlabel('Time (seconds)')
    plt.ylabel('Queue usage (packets)')
    plt.title(f'Queue usage behavior for flows \n flow 1 :{flow1} and flow 2 : {flow2}')
    plt.legend(loc='upper right')
    plt.grid(True)
    plot_name = f'{plot_name}.png'
    plt.savefig(path + plot_name)
    plt.close()

############################################################################################################################################################################
####################################################################### METHOD 2 #############################################################################################################
############################################################################################################################################################################


# map hex to ip
def hex_to_ip(hex):
    ip = ''
    for i in range(0, len(hex), 2):
        ip += str(int(hex[i:i+2], 16)) + '.'
    return ip[:-1]
            

def extract_queue_depths(log_file):
    #  a0100b64 : 160.16.11.100  --> src
    #  a0100c64: 160.16.12.100  --> src
    #  a0101f64: 160.16.31.100  --> dst
    # 1 : ICMP (Internet Control Message Protocol)
    # 11 : UDP (User Datagram Protocol)
    # 6 : TCP (Transmission Control Protocol)

    host_ips = {'h1': '160.16.11.100', 'h2': '160.16.31.100', 'h3': '160.16.12.100'}
    src_ips = [host_ips['h1'], host_ips['h3']]
    dst_ips = [host_ips['h2']]
    udp = 11

    hex_ip_dict = {'a0100b64': '160.16.11.100', 'a0100c64': '160.16.12.100', 
                'a0101f64': '160.16.31.100'}


    logger.info(f' PROCESSING APPROACH 2:')
    global_timestamp_pattern = r'\*\s+standard_metadata\.egress_global_timestamp:\s+([0-9a-fA-F]+)'
    queue_usage_pattern = r'\*\s+standard_metadata\.deq_qdepth\s{5,}:\s+(\d+)'
    flow_id_pattern = r'\*\s+meta\.flowID\s{5,}:\s+(\d+)'
    protocol_pattern = r'\*\s+hdr\.ipv4\.protocol\s{5,}:\s+(\d+)'
    src_ip_pattern =   r'\*\s+hdr\.ipv4\.srcAddr\s{5,}:\s+([0-9a-fA-F]+)'
    dst_ip_pattern =   r'\*\s+hdr\.ipv4\.dstAddr\s{5,}:\s+([0-9a-fA-F]+)'
   
    
    # Initialize a dictionary to hold the queue depth data for each flow
    queue_depth_data = {}

    # Open the log file and process each line
    with open(log_file, 'r') as file:
        base_time = None  # We will set the first timestamp as the base time
        
        time_stamps = []
        qdepths = []
        flow_ids = []

        flow_protocol = []
        flow_src_ip = []
        flow_dst_ip = []
        
        for line in file:
            # logging.info(f'Processing line: {line.strip()}')
            timestamp_match = re.search(global_timestamp_pattern,line)
            qdepth_match = re.search(queue_usage_pattern, line)
            flow_id_match = re.search(flow_id_pattern, line)
            protocol_match = re.search(protocol_pattern, line)
            src_ip_match = re.search(src_ip_pattern, line)
            dst_ip_match = re.search(dst_ip_pattern, line)

            if timestamp_match :
                hex_timestamp = timestamp_match.group(1)
                timestamp_value = int(hex_timestamp, 16)
                # Assume that the first timestamp corresponds to the start of the logging
                if base_time is None:
                    base_time = timestamp_value
                # Calculate the time delta in microseconds (assuming the counter is in microseconds)
                time_delta = timestamp_value - base_time  # This will be in the unit of the timestamp
                time_delta = time_delta / 1000000  # Convert to seconds
                time_stamps.append(time_delta)
                
            # Extract the flow ID and queue depth from the log line
            if qdepth_match:
                qdepth = int(qdepth_match.group(1))
                qdepths.append(qdepth)

            if flow_id_match:
                flow_id = int(flow_id_match.group(1))
                flow_ids.append(flow_id)
                # If the flow ID is not yet in the dictionary, initialize an empty list
                if flow_id not in queue_depth_data:
                    queue_depth_data[flow_id] = []
            
            ######################################################################################################################
            if protocol_match:
                protocol = int(protocol_match.group(1))
                flow_protocol.append(protocol)
            

            if src_ip_match:
                src_ip = src_ip_match.group(1)
                flow_src_ip.append(hex_to_ip(src_ip))
            
            
            if dst_ip_match:
                dst_ip = dst_ip_match.group(1)
                flow_dst_ip.append(hex_to_ip(dst_ip))
    
    
    ###################################################################################################
    combined_data = list(zip(flow_protocol, flow_src_ip, flow_dst_ip, flow_ids, time_stamps, qdepths))
    logger.info(f'length of combined_data: {len(combined_data)}')
    
    # item 0 : protocol
    # item 1 : src_ip
    # item 2 : dst_ip
    # item 3 : flow_id
    # item 4 : timestamp
    # item 5 : qdepth


    # Filter for UDP, non-zero flow IDs, and packets involving host IPs
    filtered_data = [
        item for item in combined_data

        # if item[0] == udp and item[3] != 0 and item[1] in host_ips.values() and item[2] in host_ips.values()

        # source should be h1 or h3 and destination should be h2 (return udp packets with flow ids not equal to 0 and source ip is h1 or h3 and destination ip is h2)
        if item[0] == udp and item[3] != 0 and item[1] in src_ips and item[2] in dst_ips
    ]
    
    # length of lists of filtered data 
    logger.info(f'length of filtered_data: {len(filtered_data)}')
    for i in range(50):
        logger.info(f'item {i} : protocol, src_ip, dst_ip, flow_id, timestamp, qdepth: {filtered_data[i]}')


    # Initialize or clear the dictionary to hold the queue depth data for each flow
    queue_depth_data = {}

    # Process the filtered data
    for protocol, src_ip, dst_ip, flow_id, timestamp, qdepth in filtered_data:
        if flow_id not in queue_depth_data:
            queue_depth_data[flow_id] = []
        queue_depth_data[flow_id].append((timestamp, qdepth))

    # Sort the queue depth data for each flow based on timestamps
    for flow_id in queue_depth_data:
        queue_depth_data[flow_id] = sorted(queue_depth_data[flow_id], key=lambda x: x[0])
        logger.info(f'flow_id: {flow_id} has {len(queue_depth_data[flow_id])} queue depths, max queue depth (time_stamp , depth): {max(queue_depth_data[flow_id], key=lambda x: x[1])}')


    ##########################  LOGS  ##########################################################################
    
    

    # logg length of the lists 
    logger.info(f'length of time_stamps: {len(time_stamps)}')
    logger.info(f'length of qdepths: {len(qdepths)}')
    logger.info(f'length of flow_ids: {len(flow_ids)}')
    logger.info(f'length of flow_protocol: {len(flow_protocol)}')
    logger.info(f'length of flow_src_ip: {len(flow_src_ip)}')
    logger.info(f'length of flow_dst_ip: {len(flow_dst_ip)}')
    logger.info(f'unique flow_ids: {list(set(flow_ids))}')
    logger.info(f'unique flow_protocol: {list(set(flow_protocol))}')
    logger.info(f'unique flow_src_ip: {list(set(flow_src_ip))}')
    logger.info(f'unique flow_dst_ip: {list(set(flow_dst_ip))}')

    
    
    
    

    

    return queue_depth_data





##########################################################################################################################################################
def plot_queue_usage_for_competing_flows(args, qdepth_values_per_flow, plot_name, path, downsample_rate=50):
    fig, ax = plt.subplots(figsize=(15, 8))  # Set the figure size for better visibility in papers

    queue_capacity = int(args.full_queue_depth.split('packets')[0])

    # Enhanced color palette for better distinction in printed and on-screen formats
    flow_colors = {1: "#2ca02c", 2: "#ff7f0e"}  # Example: using hex color codes for precision

    for flow_id in [1, 2]:  # Assuming two competing flows
        if flow_id in qdepth_values_per_flow:
            timestamps, qdepths = zip(*qdepth_values_per_flow[flow_id])  # Extract data

            # Downsample the data to make the plot less cluttered
            if downsample_rate > 1:
                timestamps = timestamps[::downsample_rate]
                qdepths = qdepths[::downsample_rate]

            # Plot each flow with specific settings
            ax.plot(timestamps, qdepths, label=f'Flow {flow_id}', color=flow_colors[flow_id], linewidth=3, marker='o', markersize=5)

            # Calculate average and maximum queue depth for annotations
            avg_qdepth = np.mean(qdepths)
            max_qdepth = np.max(qdepths)

            # Add a horizontal line indicating the average queue depth
            ax.axhline(y=avg_qdepth, color=flow_colors[flow_id], linestyle='--', linewidth=1.5, label=f'Avg Flow {flow_id}')

    # Styling the plot with clear labels and titles
    ax.set_xlabel('Time (seconds)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Egress Switch Queue Usage (#packets)', fontsize=14, fontweight='bold')
    ax.set_title('Egress Switch Queue Usage for Competing Flows', fontsize=16, fontweight='bold')
    ax.legend(fontsize=12, loc='upper right')
    ax.grid(True, linestyle='--')

    # # Adding a line for the queue capacity, if necessary
    # if queue_capacity:
    #     ax.axhline(y=queue_capacity, color='red', linestyle='-.', linewidth=2, label='Queue Capacity')
    #     ax.annotate(f'Capacity: {queue_capacity} packets', xy=(0.5, queue_capacity), xycoords=('axes fraction', 'data'),
    #                 textcoords="offset points", xytext=(0,10), ha='center', fontsize=12, color='red')

    # Save the plot with an appropriate bounding box to include all annotations
    plt.tight_layout()
    final_plot_path = f'{path}/{plot_name}.png'
    plt.savefig(final_plot_path, bbox_inches='tight')
    plt.close()

    print(f"Plot saved as {final_plot_path}")


##############################################################################################################

def move_file_content(src_path, dest_path):
    # Verify source file exists
    if not os.path.exists(src_path):
        raise ValueError(f'Log file {src_path} does not exist.')

    # Perform the move operation
    try:
        # If destination exists and content differs, or doesn't exist, write the content.
        if not os.path.exists(dest_path) or os.path.getsize(src_path) != os.path.getsize(dest_path):
            shutil.copyfile(src_path, dest_path)
            logger.info(f'Content from source has been successfully moved to destination.')
        else:
            logger.info(f'File already exists with identical content. Skipping move operation.')
    except Exception as e:
        logger.error(f'Failed to move content from {src_path} to {dest_path}: {e}')

