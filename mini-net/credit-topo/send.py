#!/usr/bin/python3
import argparse
# import sys
import socket
# import random
# import struct
import argparse

#   hexdump(pkt)
from scapy.all import sendp, get_if_list, get_if_hwaddr , get_if_addr
from scapy.all import Packet
from scapy.all import Ether, IP, UDP, TCP , DNS


def get_if():
    ifs=get_if_list()
    iface=None # "h1-eth0"
    for i in get_if_list():
        print(i)
        if "enp0s8" in i:
            iface=i
            break
        if "h1-eth0" in i:
            iface=i
            break
        if "h2-eth0" in i:
            iface=i
            break
        if "h3-eth0" in i:
            iface=i
            break
    if not iface:
        print("Cannot find enp0s8 interface")
        exit(1)
    return iface
 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ip_addr', type=str, help="The destination IP address to use")
    parser.add_argument('message', type=str, help="The message to include in packet")
    args = parser.parse_args()

    addr = socket.gethostbyname(args.ip_addr)
    iface = get_if()
    

    
    print(("sending on interface {} to IP addr {} , message {} ".format(iface, str(addr), args.message)))
    pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
    pkt = pkt /IP(dst=addr)/TCP()/args.message
    # IP(src=get_if_addr(iface),

    pkt.show2()
    sendp(pkt, iface=iface, verbose=False)


if __name__ == '__main__':
    main()
