# protocol_src_dst = list(zip(flow_protocol, flow_src_ip, flow_dst_ip))
#     # length before processing 
#     logger.info(f'length of protocol_src_dst before processing: {len(protocol_src_dst)}')
#     # filter out non udp list members
#     udp_protocol_src_dst = [protocol_src_dst[i] for i in range(len(protocol_src_dst)) if protocol_src_dst[i][0] == udp]  
    
#     # filter out non host ips
#     host_protocol_src_dst = [udp_protocol_src_dst[i] for i in range(len(udp_protocol_src_dst)) if udp_protocol_src_dst[i][1] in host_ips.values() and udp_protocol_src_dst[i][2] in host_ips.values()]
#     logger.info(f'length of host_protocol_src_dst (only udp and host ips): {len(host_protocol_src_dst)}')
    
#     # add time stamps and qdepths to the dictionary for non zero flow ids
#     for i in range(len(flow_ids)):
#         queue_depth_data[flow_ids[i]].append((time_stamps[i], qdepths[i]))
    
#     # sort the queue depth data for each flow based on time stamps
#     for flow_id,  qdepths_list in queue_depth_data.items():
#         queue_depth_data[flow_id] = sorted(qdepths_list, key=lambda x: x[0])
#     logger.info(f'number of flows: {len(queue_depth_data)}')
#     # logg flows queue depth length and time stamps length for each flow
#     for flow_id,  qdepths_list in queue_depth_data.items():
#         logger.info(f'flow_id: {flow_id} has {len(qdepths_list)} queue depths and {len(qdepths_list)} time stamps, max queue depth: {max(qdepths_list, key=lambda x: x[1])}')



# def move_file_content(src_path, dest_path):

#     if not os.path.exists(src_path):
#         rasing_error_message = f'Log file {src_path} does not exist.'
#         raise ValueError(rasing_error_message)
    

#     elif not os.path.exists(dest_path):
#             logger.info(f'Moving file from source path to destination path')
#             with open(src_path, 'r') as source_file:
#                 content = source_file.read()

#             with open(dest_path, 'w') as dest_file:
#                 dest_file.write(content)
            
#             logger.info(f'File moved successfully.')

#     elif os.path.exists(dest_path):
#         # Check the size of the file in the destination path and the source path
#         if os.path.getsize(src_path) != os.path.getsize(dest_path):
#             logger.info(f'File {dest_path} already exists but has different content. Overwriting the file.')
#             with open(src_path, 'r') as source_file:
#                 content = source_file.read()

#             with open(dest_path, 'w') as dest_file:
#                 dest_file.write(content)
            
#             logger.info(f'File {dest_path} moved successfully.')                


#     else:
#         logger.info(f'File {dest_path} already completed and exists. Skipping move operation.')




# def plot_queue_usage_for_competing_flows(args, qdepth_values_per_flow, plot_name, path, downsample_rate=50):
#     fig, ax = plt.subplots(figsize=(15, 8))

#     queue_capacity = int(args.full_queue_depth.split('packets')[0])

#     # Define specific colors for better readability
#     flow_colors = {1: "green", 2: "orange"}
#     # Plot only for flow IDs 1 and 2
#     for flow_id in [1, 2]:
#         if flow_id in qdepth_values_per_flow:
#             qdepth_values = qdepth_values_per_flow[flow_id]
#             time_stamps, qdepths = zip(*qdepth_values)  # Unzipping into two lists

#             # Downsample the data if necessary
#             if downsample_rate > 1:
#                 time_stamps = time_stamps[::downsample_rate]
#                 qdepths = qdepths[::downsample_rate]

#             ax.plot(time_stamps, qdepths, label=f'Flow {flow_id}', color=flow_colors[flow_id], linewidth=2.5)

#             # Calculate and annotate average and maximum queue depth
#             avg_qdepth = np.mean(qdepths)
#             max_qdepth = np.max(qdepths)
#             # ax.annotate(f'Avg: {avg_qdepth:.2f}, Max: {max_qdepth}', xy=(time_stamps[-1], qdepths[-2]),
#             #             textcoords="offset points", xytext=(-15,300), ha='center', color=flow_colors[flow_id])
#             # add avergae usage line for each flow
#             ax.axhline(y=avg_qdepth, color=flow_colors[flow_id], linestyle=':', linewidth=2)


#     # Customize the plot
#     ax.set_xlabel('Time (seconds)')
#     ax.set_ylabel('Queue Usage (packets)')
#     ax.set_title('Queue Usage Behavior for Flows 1 and 2')
#     ax.legend(loc='upper right')
#     ax.grid(True)

#     # Optionally, add a horizontal line for queue capacity
#     # ax.axhline(y=queue_capacity, color='r', linestyle='--', linewidth=2)
#     # ax.annotate(f'Egress Queue capacity: {queue_capacity} packets', xy=(0, queue_capacity), xytext=(0, queue_capacity + 5),
#     #             arrowprops=dict(facecolor='black', shrink=0.05))

#     # Save the plot
#     plot_name = f'{plot_name}.png'
#     plt.savefig(path + plot_name, bbox_inches='tight')
#     plt.close()

