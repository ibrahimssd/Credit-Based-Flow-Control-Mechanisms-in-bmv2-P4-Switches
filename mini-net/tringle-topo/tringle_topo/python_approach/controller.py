from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI
controller = SimpleSwitchThriftAPI(9091,'127.0.0.1')    #'10.10.1.101')
# Arp table
controller.table_add('arp_lpm','arp_forward',['160.16.11.100/32'],['1'])
controller.table_add('arp_lpm','arp_forward',['160.16.31.100/32'],['2'])
controller.table_add('arp_lpm','arp_forward',['160.16.12.100/32'],['3'])
controller.table_add('arp_lpm','arp_forward',['10.0.0.4/32'],['4'])
# ipv4 table
controller.table_add('ipv4_lpm','ipv4_forward',['160.16.11.100/32'],['1'])
controller.table_add('ipv4_lpm','ipv4_forward',['160.16.31.100/32'],['2'])
controller.table_add('ipv4_lpm','ipv4_forward',['160.16.12.100/32'],['3'])
controller.table_add('ipv4_lpm','ipv4_forward',['10.0.0.4/32'],['4'])



