

#!/bin/bash
####################################### BASIC FORWARDING  ############################################################

# [1] ########## TEST THE EFFECT OF FULL QUEUE DEPTH  ON THE QUEUE USAGE ##########

# Default Queu depth : 64 packets
# python queue_usage.py --egress_bottleneck '1GiB'\
#                         --flow_type 'iperf_UDP'\
#                         --full_queue_depth '64packets'\
#                         --egress_queue_rate '10packets'\
#                         --task 'basic_Forwarding_competing'\
#                         --downsample_rate 50\
#                        --folder_path 'basic_forwarding_full_queue_depth_effect/'\
#                         --experiment 1                    


# python queue_usage.py --egress_bottleneck '1GiB' \
#                         --full_queue_depth '100packets' \
#                         --flow_type 'iperf_UDP'\
#                         --egress_queue_rate '10packets'\
#                         --task 'basic_Forwarding_competing'\
#                         --downsample_rate 50\
#                        --folder_path 'basic_forwarding_full_queue_depth_effect/'\
#                         --experiment 2\


# ---------> VERFIED SETTINGS
# python queue_usage.py --egress_bottleneck '1GiB' \
#                         --full_queue_depth '10000packets' \
#                         --flow_type 'iperf_UDP' \
#                         --egress_queue_rate '10packets'\
#                         --task 'basic_Forwarding_competing'\
#                         --downsample_rate 40\
#                         --folder_path 'basic_forwarding_full_queue_depth_effect/'\
#                         --experiment 3\




# python queue_usage.py --egress_bottleneck '1GiB' \
#                         --full_queue_depth '50000packets' \
#                         --flow_type 'iperf_UDP' \
#                         --egress_queue_rate '10packets'\
#                         --task 'basic_Forwarding_competing'\
#                         --downsample_rate 50\
#                         --folder_path 'basic_forwarding_full_queue_depth_effect/'\
#                         --experiment 4\


# python queue_usage.py --egress_bottleneck '1GiB' \
#                         --full_queue_depth '2000000packets' \
#                         --flow_type 'iperf_UDP' \
#                         --egress_queue_rate '10packets'\
#                         --task 'basic_Forwarding_competing'\
#                         --downsample_rate 50\
#                         --folder_path 'basic_forwarding_full_queue_depth_effect/'\
#                         --experiment 5\




# [2] ########## TEST THE EFFECT OF QUEUE RATE ON THE QUEUE USAGE ##########
# testing queu rates : 5 10 20 70 100 
# python queue_usage.py --egress_bottleneck '1GiB' \
#                         --full_queue_depth '10000packets'\
#                         --flow_type 'iperf_UDP' \
#                         --egress_queue_rate '5packets'\
#                         --task 'basic_Forwarding_competing'\
#                         --experiment 1\
#                         --folder_path 'basic_forwarding_queue_rate_effect/'\
#                         --downsample_rate 50\


### ------> Verified settings
# python queue_usage.py --egress_bottleneck '1GiB' \
#                         --full_queue_depth '10000packets'\
#                         --flow_type 'iperf_UDP' \
#                         --egress_queue_rate '10packets'\
#                         --task 'basic_Forwarding_competing'\
#                         --experiment 2\
#                         --folder_path 'basic_forwarding_queue_rate_effect/'\
#                         --downsample_rate 50\


# python queue_usage.py --egress_bottleneck '1GiB' \
#                         --full_queue_depth '10000packets'\
#                         --flow_type 'iperf_UDP' \
#                         --egress_queue_rate '20packets'\
#                         --task 'basic_Forwarding_competing'\
#                         --experiment 3\
#                         --folder_path 'basic_forwarding_queue_rate_effect/'\
#                         --downsample_rate 50\


# python queue_usage.py --egress_bottleneck '1GiB' \
#                         --full_queue_depth '10000packets'\
#                         --flow_type 'iperf_UDP' \
#                         --egress_queue_rate '70packets'\
#                         --task 'basic_Forwarding_competing'\
#                         --experiment 4\
#                         --folder_path 'basic_forwarding_queue_rate_effect/'\
#                         --downsample_rate 50\


# python queue_usage.py --egress_bottleneck '1GiB' \
#                         --full_queue_depth '10000packets'\
#                         --flow_type 'iperf_UDP' \
#                         --egress_queue_rate '100packets'\
#                         --task 'basic_Forwarding_competing'\
#                         --experiment 5\
#                         --folder_path 'basic_forwarding_queue_rate_effect/'\
#                         --downsample_rate 50\

# *************************************************************************************************************

# 1) >>>>>>> BEST QUEUE DEPTH = 10000 packets 
# 2) >>>>>>>> BEST QUEUE RATE = 10 packets

# python queue_usage.py --egress_bottleneck '1GiB' \
#                         --full_queue_depth '10000packets'\
#                         --flow_type 'iperf_UDP' \
#                         --egress_queue_rate '10packets'\
#                         --task 'basic_Forwarding_competing'\
#                         --experiment 3\
#                         --folder_path 'basic_forwarding_queue_rate_effect/'\
#                         --downsample_rate 50\

# *************************************************************************************************************



####################################### CLONING FORWARDING  ################################################################################

#[1] ########## TEST THE EFFECT OF FULL QUEUE DEPTH  ON THE QUEUE USAGE ##########  Verrified settings

# BASIC FORWARDING with CLONING CREDIT-BASE-FLOW-CONTROL

# python queue_usage.py --egress_bottleneck '1GiB'\
#                         --full_queue_depth '10000packets'\
#                         --queue_depth_limit '10000packets' \
#                         --egress_queue_rate '10packets'\
#                         --weight_rate '2:1'\
#                         --flow_type 'iperf_UDP'\
#                             --task 'clone_Forwarding_competing'\
#                             --folder_path 'clone_forwarding_full_queue_depth_effect/'\
#                             --downsample_rate 50\
#                             --experiment 1\

