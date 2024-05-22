/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

// Define constants for types of cloned packets
#define PKT_INSTANCE_TYPE_NORMAL 0
#define PKT_INSTANCE_TYPE_INGRESS_CLONE 1
#define PKT_INSTANCE_TYPE_EGRESS_CLONE 2
#define PKT_INSTANCE_TYPE_COALESCED 3
#define PKT_INSTANCE_TYPE_INGRESS_RECIRC 4
#define PKT_INSTANCE_TYPE_REPLICATION 5
#define PKT_INSTANCE_TYPE_RESUBMIT 6


// Define constants for types of packets
const bit<16> TYPE_IPV4 = 0x0800;
const bit<16> TYPE_ARP = 0x0806;
const bit<8>  IPV4_OPTION_CREDIT = 0x31;

// Define constants for queu depth

const bit<19> allowed_queu_depth = 80;
const bit<19> full_queue_depth = 100;



// minimum size of ethernet, ipv4 and credit headers
const bit<8> Ethernet_length= 14; //bytes
const bit<8> Ipv4_length= 20; //bytes
const bit<8> Arp_length= 26;
const bit<8> Ipv4_option_length= 3; // 3 bytes 
const bit<8> credit_length= 8; //bytes
const bit<8> ipv4_packet_len = Ethernet_length+Ipv4_length+Ipv4_option_length+credit_length;// bytes;
const bit<8> arp_packet_len = Ethernet_length+Arp_length+Ipv4_option_length+credit_length;// bytes;
        

/*           Errors            */
error { IPHeaderTooShort }



/*************************************************************************
*********************** D A T A   T Y P E S  ***********************************
*************************************************************************/

typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;
typedef bit<32> switchID_t;
typedef bit<32> credval_t;
typedef bit<4>  switchType_t;
/*************************************************************************
*********************** R E G I S T E R S   ***********************************
*************************************************************************/


register<bit<32>>(1) flowIds_register; 

// save flow_id of the original packet to append in credit header of the cloned packet. 

/*
 0                  31
 |------------------|
 |   flowId(32)     |
 |------------------|
*/


register<bit<8>>(10) check_init_register; 

// save flow_id of the original packet to append in credit header of the cloned packet. 

/*
 0                    7
 |--------------------|
 |  initialization(8) |
 |--------------------|
*/


register<bit<32>>(10) credit_register;


/*
 0                  31
 |------------------|
 |   Credits(32)    |
 |------------------|
*/

register<bit<112>>(10) egress_register;

/*
 0                  31                   79            111
 |------------------+---------------------|-------------|
 |    Credit(32)    |    timestamp(48)    |  flowID(32) |
 |------------------+---------------------|-------------|
*/


/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/


header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
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

header ipv4_option_t {
    bit<3> copyFlag;
    bit<5> optClass;
    bit<8> option;
    bit<8> optionLength;
}

struct toCPU_t {
    bit<16> ingPort;
    bit<32> dstIP;
    bit<32> flowID;
}

header credit_t {
    credval_t creditValue;
    bit<32> flow_id; 
}
 
struct metadata {

    toCPU_t toCPU;
    switchID_t switch_id;
    switchID_t flowID;
    switchType_t switch_type; // 0,1,2 for credit , core , egress switches
    credval_t available_cred;
    credval_t computed_cred;
    credval_t status;
}

//struct credit header 

struct headers {
    ethernet_t    ethernet;
    arp_t         arp;
    ipv4_t        ipv4;
    ipv4_option_t ipv4_option;
    credit_t      credit;
}

/*************************************************************************
*********************** P A R S E R  ***********************************
*************************************************************************/

parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start{
    packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            TYPE_ARP: parse_arp;
            TYPE_IPV4: parse_ipv4;
            default: accept;
        }
    }

    state parse_arp{
        packet.extract(hdr.arp);
        transition accept;
        
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        verify(hdr.ipv4.ihl >= 5, error.IPHeaderTooShort);
        transition select(hdr.ipv4.ihl) {
            5             : accept;
            default       : parse_ipv4_option;
        }
    
        
    }

    state parse_ipv4_option {
        packet.extract(hdr.ipv4_option);
        transition select(hdr.ipv4_option.option) {
            IPV4_OPTION_CREDIT: parse_credit;
            default: accept;
        }
    } 

    state parse_credit {
        packet.extract(hdr.credit);
        transition accept;
    }

}

                

/*************************************************************************
************   C H E C K S U M    V E R I F I C A T I O N   *************
*************************************************************************/

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {   
    apply {  }
}

/*************************************************************************
            ************   G E T   C R E D I T   *************
*************************************************************************/

