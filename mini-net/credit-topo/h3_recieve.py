#!/usr/bin/python3

import sys
import struct
import os

from scapy.all import sniff, sendp, hexdump, get_if_list, get_if_hwaddr
from scapy.all import Packet, IPOption
from scapy.all import ShortField, IntField, LongField, BitField, FieldListField, FieldLenField
from scapy.all import IP, TCP, UDP, Raw, IPv6, ARP, BOOTP
from scapy.all import *
from scapy.layers.inet import _IPOption_HDR


def get_if():
    ifs = get_if_list()
    iface = None
    for i in ifs:
        if "h3-eth0" in i or "h2-eth0" in i or "h1-eth0" in i:
            iface = i
            break
    if not iface:
        print("Cannot find suitable interface")
        exit(1)
    return iface


def handle_pkt(pkt):
    if not (BOOTP in pkt or ARP in pkt or IPv6 in pkt):
        print("Got a packet:")
        pkt.show2()
        sys.stdout.flush()


def main():
    iface = get_if()
    print("Sniffing on %s" % iface)
    sys.stdout.flush()
    sniff(iface=iface, prn=lambda x: handle_pkt(x))


if __name__ == '__main__':
    main()
