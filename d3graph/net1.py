import os
import socket, struct
import json
import nmap
from snmp_cmds import snmpwalk

currenthost = os.popen("netstat -nr").read()

print("\nnetstat value for current host:\n", currenthost)


def get_default_gateway_linux():
    """Read the default gateway directly from /proc."""
    print("\n\nGet default host gateway:")
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue

            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))


def snmp_check(host_gateway):

#    netstat_gateway = os.popen("snmpnetstat -v 2c -c public -Ci " + host_gateway).read()
#    return netstat_gateway
    print("\n\nSNMPnetstat for host gateway:" + host_gateway)
    netstat_gateway = os.popen("snmpnetstat -v 2c -c public -Cr " + host_gateway).read()
    snmpnetstat_split = netstat_gateway.split('IPv6 Routing tables (inetCidrRouteTable)', 2)
    ipv4_table = snmpnetstat_split[0]
    return ipv4_table




def get_allhost_details(ip_details):

    print("\n\nhost details:")
    # initialize the port scanner
    nmScan = nmap.PortScanner()
    # scan localhost for ports in range 21-443
    currenthost1 = os.popen("netstat -nr").read()
    nmScan.scan(currenthost1, '21-443')
    # run a loop to print all the found result about the port
    for ip_details in nmScan.all_hosts():
        print('Host : %s (%s)' % (ip_details, nmScan[ip_details].hostname()))
        print('State : %s' % nmScan[ip_details].state())
        for proto in nmScan[ip_details].all_protocols():
            print('----------')
            print('Protocol : %s' % proto)
 
            lport = sorted(nmScan[ip_details][proto].keys())
            for port in lport:
                print ('port : %s\tstate : %s' % (port, nmScan[ip_details][proto][port]['state']))

def add_newvar_convertintoJson(host_subnet):
    
    print("\n\nconverting to Json, nmap scan for subnet:")    
    # initialize the port scanner
    nmScan = nmap.PortScanner()
    nmap_scan=nmScan.scan(hosts= host_subnet, arguments='-n -sP -PE -PA21,23,80,3389')
    hosts_list = [(x, nmScan[x]['status']['state'], nmScan[x]['vendor'].keys(), nmScan[x]['vendor'].values()) for x in nmScan.all_hosts()]
    #hosts_list = [x for x in nmScan.all_hosts()]
    for host, status, vendor_id, vendor_values in hosts_list:
        print(host,":",status,":",vendor_id, ":", vendor_values)
    
    for key in nmap_scan['scan']:
        nmap_scan['scan'][key]['Routing'] = {}
        nmap_scan['scan'][key]['L2 Details'] = {}
        nmap_scan['scan'][key]['L3 Details'] = {}
    
    b = json.dumps(nmap_scan)
    print(b)
    return b
    print("out from json_nmap scan function")
    #return b

def get_hostipaddress(host_subnet):
    
    # initialize the port scanner
    print("\n\nscanning host subnet to get the active hosts list:" + host_subnet)
    nmScan = nmap.PortScanner()
    a=nmScan.scan(hosts= host_subnet, arguments='-n -sP -PE -PA21,23,80,3389')
    hosts_list = nmScan.all_hosts()
    return hosts_list


def netstat_subnet(snmp_hostgateway):
#    dictzip = []
    netstat_split = snmp_hostgateway.split()
    columns = 4
    netstat_list = [netstat_split[i * columns:(i + 1) * columns] for i in range((len(netstat_split) + columns - 1) // columns)]
    print("\n\nSubnet details value:")

    activehosts = []
    final_json = []
    for i in range(2, len(netstat_list)):
#        dictzip.append(dict(zip(netstat_list[1], netstat_list[i])))
 
        testdict = dict(zip(netstat_list[1], netstat_list[i]))
        hosts_subnet=testdict.get('Destination')
        ip_details = get_hostipaddress(hosts_subnet)
        #nmScan = nmap.PortScanner()
        #nmap_scan=nmScan.scan(hosts= hosts_subnet, arguments='-n -sP -PE -PA21,23,80,3389')
        #hosts_list = [x for x in nmScan.all_hosts()]
        activehosts.append(ip_details)
        print("\n\nhostslist", ip_details)
     
        json_1 = add_newvar_convertintoJson(hosts_subnet)
        json_2 = json.loads(json_1)
        #get_allhost_details(ip_details)
        
            
        for x in ip_details:
             try:
                 #get_allhost_details(x)
                 output=os.popen("snmpnetstat -v 2c -c public -Cr " + x).read()
                 print("SNMPnetstat table " + x)
                 print(output)
                 string_split = output.split('IPv6 Routing tables (inetCidrRouteTable)', 2)
                 ipv4_table1 = string_split[0]          #Assigning to different table based on string_split output
                 ipv6_table1 = string_split[1]

                 ipv4_table = ipv4_table1.split()        # Splitting each table.
                 ipv6_table = ipv6_table1.split()
                 #print("ipv4_table", ipv4_table)
                 #print("ipv6_table", ipv6_table)
                 columns = 4                             # dividing into columns, choosed no. of columns, as we have 4 different table headers,.  
                 ipv4_list = [ipv4_table[i * columns:(i + 1) * columns] for i in range((len(ipv4_table) + columns - 1) // columns)]
                 ipv6_list = [ipv6_table[i * columns:(i + 1) * columns] for i in range((len(ipv6_table) + columns - 1) // columns)]
                 #print("\nipv4: \n")
 
                 ipv4_dict = []                         #appending to list  using dictzip  
                 for i in range(2, len(ipv4_list)):
                     ipv4_dict.append(dict(zip(ipv4_list[1], ipv4_list[i])))
                 for k in range(len(ipv4_dict)):
                     print(ipv4_dict[k])

                 ipv6_dict = []
                 for j in range(1, len(ipv6_list)):
                     ipv6_dict.append(dict(zip(ipv6_list[0], ipv6_list[j])))
                 for m in range(len(ipv6_dict)):
                     print(ipv6_dict[m])


                 json_2['scan'][x]['Routing']['ipv6'] = ipv6_dict
                 json_2['scan'][x]['Routing']['ipv4'] = ipv4_dict
             except:
                 json_2['scan'][x]['Routing']['ipv4'] = print("Timeout while trying to connect to "+x)
                 json_2['scan'][x]['Routing']['ipv6'] = print("Timeout while trying to connect to "+x)
       
        json_3 = json.dumps(json_2) 
        print(json_3)

        final_json.append(json_3)
    
    print("\n\n\nfinal json file\n", final_json) 
                
       

host_gateway = get_default_gateway_linux()
print("\n\ngateway address for current host:")
print(host_gateway)

snmp_hostgateway = snmp_check(host_gateway)
print("\n\nsnmpnetstat Ipv4 value host gateway:")
print(snmp_hostgateway)

netstat_subnet(snmp_hostgateway)

