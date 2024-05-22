from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI


#---------------------------------- Switch (1) Rules ---------------------------------------------------------#
switch1_controller = SimpleSwitchThriftAPI(9091)

# Forwarding Rules
# arp_lpm table: arp_forward
switch1_controller.table_add('arp_lpm','arp_forward',['160.16.11.100/32'],['1'])
switch1_controller.table_add('arp_lpm','arp_forward',['160.16.12.100/32'],['4'])
switch1_controller.table_add('arp_lpm','arp_forward',['160.16.31.100/32'],['2'])
switch1_controller.table_add('arp_lpm','arp_forward',['10.10.10.3/32'],['3'])

# ipv4_lpm table: ipv4_forward
# egressSpec_t port , switchID_t swid , switchID_t flowid , flowWeight, switchType_t natureId
# nature ID: 0: ingress, 1: egress, 2: natural
switch1_controller.table_add('ipv4_lpm','ipv4_forward',['160.16.31.100','160.16.11.100'],['1','1','1','4','2'])
switch1_controller.table_add('ipv4_lpm','ipv4_forward',['160.16.31.100','160.16.12.100'],['4','1','2','8','2'])
switch1_controller.table_add('ipv4_lpm','ipv4_forward',['160.16.11.100','160.16.31.100'],['2','1','1','4','0'])
switch1_controller.table_add('ipv4_lpm','ipv4_forward',['160.16.12.100','160.16.31.100'],['2','1','2','8','0'])
# switch1_controller.table_add('ipv4_lpm','ipv4_forward',['10.10.10.3'],['3','1','1','0'])


# Cloning Rules
# mirroring table: mirroring_add
switch1_controller.mirroring_add(1,1)
switch1_controller.mirroring_add(2,2)
switch1_controller.mirroring_add(3,3)

# Queueing Rules 
# set_queue_depth
# switch1_controller.set_queue_depth(100,1)
# switch1_controller.set_queue_depth(100,2)
# switch1_controller.set_queue_depth(100,3)

#---------------------------------- Switch (2) Rules ---------------------------------------------------------#
switch2_controller = SimpleSwitchThriftAPI(9092)
# Forwarding Rules
# arp_lpm table: arp_forward 
switch2_controller.table_add('arp_lpm','arp_forward',['160.16.11.100/32'],['2'])
switch2_controller.table_add('arp_lpm','arp_forward',['160.16.12.100/32'],['2'])
switch2_controller.table_add('arp_lpm','arp_forward',['160.16.31.100/32'],['1'])
switch2_controller.table_add('arp_lpm','arp_forward',['10.10.10.3/32'],['3'])

# ipv4_lpm table: ipv4_forward
# egressSpec_t port , switchID_t swid , switchID_t flowid , flowWeight, switchType_t natureId
switch2_controller.table_add('ipv4_lpm','ipv4_forward',['160.16.11.100','160.16.31.100'],['1','2','1','4','2'])
switch2_controller.table_add('ipv4_lpm','ipv4_forward',['160.16.12.100','160.16.31.100'],['1','2','2','8','2'])
switch2_controller.table_add('ipv4_lpm','ipv4_forward',['160.16.31.100','160.16.11.100'],['2','2','1','4','0'])
switch2_controller.table_add('ipv4_lpm','ipv4_forward',['160.16.31.100','160.16.12.100'],['2','2','2','8','0'])
# switch2_controller.table_add('ipv4_lpm','ipv4_forward',['10.10.10.3'],['3','2','1','0'])

# Cloning Rules
# mirroring table: mirroring_add
switch2_controller.mirroring_add(1,1)
switch2_controller.mirroring_add(2,2)
switch2_controller.mirroring_add(3,3)

# Queueing rules 
# set_queue_depth
full_queue_depth = 10000
switch2_controller.set_queue_depth(full_queue_depth,1) # number of packets
switch2_controller.set_queue_depth(full_queue_depth,2)
switch2_controller.set_queue_depth(full_queue_depth,3)
switch2_controller.set_queue_depth(full_queue_depth,4)

# Add queuing rates  (in Mbps)
switch2_controller.set_queue_rate(10,1) 
