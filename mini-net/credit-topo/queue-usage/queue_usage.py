import re
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import logging
import os
import argparse
import numpy as np
import re
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from utils import ( extract_qdepth_from_log,plot_qdepth_from_log, # METHOD 1
                   extract_queue_depths,plot_queue_usage_for_competing_flows, # METHOD 2
                   move_file_content,
                    )
# set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)





# SET MAIN FUNCTION
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot queue consumption behavior.')
    parser.add_argument('--egress_bottleneck', type=str, default='100Mbits', help='Bottleneck link bandwidth.')
    parser.add_argument('--full_queue_depth', type=str, default='DEFAULT', help='Queue depth.')
    parser.add_argument('--queue_depth_limit', type=str, default='NONE', help='Queue depth limit.')
    parser.add_argument('--flow_type', type=str, default='iperf_UDP', help='Flow type.')
    parser.add_argument('--egress_queue_rate', type=str, default='DEFAULT', help='Queue rate.')
    parser.add_argument('--task', type=str, default='Basic_Forwarding', help='Task name.')
    parser.add_argument('--weight_rate', type=str, default='NONE', help='Weight rate.')
    parser.add_argument('--downsample_rate', type=int, default=10, help='Downsample rate.')
    parser.add_argument('--experiment', type=int, default=0, help='Experiment number.')
    parser.add_argument('--folder_path', type=str, default='./plots/', help='Folder path.')
    parser.add_argument('--cloning_delay', type=str, default='NONE', help='Cloning delay.')
    args = parser.parse_args()



    # MOVE log_file = '../logs/p4s.s2.log'
    log_file = '../logs/p4s.s2.log'
    src_path = log_file
    log_file_name= f'exp{args.experiment}_task:{args.task}-bottleneck:{args.egress_bottleneck}-queue_depth:{args.full_queue_depth}-queue_depth_limit:{args.queue_depth_limit}-flow_type:{args.flow_type}-queue_rate:{args.egress_queue_rate}-weight_rate:{args.weight_rate}--cloning_delay:{args.cloning_delay}'
    dest_path = f'./logs/{args.folder_path}{log_file_name}.log'
    

    # EXTRACT QDEPTH VALUES FROM LOG FILE
    #Check if the log file exists
    process_file = src_path
    # logger.info(f'Processing file: {process_file}')

    if not os.path.exists(process_file):
        rasing_error_message = f'Log file {process_file} does not exist.'
        raise ValueError(rasing_error_message)
    
    
    plot_path =  f'./plots/{args.folder_path}'
    
    # MOVE log_file
    move_file_content(src_path, dest_path)
   

    # METHOD 2
    plot_name = f'METHOD2_exp{args.experiment}_task:{args.task}-bottleneck:{args.egress_bottleneck}-queue_depth:{args.full_queue_depth}-queue_depth_limit:{args.queue_depth_limit}-flow_type:{args.flow_type}-queue_rate:{args.egress_queue_rate}-downsample_rate:{args.downsample_rate}-weight_rate:{args.weight_rate}-cloning_delay:{args.cloning_delay}'
    qdepth_values_per_flow = extract_queue_depths(process_file)
    plot_queue_usage_for_competing_flows(args,qdepth_values_per_flow, 
                            plot_name=plot_name,
                            path=plot_path,
                           downsample_rate=args.downsample_rate,
                           )
    















    ############################################################
    
    #  # METHOD 1
    # plot_name = f'METHOD1_exp{args.experiment}_task:{args.task}-bottleneck:{args.egress_bottleneck}-queue_depth:{args.full_queue_depth}-queue_depth_limit:{args.queue_depth_limit}-flow_type:{args.flow_type}-queue_rate:{args.egress_queue_rate}-downsample_rate:{args.downsample_rate}-weight_rate:{args.weight_rate}-cloning_delay:{args.cloning_delay}'
    # qdepth_values_per_flow_dict = extract_qdepth_from_log(process_file)
    # plot_qdepth_from_log(args,qdepth_values_per_flow_dict, 
    #                         plot_name=plot_name,
    #                         path=plot_path,
    #                        downsample_rate=args.downsample_rate,
    #                        )
    






