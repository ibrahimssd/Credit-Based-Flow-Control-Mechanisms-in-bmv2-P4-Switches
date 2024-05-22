
# def plot_qdepth_behavior(qdepth_values_per_flow, file_name , path, downsample_rate=10):
#     """
#     Plots the queue consumption behavior for multiple flows.

#     Args:
#         qdepth_values_per_flow (dict): Dictionary where keys are flow IDs and values are lists of queue depth values.
#         ... other arguments ...
#         downsample_rate (int): The rate at which data should be downsampled. Default is 10.
#     """
#     max_length = max(len(qdepth_values) for qdepth_values in qdepth_values_per_flow.values())
#     time_series = range(0, max_length, downsample_rate)
    
#     plt.figure(figsize=(15, 8))  # Increase the figure size
    
#     colors = ['blue', 'red', 'green', 'purple', 'orange']
#     line_styles = ['-', '--', '-.', ':']  # Add more line styles for differentiation

#     for flow_id, qdepth_values in qdepth_values_per_flow.items():
#         if len(qdepth_values) < max_length:
#             placeholder_value = 0
#             qdepth_values = np.pad(qdepth_values, (0, max_length - len(qdepth_values)), 'constant', constant_values=placeholder_value)
        
#         # Downsample the data points for better visibility
#         downsampled_qdepth_values = qdepth_values[::downsample_rate]

#         plt.plot(time_series, downsampled_qdepth_values, label=f'Flow {flow_id}', color=colors[flow_id % len(colors)], linestyle=line_styles[flow_id % len(line_styles)], linewidth=2.5)  # Increase linewidth
    
#     flow1 ='h1-h2'
#     flow2 ='h3-h2'
#     plt.xlabel('Time (seconds)')
#     plt.ylabel('Queue usage (packets)')
#     plt.title(f'Queue usage behavior for flows \n flow 1 :{flow1} and flow 2 : {flow2}')
#     plt.legend(loc='upper right')
#     plt.grid(True)
#     plot_name = f'{file_name}.png'
#     plt.savefig(path + plot_name)
#     plt.close()










# def extract_qdepth_from_log(log_file):
#     queue_usage_pattern = r'\*\s+standard_metadata\.deq_qdepth\s+:\s+(\d+)'
#     flow_id_pattern = r'\*\s+meta\.flowID\s+:\s+(\d+)'
    
#     # Initialize an empty list to store the extracted values
#     qdepth_values = []
#     flow_ids = []
#     with open(log_file, 'r') as file:
#         for line in file:
#             flow_id_match = re.search(flow_id_pattern, line)
#             queu_usage_match = re.search(queue_usage_pattern, line)
#             if flow_id_match:
#                    # Extract the value as an integer
#                     flow_id = int(flow_id_match.group(1))
#                     # print("Flow ID:", flow_id)
#                     flow_ids.append(flow_id) 
#             elif queu_usage_match:
#                     # Extract the value as an integer
#                     deq_qdepth = int(queu_usage_match.group(1))
#                     # print("Dequeue Queue Depth:", deq_qdepth)
#                     qdepth_values.append(deq_qdepth)

#             else:
#                 # logger.info(f'NO MATCH: {line}')
#                 continue

#     logger.info(f'qdepth_values length before removing zero flow ids : {len(qdepth_values)}')
#     logger.info(f'flow_ids length before removing zero flow ids : {len(flow_ids)}')
#     # keep qdepth values for non-zero flow ids
#     qdepth_values = [qdepth_values[i] for i in range(len(qdepth_values)) if flow_ids[i] != 0]
#     flow_ids = [flow_ids[i] for i in range(len(flow_ids)) if flow_ids[i] != 0]
#     logger.info(f'qdepth_values length after removing zero flow ids : {len(qdepth_values)}')
#     logger.info(f'flow_ids length after removing zero flow ids : {len(flow_ids)}')

#     # RAISE ERROR IF FLOW IDS has values of 0 
#     if 0 in flow_ids:
#         rasing_error_message = 'Flow IDs should not have values of 0. Check if the log file contains the correct flow ids.'
#         raise ValueError(rasing_error_message)
    
#     # separate qdepth values for each flow id
#     unique_flow_ids = list(set(flow_ids))
#     logger.info(f'length of flow_ids: {len(flow_ids)}')
#     qdepth_values_per_flow = []
#     for flow_id in unique_flow_ids:
#         qdepth_values_per_flow.append([qdepth_values[i] for i in range(len(qdepth_values)) if flow_ids[i] == flow_id])

    
#     # return as dictionary
#     qdepth_values_per_flow_dict = {}
#     for i in range(len(unique_flow_ids)):
#         qdepth_values_per_flow_dict[unique_flow_ids[i]] = qdepth_values_per_flow[i]
    
#     if qdepth_values_per_flow_dict == {}:
#         rasing_error_message = 'qdepth_values_per_flow_dict is empty. Check if the log file contains the correct flow ids.'
#         raise ValueError(rasing_error_message)
    
#     return qdepth_values_per_flow_dict

