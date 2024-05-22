from p4utils.mininetlib.network_API import NetworkAPI

def start_network():
    
    net = NetworkAPI()
    net.setLogLevel('info')
    net.addP4Switch('s1')
    net.addHost('h1')
    net.addHost('h2')
    net.addHost('h3')
    net.addHost('controller')

    # pass p4 program
    net.setP4Source('s1','l2_forwarding.p4')
    net.setThriftPort('s1',9091)
    # net.setP4CliInput('s1','./cli_input.txt')
    
    # add links to nodes 
    net.addLink('s1', 'h1')
    net.addLink('s1', 'h2')
    net.addLink('s1', 'h3')
    net.addLink('s1','controller')

    # add ports 

    net.setIntfPort('s1', 'h1', 1)  # Set the number of the port on s1 facing h1
    net.setIntfPort('h1', 's1', 1)  # Set the number of the port on h1 facing s1
    net.setIntfPort('s1', 'h2', 2)  # Set the number of the port on s1 facing h2
    net.setIntfPort('h2', 's1', 2)  # Set the number of the port on h2 facing s1
    net.setIntfPort('s1', 'h3', 3)  # Set the number of the port on s1 facing h3
    net.setIntfPort('h3', 's1', 3)  # Set the number of the port on h3 facing s1
    net.setIntfPort('s1', 'controller',4)  # Set the number of the port on s1 facing h4
    net.setIntfPort('controller', 's1',4)  # Set the number of the port on h4 facing s1
    
    # set IP addresses for interfaces 
    h1_s1_ip = '160.16.11.100/24'
    h2_s1_ip = '160.16.31.100/24'
    h3_s1_ip = '160.16.12.100/24'

    net.setIntfIp('h1', 's1', h1_s1_ip)
    net.setIntfIp('h2', 's1', h2_s1_ip)
    net.setIntfIp('h3', 's1', h3_s1_ip)
    

    # set bandwidth for all links
    net.setBwAll(1000)
    # net.setDelay()
    # net.setLoss()
    # net.setBw('s1','h1', 5)

    # automatic assignment of IPs
    # net.l2()

    # net.enablePcapDumpAll()
    log_directory = './logs' 
    # net.enableLogAll(log_directory)

    #enable the network client and start the network
    net.enableCli()
    net.startNetwork()



if __name__ == '__main__':
    start_network()