control GetCredit(inout headers hdr, inout metadata meta) {
    bit<32> tmp;
    bit<32> flowid;
    apply {

        //get the avialable credits at credit register and save them to meta data
        flowid= meta.flowID;
        credit_register.read(tmp, (bit<32>) flowid); 
        meta.available_cred = meta.available_cred + tmp[31:0];
        
    }
}

/*************************************************************************
            ************   I N I T   R E G I S T E R   *************
*************************************************************************/

// initialize register with some random credits for forwarding. 
control RegInit( inout metadata meta) {
    bit<32> tmp;
    bit<8> tmp_init;
    bit<32> cred;
    bit <32> flowid;
    bit<8> check_initialization;
    apply {

        //assign packet flow id 
        flowid = meta.flowID;         
        credit_register.read(tmp, flowid); 
        check_init_register.read(tmp_init, flowid);

        check_initialization = tmp_init[7:0];

        if(check_initialization==0){

        tmp[31:0]=100;
        tmp_init[7:0]=1;
        credit_register.write((bit<32>) flowid, tmp);
        check_init_register.write(flowid,tmp_init);
        }

        
        
        
        // tmp[79:32] = standard_metadata.inggress_global_timestamp;
        
        //if(cred==0){ //initialize register if it is empty
        
        
        
        //}
    }
}


/*************************************************************************
  ************   S E T   C R E D I T S T O R I G I S T E R *************
*************************************************************************/

control AddCredit(inout headers hdr , 
                 inout metadata meta,
                 inout  standard_metadata_t standard_metadata){
    bit<32> tmp;
    bit<32> curr_credit;
    bit <32> flowid;

    apply{
        
        flowid= hdr.credit.flow_id;
        //get the available credit
        credit_register.read(tmp,(bit<32>) flowid);

        //increment the credit
        curr_credit= tmp[31:0] ;
        curr_credit= curr_credit + hdr.credit.creditValue;
        tmp[31:0] =  curr_credit;        
        //set the new credit value in the register
        credit_register.write((bit<32>) flowid, tmp);
    }
}


/*****************************************************************************************
************   S U B T R A C T  C R E D I T S   F R O M  R I G I S T E R ********
******************************************************************************************/

control DecrementCredit(inout headers hdr, inout metadata meta ,inout standard_metadata_t standard_metadata) {

    bit<32> curr_credit;
    bit<32> tmp;
    bit<32> flowid;

    apply {
        flowid =meta.flowID;
        //get the current value of credit
        credit_register.read(tmp, (bit<32>) flowid);

        //decrement the credit 
        curr_credit = tmp[31:0] - 1;

        //save the new value of credit
        tmp[31:0] = curr_credit;
        credit_register.write(flowid, tmp);
    
    }
}

/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/
     

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {
    
    AddCredit()           add_credit;
    DecrementCredit()     sub_credit;
    GetCredit()           get_credit;
    RegInit()             initialize_reg;

action drop() {
    mark_to_drop(standard_metadata);
}
    
action ipv4_forward(egressSpec_t port , switchID_t swid , switchID_t flowid , switchType_t natureId) {
    standard_metadata.egress_spec = port;
    meta.switch_id = swid; // save switch id in meta data
    meta.flowID = flowid ; // save flow id in meta data
    meta.switch_type= natureId;// save switch type in meta data (S1:0, S2:1, S3:2)
    // hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;
    // hdr.ethernet.dstAddr = dstAddr;
    //hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
}

action arp_forward( egressSpec_t port  ){

    standard_metadata.egress_spec=port;
    // hdr.arp.sender_hAddress= sender_mac;
    // hdr.arp.sender_pAddress = sender_ip;
}
    

table arp_lpm {
    key = {
        hdr.arp.target_pAddress:lpm;
    }

    actions = {
        // drop;
        arp_forward;
        drop;
        NoAction;
    }
    size=1024;
    const  default_action =   drop();
}
    

table ipv4_lpm {
    key = {
        hdr.ipv4.dstAddr: lpm;
    }
    actions = {
        drop;
        ipv4_forward;
        NoAction;
    }
    size = 1024;
    const default_action = drop();
}


    apply {
        

        if (hdr.arp.isValid()){
           arp_lpm.apply();
           // 
        } 

        
        else if (hdr.ipv4.isValid()){
            // !hdr.credit.isValid()
                        
            if (ipv4_lpm.apply().hit){

                // check credits availability ,subtract credits , else drop packet for ingress switch
                
                if (meta.switch_type==0){ 

                    if (!hdr.credit.isValid()){ //hdr.ethernet.etherType == TYPE_IPV4
                        get_credit.apply(hdr, meta);
                        if (meta.available_cred == 0){
                            initialize_reg.apply(meta);
                            // mark_to_drop(standard_metadata);
                        } else {
                                sub_credit.apply(hdr,meta,standard_metadata);
                        }
                    }    
            }

                
                // add credits for ingress switch
                if(meta.switch_type==2){

                   if (hdr.credit.isValid()){
                        //add the received credit to register
                        add_credit.apply(hdr, meta,standard_metadata);
                        //drop the cloned packet (credit packet)
                        // mark_to_drop(standard_metadata);
                    } 
                }
                    
            }

            else {  
                    // if(hdr.credit.isValid()){
                    //     meta.flowID=hdr.credit.flow_id;
                    // }

                    // first packet dropped 
                    meta.toCPU.ingPort = (bit<16>) standard_metadata.ingress_port;
                    meta.toCPU.dstIP = hdr.ipv4.dstAddr;
                    meta.toCPU.flowID = meta.flowID; 
                    
                    //digest packet
                    digest(meta.flowID, meta.toCPU);   
            }
        } 
    }            
}

