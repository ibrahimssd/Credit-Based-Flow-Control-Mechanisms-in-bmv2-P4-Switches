#!/usr/bin/python3

import sys
import struct
import os

from scapy.all import sniff, sendp, hexdump, get_if_list, get_if_hwaddr
from scapy.all import Packet, IPOption
from scapy.all import ShortField, IntField, LongField, BitField, FieldListField, FieldLenField
from scapy.all import IP, TCP, UDP, Raw, IPv6, ARP ,BOOTP
from scapy.all import *
from scapy.layers.inet import _IPOption_HDR


def get_if():
    ifs=get_if_list()
    iface=None
    for i in get_if_list():
        if "h1-eth0" in i:
            iface=i
            break
    if not iface:
        print("Cannot find enp0s8 interface")
        exit(1)
    return iface

def handle_pkt(pkt):
    # if MyTunnel in pkt or
    
    if ( not BOOTP in pkt and not ARP in pkt  and not IPv6 in pkt ):
        print("got a packet")
        pkt.show2()
#       hexdump(pkt)
#       print "len(pkt) = ", len(pkt)
        sys.stdout.flush()


def main():
    ifaces = [i for i in os.listdir('/sys/class/net/') if 'enp0s' in i]
    iface = 'h1-eth0' #ifaces[1]
    # print(ifaces)
    print(("sniffing on %s" % iface))
    sys.stdout.flush()
    sniff(iface = iface,
          prn = lambda x: handle_pkt(x))

if __name__ == '__main__':
    main()