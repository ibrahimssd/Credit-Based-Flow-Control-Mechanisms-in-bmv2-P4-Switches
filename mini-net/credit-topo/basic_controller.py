from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI

################ Rules for s1 ####################################################################################################
switch1_controller = SimpleSwitchThriftAPI(9091)

################ Arp rules ################
switch1_controller.table_add('arp_lpm','arp_forward',['160.16.11.100/32'],['1'])
switch1_controller.table_add('arp_lpm','arp_forward',['160.16.31.100/32'],['2'])
switch1_controller.table_add('arp_lpm','arp_forward',['10.10.10.3/32'],['3'])
switch1_controller.table_add('arp_lpm','arp_forward',['160.16.12.100/32'],['4'])
################ IPv4 rules ################

# switch1_controller.table_add('ipv4_lpm','ipv4_forward',['160.16.11.100/32'],['1'])
# switch1_controller.table_add('ipv4_lpm','ipv4_forward',['160.16.31.100/32'],['2'])
# switch1_controller.table_add('ipv4_lpm','ipv4_forward',['10.10.10.3/32'],['3'])
# switch1_controller.table_add('ipv4_lpm','ipv4_forward',['160.16.12.100/32'],['4'])

# UPDATE: 2021-05-25
# nature ID: 0: ingress, 1: egress, 2: natural
# action ipv4_forward(egressSpec_t port , switchID_t swid , flowID_t flowid , switchType_t natureId)
switch1_controller.table_add('ipv4_lpm','ipv4_forward',['160.16.31.100','160.16.11.100'],['1','1','1','2'])
switch1_controller.table_add('ipv4_lpm','ipv4_forward',['160.16.31.100','160.16.12.100'],['4','1','2','2'])
switch1_controller.table_add('ipv4_lpm','ipv4_forward',['160.16.11.100','160.16.31.100'],['2','1','1','0'])
switch1_controller.table_add('ipv4_lpm','ipv4_forward',['160.16.12.100','160.16.31.100'],['2','1','2','0'])



# Queueing rules
# DEAFULT: 64 packets
# set_queue_depth
# s1_full_queue_depth = 2000000    #2M packets # 64 packets
# switch1_controller.set_queue_depth(s1_full_queue_depth,1) # number of packets
# switch1_controller.set_queue_depth(s1_full_queue_depth,2)
# switch1_controller.set_queue_depth(s1_full_queue_depth,3)
# switch1_controller.set_queue_depth(s1_full_queue_depth,4)
# # add queuing rates  (packets per second)
# switch1_controller.set_queue_rate(2000000,2) # 1 0 packets per second



################ Rules for s2 ##################################################################################################################
switch2_controller = SimpleSwitchThriftAPI(9092)
################ Arp rules ################
switch2_controller.table_add('arp_lpm','arp_forward',['160.16.11.100/32'],['2'])
switch2_controller.table_add('arp_lpm','arp_forward',['160.16.31.100/32'],['1'])
switch2_controller.table_add('arp_lpm','arp_forward',['10.10.10.4/32'],['3'])
switch2_controller.table_add('arp_lpm','arp_forward',['160.16.12.100/32'],['2'])
################ IPv4 rules ################
# switch2_controller.table_add('ipv4_lpm','ipv4_forward',['160.16.11.100/32'],['2'])
# switch2_controller.table_add('ipv4_lpm','ipv4_forward',['160.16.31.100/32'],['1'])
# switch2_controller.table_add('ipv4_lpm','ipv4_forward',['10.10.10.4/32'],['3'])
# switch2_controller.table_add('ipv4_lpm','ipv4_forward',['160.16.12.100/32'],['2'])


# UPDATE: 2021-05-25
# nature ID: 0: ingress, 1: egress, 2: natural
# action ipv4_forward(egressSpec_t port , switchID_t swid , flowID_t flowid , switchType_t natureId)
switch2_controller.table_add('ipv4_lpm','ipv4_forward',['160.16.11.100','160.16.31.100'],['1','2','1','2'])
switch2_controller.table_add('ipv4_lpm','ipv4_forward',['160.16.12.100','160.16.31.100'],['1','2','2','2'])
switch2_controller.table_add('ipv4_lpm','ipv4_forward',['160.16.31.100','160.16.11.100'],['2','2','1','0'])
switch2_controller.table_add('ipv4_lpm','ipv4_forward',['160.16.31.100','160.16.12.100'],['2','2','2','0'])


# Queueing rules 
# DEAFULT: 64 packets
# Verified: 10000 packets
# set_queue_depth
s2_full_queue_depth = 10000    #2M packets # 64 packets
switch2_controller.set_queue_depth(s2_full_queue_depth,1) # number of packets
switch2_controller.set_queue_depth(s2_full_queue_depth,2)
switch2_controller.set_queue_depth(s2_full_queue_depth,3)
switch2_controller.set_queue_depth(s2_full_queue_depth,4)
# add queuing rates  (packets per second)
switch2_controller.set_queue_rate(100,1) # 1 0 packets per second
# when we increase the queue rate the max usage decreases.