/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control Queue_usage(inout metadata meta ,inout standard_metadata_t standard_metadata){

    
    credval_t computed_credits;
    
    int<32> diff;
     apply{
           
          // queu_depth and deq_qdepth both with size 19 bits
          // maximum allowed queu depth = 80 , full queue depth = 100 
          // 10% = 0.1 = (1/2^3)-(1/2^6)= 0.109375
          // 80% = 8*0.109375 = 0.875
          // 10% of 80 = 0.109375*80 =  8.75
          // 80% of 80 = 0.109375**80


          // check if the value is negative 
          if ((int<19>)standard_metadata.deq_qdepth >= (int<19>)allowed_queu_depth){

                meta.computed_cred =0;
                meta.status = 1;

          } else{
                
                // full available credits 
                computed_credits = (bit<32>)(allowed_queu_depth-standard_metadata.deq_qdepth); 

               

                // check if the queue reaches 80%(87.5 %) of usage. 
                if (standard_metadata.deq_qdepth>= ((8 * allowed_queu_depth)>> 3) - ((8 * allowed_queu_depth) >> 6) ){
                    
                    // send credit packet with only 20% (21.88 %) of queue usage. 
                    diff = ((2* (int<32>)computed_credits) >> 3 )-((2* (int<32>)computed_credits) >> 6);
                    
                    meta.computed_cred = (bit<32>) diff;
                    meta.status = 80;
                } 
                
                // check if the queue usage reaches 10% (10.9 %) , use the full available credits
                else if (standard_metadata.deq_qdepth <=  (allowed_queu_depth >> 3)-(allowed_queu_depth >> 6) ){
                    
                    meta.computed_cred = computed_credits; //(bit<32>) (full_queue_depth - standard_metadata.deq_qdepth);
                    meta.status = 10;
                }
                
                // when the queue usage is more than 10% (10.9 %) and less than 80%(87.5 %) send  60% of the computed credits
                else {
                    
                    // send 60% (65.6 %) of credits
                    diff = ((6* (int<32>)computed_credits) >> 3 )-((6* (int<32>) computed_credits) >> 6);
                    meta.computed_cred = (bit<32>) diff;
                    meta.status = 50;
                }
                } 
            }
            }