# python queue_usage.py --egress_bottleneck '1GiB'\
#                         --full_queue_depth '50000packets'\
#                         --queue_depth_limit '50000packets' \
#                         --egress_queue_rate '10packets'\
#                         --weight_rate '2:1'\
#                         --flow_type 'iperf_UDP'\
#                             --task 'clone_Forwarding_competing'\
#                             --folder_path 'clone_forwarding_full_queue_depth_effect/'\
#                             --downsample_rate 50\
#                             --experiment 2\




# [2] ########## TEST THE EFFECT OF QUEUE RATE ON THE QUEUE USAGE #################  Verfiied settings
# Testing queu rates : 10, 20, 70, 100
# python queue_usage.py --egress_bottleneck '1GiB'\
#                         --full_queue_depth '10000packets'\
#                         --queue_depth_limit '10000packets' \
#                         --flow_type 'iperf_UDP'\
#                         --egress_queue_rate '10packets'\
#                         --weight_rate '2:1'\
#                             --task 'clone_Forwarding_competing'\
#                             --folder_path 'clone_forwarding_queue_rate_effect/'\
#                             --downsample_rate 50\
#                             --experiment 1\

# python queue_usage.py --egress_bottleneck '1GiB'\
#                         --full_queue_depth '10000packets'\
#                         --queue_depth_limit '10000packets' \
#                         --flow_type 'iperf_UDP'\
#                         --egress_queue_rate '20packets'\
#                         --weight_rate '2:1'\
#                             --task 'clone_Forwarding_competing'\
#                             --folder_path 'clone_forwarding_queue_rate_effect/'\
#                             --downsample_rate 50\
#                             --experiment 2\



# python queue_usage.py --egress_bottleneck '1GiB'\
#                         --full_queue_depth '10000packets'\
#                         --queue_depth_limit '10000packets' \
#                         --flow_type 'iperf_UDP'\
#                         --egress_queue_rate '70packets'\
#                         --weight_rate '2:1'\
#                         --task 'clone_Forwarding_competing'\
#                         --folder_path 'clone_forwarding_queue_rate_effect/'\
#                         --downsample_rate 50\
#                         --experiment 3\

# python queue_usage.py --egress_bottleneck '1GiB'\
#                         --full_queue_depth '10000packets'\
#                         --queue_depth_limit '10000packets' \
#                         --flow_type 'iperf_UDP'\
#                         --egress_queue_rate '100packets'\
#                         --weight_rate '2:1'\
#                             --task 'clone_Forwarding_competing'\
#                             --folder_path 'clone_forwarding_queue_rate_effect/'\
#                             --downsample_rate 50\
#                             --experiment 4\


# python queue_usage.py --egress_bottleneck '1GiB'\
#                         --full_queue_depth '10000packets'\
#                         --queue_depth_limit '10000packets' \
#                         --flow_type 'iperf_UDP'\
#                         --egress_queue_rate '100packets'\
#                         --weight_rate '2:1'\
#                             --task 'clone_Forwarding_competing'\
#                             --folder_path 'clone_forwarding_queue_rate_effect/'\
#                             --downsample_rate 50\
#                             --cloning_delay '3000000microseconds'\
#                             --experiment 5\




# [3] ########## TEST THE EFFECT OF THE EGRESS  CLONING DELAY ON THE QUEUE USAGE ##############

# WITHOUT DELAY
### NEDDED to be repeated (error)
# python queue_usage.py --egress_bottleneck '1GiB'\
#                         --full_queue_depth '10000packets'\
#                         --queue_depth_limit '10000packets'\
#                         --flow_type 'iperf_UDP'\
#                         --egress_queue_rate '10packets'\
#                         --weight_rate '2:1'\
#                             --task 'clone_Forwarding_competing'\
#                             --folder_path 'clone_forwarding_egress_clone_delay_effect/'\
#                             --downsample_rate 50\
#                             --cloning_delay 'NODelay'\
#                             --experiment 1\


# WITH DELAY = 1500 microseconds
# python queue_usage.py --egress_bottleneck '1GiB'\
#                         --full_queue_depth '10000packets'\
#                         --queue_depth_limit '10000packets'\
#                         --flow_type 'iperf_UDP'\
#                         --egress_queue_rate '10packets'\
#                         --weight_rate '2:1'\
#                             --task 'clone_Forwarding_competing'\
#                             --folder_path 'clone_forwarding_egress_clone_delay_effect/'\
#                             --downsample_rate 50\
#                             --cloning_delay '1500microseconds'\
#                             --experiment 2\


# WITH DELAY =  3000000 microseconds (3seconds)
# python queue_usage.py --egress_bottleneck '1GiB'\
#                         --full_queue_depth '10000packets'\
#                         --queue_depth_limit '10000packets'\
#                         --flow_type 'iperf_UDP'\
#                         --egress_queue_rate '10packets'\
#                         --weight_rate '2:1'\
#                             --task 'clone_Forwarding_competing'\
#                             --folder_path 'clone_forwarding_egress_clone_delay_effect/'\
#                             --downsample_rate 50\
#                             --cloning_delay '3000000microseconds'\
#                             --experiment 3\












# [5] ########## TEST THE EFFECT OF FLOW TYPE ON THE QUEUE USAGE ##################
# [6] ########## TEST THE EFFECT OF NO QUEUE LIMIT WITH DIFFERENT FULL QUEUE DEPTH ON THE QUEUE USAGE ##########
# [7] ########## TEST THE EFFECT OF WEIGHT RATE ON THE QUEUE USAGE ################