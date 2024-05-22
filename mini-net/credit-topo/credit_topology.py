# from cgitb import enable
from p4utils.mininetlib.network_API import NetworkAPI

def run_switches():
    try:
        # Define network topology
        net = NetworkAPI()
        net.addP4Switch('s1') # other_config=['--max-buffer=2000000']
        net.addP4Switch('s2') # other_config=['--max-buffer=2000000']
        net.addHost('h1')
        net.addHost('h2')
        net.addHost('h3')
        net.addHost('h4')  #controller

        # Assign P4 code to switches
        # p4_source_file = 'basic_forwarding.p4'
        p4_source_file = 'clone.p4'
        net.setP4Source('s1', p4_source_file)
        net.setP4Source('s2', p4_source_file)

        # Assign device IDs to switches
        s1_id = 1
        s2_id = 2
        net.setP4SwitchId('s1', s1_id)
        net.setP4SwitchId('s2', s2_id)

        # Assign thrift ports
        s1_thrift_port = 9091
        s2_thrift_port = 9092
        net.setThriftPort('s1', s1_thrift_port)
        net.setThriftPort('s2', s2_thrift_port)

        # Connect the topology
        net.addLink('s1', 'h1')
        net.addLink('s1', 'h3')
        net.addLink('s1', 's2')
        net.addLink('s2', 'h2')
        net.addLink('s1', 'h4')
        net.addLink('s2', 'h4')

        # Set interface ports for the connections
        s1_h1_port = 1
        h1_s1_port = 0
        s1_h3_port = 4
        h3_s1_port = 0
        s1_s2_port = 2
        s2_s1_port = 2
        s2_h2_port = 1
        h2_s2_port = 0
        s1_h4_port = 1
        h4_s1_port = 3
        s2_h4_port = 2
        h4_s2_port = 3
        net.setIntfPort('s1', 'h1', s1_h1_port) # The interface of s1 facing h1
        net.setIntfPort('h1', 's1', h1_s1_port)  # The interface of h1 facing s1
        net.setIntfPort('s1', 'h3', s1_h3_port)
        net.setIntfPort('h3', 's1', h3_s1_port)
        net.setIntfPort('s1', 's2', s1_s2_port)
        net.setIntfPort('s2', 's1', s2_s1_port)
        net.setIntfPort('s2', 'h2', s2_h2_port)
        net.setIntfPort('h2', 's2', h2_s2_port)
        net.setIntfPort('h4', 's1', s1_h4_port)
        net.setIntfPort('s1', 'h4', h4_s1_port)
        net.setIntfPort('h4', 's2', s2_h4_port)
        net.setIntfPort('s2', 'h4', h4_s2_port)

        # Set IP addresses and MAC addresses for interfaces
        s1_h1_ip = '160.16.11.10/24'
        s1_h1_mac = '00:00:00:00:10:11'
        h1_s1_ip = '160.16.11.100/24'
        h1_s1_mac = '00:00:00:00:11:01'
        s1_h3_ip = '160.16.12.10/24'
        s1_h3_mac = '00:00:00:00:10:12'
        h3_s1_ip = '160.16.12.100/24'
        h3_s1_mac = '00:00:00:00:12:01'
        s2_h2_ip = '160.16.31.10/24'
        s2_h2_mac = '00:00:00:00:20:10'
        h2_s2_ip = '160.16.31.100/24'
        h2_s2_mac = '00:00:00:00:21:00'
        s1_s2_ip = '160.16.1.10/24'
        s1_s2_mac = '00:00:00:00:01:02'
        s2_s1_ip = '160.16.1.20/24'
        s2_s1_mac = '00:00:00:00:02:01'
        s1_h4_ip = '10.10.10.1/24'
        s1_h4_mac = '00:00:00:00:00:01'
        h4_s1_ip = '10.10.10.3/24'
        s2_h4_ip = '10.10.10.2/24'
        h4_s2_ip = '10.10.10.4/24'
        net.setIntfIp('s1', 'h1', s1_h1_ip) # The interface of s1 facing h1
        net.setIntfMac('s1', 'h1', s1_h1_mac)
        net.setIntfIp('h1', 's1', h1_s1_ip)  # The interface of h1 facing s1
        net.setIntfMac('h1', 's1', h1_s1_mac) 
        net.setIntfIp('s1', 'h3', s1_h3_ip)  # The interface of s1 facing h3
        net.setIntfMac('s1', 'h3', s1_h3_mac)
        net.setIntfIp('h3', 's1', h3_s1_ip) # The interface of h3 facing s1
        net.setIntfMac('h3', 's1', h3_s1_mac)
        net.setIntfIp('s2', 'h2', s2_h2_ip)   # The interface of s2 facing h2
        net.setIntfMac('s2', 'h2', s2_h2_mac)
        net.setIntfIp('h2', 's2', h2_s2_ip)   # The interface of h2 facing s2
        net.setIntfMac('h2', 's2', h2_s2_mac)
        net.setIntfIp('s1', 's2', s1_s2_ip)  # The interface of s1 facing s2
        net.setIntfMac('s1', 's2', s1_s2_mac)
        net.setIntfIp('s2', 's1', s2_s1_ip) # The interface of s2 facing s1
        net.setIntfMac('s2', 's1', s2_s1_mac)
        net.setIntfIp('s1', 'h4', s1_h4_ip) # The interface of s1 facing h4
        net.setIntfIp('h4', 's1', h4_s1_ip) # The interface of h4 facing s1
        net.setIntfIp('s2', 'h4', s2_h4_ip) # The interface of s2 facing h4
        net.setIntfIp('h4', 's2', h4_s2_ip) # The interface of h4 facing s2

        # Set link bandwidth
        link_bandwidth = 1000
        # net.setBwAll(link_bandwidth)
        # Set bandwidth for specific link
        net.setBw('h1', 's1', link_bandwidth)
        net.setBw('h3', 's1', link_bandwidth)
        net.setBw('s1', 's2', link_bandwidth)
        net.setBw('s2', 'h2', link_bandwidth)
        

        # Set link delay 
        link_delay = 10 # RTT 60ms
        net.setDelay('h1', 's1', link_delay)
        net.setDelay('h3', 's1', link_delay)
        net.setDelay('s1', 's2', link_delay)
        net.setDelay('s2', 'h2', link_delay)
        # Enable logging for all nodes
        log_directory = './logs'
        net.enableLogAll(log_directory)
        # set log for only switches
        # net.enableLog('s1', log_directory)
        # Start the network
        net.enableCli()
        net.startNetwork()

    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == '__main__':
    run_switches()