control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    
   bit<112> tmp;
   bit<32> tmp_id;
   bit<48> cloning_interval;
   bit<48> last_cloning_timestamp;
   bit<48> emptying_queue_time; 
   bit<32> floID;
   
   Queue_usage()  compute_queue_usage;    

   
  // display values in logs file for debuging
  table debug {
      
        key = {            
            
            meta.switch_id: exact;
            meta.flowID : exact;
            hdr.credit.flow_id:exact;
            meta.switch_type: exact;
            standard_metadata.egress_global_timestamp:exact;
            hdr.credit.creditValue: exact;
            standard_metadata.packet_length : exact;        
            standard_metadata.deq_qdepth: exact; 
            standard_metadata.enq_qdepth: exact;
            meta.computed_cred: exact;
            meta.status: exact;
            

            
        }

        actions = { }
    }

    



    action drop() {
        mark_to_drop(standard_metadata);
    }
 
    action clear_ttl (){
       hdr.ipv4.ttl =0;
    }

    action swap_addr(){
         bit<32> ipv4dst= hdr.ipv4.dstAddr;
         // 0xac100b64: 172.16.11.100 h11
         // 0xac101464 : 172.16.20.100 h2
         // 0xac101f64 : 172.16.31.100 h31
         //hdr.ipv4.totalLen=20;
         hdr.ipv4.dstAddr=  hdr.ipv4.srcAddr; // 0xac100b64;//
         hdr.ipv4.srcAddr=  ipv4dst; // 0xac101f64;;//
    }

    action clone_packet() {
        // const bit<32> REPORT_MIRROR_SESSION_ID1 = 500;
        // const bit<32> REPORT_MIRROR_SESSION_ID2 = 501;
        // Clone from egress to egress pipeline
        clone(CloneType.E2E, (bit<32>) standard_metadata.ingress_port);
    }
    
    // drop load from the packet ()
    action truncate_packet(in bit<8> new_length){
        truncate((bit<32>)new_length);
        // hdr.ipv4.totalLen=20;
    }

    action append_credit_header (bit<32> ID){
        //add credits to credit_header info 
        hdr.credit.setValid();
        hdr.credit.creditValue = 10; //meta.computed_cred;
        hdr.credit.flow_id= ID; 
        // hdr.credit.egressSwitchID = 4;
        // hdr.credit.timeStamp = standard_metadata.egress_global_timestamp;
        }   
    
    action append_option_header(){
       // assign credit type to option field 
       hdr.ipv4_option.setValid();
       hdr.ipv4_option.option = IPV4_OPTION_CREDIT;
       hdr.ipv4.ihl= hdr.ipv4.ihl+1 ;
    }

    apply {

        
        

        // check if it is egress to egress clonning (check if the packet is a cloned packet )
        if (standard_metadata.instance_type == PKT_INSTANCE_TYPE_EGRESS_CLONE) {
            
            
            

            // Get flow ID from egress register
            flowIds_register.read(tmp_id,(bit<32>) 0);
            floID = tmp_id[31:0];
            
            
            // process cloned packet , remove the load and append credit header
            if(hdr.ipv4.isValid() && hdr.ethernet.etherType == TYPE_IPV4 ){
            


            truncate_packet(ipv4_packet_len);   
            append_credit_header(floID);
            append_option_header();
            swap_addr();
            clear_ttl();
            
            }
            

            //set time for creating credits in egress register 
            egress_register.read(tmp,(bit<32>) floID);
            tmp[79:32] = standard_metadata.egress_global_timestamp;
            tmp[31:0]= hdr.credit.creditValue; //hdr.credit.flow_id; //
            egress_register.write((bit<32>) floID,tmp);
        
            
      // process the original packet

        } else {  

            // check if egress switch
            if (meta.switch_type==2){
                
                //the timestamp when the switch starts processing the packet

                // save flow id on flowIds_register at egress switch.
                /// use separate register for ids
                flowIds_register.read(tmp_id,(bit<32>) 0);
                tmp_id[31:0]= meta.flowID;
                flowIds_register.write((bit<32>) 0,tmp_id);
                
                
                

                // read time for clonning last packet
                egress_register.read(tmp,(bit<32>) meta.flowID);
                last_cloning_timestamp = tmp[79:32] ;  

                //the time interval between the last credit packet and the current one
                cloning_interval = standard_metadata.egress_global_timestamp - last_cloning_timestamp;
                
                // time to empty the queue delta 1500(packet size)/1MBps (link capacity)
                emptying_queue_time = 1500; // in micro seconds
                
                // pause sender for delta amount of time
                if(cloning_interval> emptying_queue_time){

                 
                 if(!hdr.credit.isValid()){

                    if(hdr.ipv4.isValid()&& hdr.ethernet.etherType== TYPE_IPV4){ 
                     
                    // compute queue usage (credits)
                    compute_queue_usage.apply(meta,standard_metadata);

                    // send credits back to sender
                    clone_packet();
                 
                 }

                 }

                }
            }
        }
        
    
    
    // debuging 
    debug.apply();
    
    
    
    }
}

/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   **************
*************************************************************************/

control MyComputeChecksum(inout headers  hdr, inout metadata meta) {
    apply {
	update_checksum(
	    hdr.ipv4.isValid(),
            { hdr.ipv4.version,
	      hdr.ipv4.ihl,
              hdr.ipv4.diffserv,
              hdr.ipv4.totalLen,
              hdr.ipv4.identification,
              hdr.ipv4.flags,
              hdr.ipv4.fragOffset,
              hdr.ipv4.ttl,
              hdr.ipv4.protocol,
              hdr.ipv4.srcAddr,
              hdr.ipv4.dstAddr },
              hdr.ipv4.hdrChecksum,
              HashAlgorithm.csum16);
    }
}

/*************************************************************************
***********************  D E P A R S E R  *******************************
*************************************************************************/

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        // packet.emit(hdr);
        packet.emit(hdr.ethernet);
        packet.emit(hdr.arp);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.ipv4_option);
        packet.emit(hdr.credit);
        
    }
}

/*************************************************************************
***********************  S W I T C H  *******************************
*************************************************************************/

V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;
