/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

const bit<16> TYPE_IPV4 = 0x0800;
const bit<16> TYPE_ARP = 0x0806;

/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/

typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;
typedef bit<16> etherType_t;
typedef bit<32> switchID_t;
typedef bit<32> portID_t;
typedef bit<32> flowID_t;
typedef bit<4>  switchType_t;


header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    etherType_t   etherType;
}

header arp_t{
   // ARP packet size = 26 bytes

    bit<16> hardware_type;
    bit<16> protocol_type;
    bit<8>  hardware_length;
    bit<8>  protocol_length;
    bit<16> op_code;
    macAddr_t sender_hAddress;
    ip4Addr_t sender_pAddress;
    macAddr_t target_hAddress;
    ip4Addr_t target_pAddress;
}

header ipv4_t {
    // IPv4 packet size = 20 bytes
    bit<4>    version;
    bit<4>    ihl;
    bit<8>    diffserv;
    bit<16>   totalLen;
    bit<16>   identification;
    bit<3>    flags;
    bit<13>   fragOffset;
    bit<8>    ttl;
    bit<8>    protocol;
    bit<16>   hdrChecksum;
    ip4Addr_t srcAddr;
    ip4Addr_t dstAddr;
}

struct metadata {
    flowID_t flowID;
    switchID_t switch_id;
    switchType_t switch_type;
    /* empty */
}

struct headers {
    ethernet_t   ethernet;
    arp_t        arp;
    ipv4_t       ipv4;

}

/*************************************************************************
*********************** P A R S E R  ***********************************
*************************************************************************/

parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start {
        transition parse_ethernet;
    }

    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            TYPE_ARP: parse_arp;
            TYPE_IPV4: parse_ipv4;
            default: accept;
        }
    }
         
    //  state parse_ethernet {
    //     packet.extract(hdr.ethernet);
    //     transition hdr.ethernet.etherType == TYPE_ARP ? parse_arp : (hdr.ethernet.etherType == TYPE_IPV4 ? parse_ipv4 : accept)
    // }
          

    state parse_arp{
        packet.extract(hdr.arp);
        transition accept;
        
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition accept;
    }



}

/*************************************************************************
************   C H E C K S U M    V E R I F I C A T I O N   *************
*************************************************************************/

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply {
        
      }
}


/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {
    action drop() {
        mark_to_drop(standard_metadata);
    }
    
    // action ipv4_forward(egressSpec_t port) {
    //     standard_metadata.egress_spec = port;
    //     // hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;
    //     // hdr.ethernet.dstAddr = dstAddr;
    //     // hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
    // }
    

    action ipv4_forward(egressSpec_t port , switchID_t swid , flowID_t flowid , switchType_t natureId) {
    standard_metadata.egress_spec = port;
    meta.switch_id = swid; 
    meta.flowID = flowid; 
    meta.switch_type= natureId;
}

    action arp_forward( egressSpec_t port ){

        standard_metadata.egress_spec=port;
        
    }


    table arp_lpm {
         key = {
           hdr.arp.target_pAddress:lpm;

         }

         actions = {
            arp_forward;
            drop;
            NoAction;
         }

         size=1024;
         default_action =   drop();
    }
    

    table ipv4_lpm {
        key = {
            // hdr.ipv4.dstAddr: lpm;
            // edit
            hdr.ipv4.srcAddr: exact;
            hdr.ipv4.dstAddr: exact;
        }
        actions = {
            ipv4_forward;
            drop;
            NoAction;
        }
        size = 1024;
        default_action = drop();
    }


    
    apply {

        if (hdr.arp.isValid()){
              arp_lpm.apply();
        } 
        
        if (hdr.ipv4.isValid()){
            ipv4_lpm.apply();
            
        }

        
    }
}


/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {

    table egress_debug {
        key = {            
            
            
            standard_metadata.egress_global_timestamp:exact;
            standard_metadata.packet_length:exact;
            meta.switch_id:exact;
            meta.switch_type:exact;
            meta.flowID :exact;
            
            hdr.ipv4.protocol:exact;
            hdr.ipv4.srcAddr:exact;
            hdr.ipv4.dstAddr:exact;
            hdr.ethernet.etherType:exact;   

            standard_metadata.deq_qdepth: exact; 
            standard_metadata.enq_qdepth: exact;
            
        }

        actions = { }
    }

    apply { 

        egress_debug.apply();

     }
}

/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   **************
*************************************************************************/

control MyComputeChecksum(inout headers hdr, inout metadata meta) {
     apply {

    }
}


/*************************************************************************
***********************  D E P A R S E R  *******************************
*************************************************************************/

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        //parsed headers have to be added again into the packet.
         packet.emit(hdr);
        // packet.emit(hdr.ethernet);
    }
}

/*************************************************************************
***********************  S W I T C H  *******************************
*************************************************************************/

//switch architecture
V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;