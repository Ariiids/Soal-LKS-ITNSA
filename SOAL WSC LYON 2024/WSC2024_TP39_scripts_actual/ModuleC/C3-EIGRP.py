import netmiko, random, time, configparser

COLOR_BLUE = '\033[1;34;40m'
COLOR_GREEN = '\033[1;32;40m'
COLOR_RED = '\033[1;31;40m'
COLOR_END = '\033[0m'

config = configparser.ConfigParser()
config.read("configs.ini")
CML_USERNAME = config.get("myvars", "CML_USERNAME")
CML_PASSWORD = config.get("myvars", "CML_PASSWORD")
CML_CONTROLLER = config.get("myvars", "CML_CONTROLLER")
ENABLE_SECRET = config.get("myvars", "ENABLE_SECRET")
LAB_NAME = config.get("myvars", "LAB_NAME")

def connect(host, command_set):
    while True:
        try:
            print(COLOR_GREEN + "Result:" + COLOR_END)
            # open the Netmiko connection via the terminal server
    
            # (SSH to the controller connects to the terminal server)
            c = netmiko.ConnectHandler(device_type='terminal_server',
                        host=CML_CONTROLLER,
                        username=CML_USERNAME,
                        password=CML_PASSWORD,
                        secret=ENABLE_SECRET)
    
            # send CR, get a prompt on terminal server
            c.write_channel('\r')
    
            # open the connection to the console
            c.write_channel(f'open /{LAB_NAME}/{host}/0\r')
    
            # switch to Cisco IOS mode
            netmiko.redispatch(c, device_type='cisco_ios')

            # send command set to devices
            c.find_prompt()
            c.enable()
            result = c.send_config_set(command_set)
            print(COLOR_GREEN + result + COLOR_END)
            print('\n')
    
            break
        except:
            while True:
                value=input(COLOR_RED+"Cannot connect to console of {}. If connection is failed over and over, please, consider manual assessment about this aspect. Retry?(y/n): ".format(host)+COLOR_END)
                if value == 'y' or value == 'n':
                    break
                else:
                    print(COLOR_RED+"Invalid input! Please, try again."+COLOR_END)
            if value == 'n':
                break

print('\n')
print('########## C3 - J1 - 3.1.1 : EIGRP Named Config ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Configure an EIGRP process in HQ2 devices (IR2, CR3, CR4, DS3 and DS4) where you can enable both IPv4 and IPv6 under same EIGRP instance'+COLOR_END)
print(COLOR_BLUE+'a. You need to use the name “WSC2024” for this EIGRP configuration.'+COLOR_END)
print(COLOR_BLUE+'b. Do not enable EIGRP on interfaces connecting to CR1 and CR2 in HQ1'+COLOR_END)
print(COLOR_RED+'Look for WSC2024 name in the output and neighbour count:'+COLOR_END)
NODES = [ 'IR2', 'CR3', 'CR4', 'DS3', 'DS4' ]
command_set = [ 'do sh ip eigrp neighbors' ]
for LAB_NODE in NODES:
    print('\n')
    temp=input("Press Enter to Next Requirement:")
    print(COLOR_BLUE+'Look for WSC2024 EIGRP instance name in expected Output for '+ LAB_NODE + COLOR_END)
    match LAB_NODE:
        case "IR2":
            print(COLOR_BLUE+'EIGRP-IPv4 VR(WSC2024) Address-Family Neighbors for AS(100)'+COLOR_END)
            print(COLOR_BLUE+'H   Address                 Interface              Hold Uptime   SRTT   RTO  Q Cnt  Seq No'+COLOR_END)
            print(COLOR_BLUE+'3   10.10.0.206             Gi0/1                    xx xxx   xx   xx  0  xx'+COLOR_END)
            print(COLOR_BLUE+'2   10.10.0.210             Gi0/2                    xx xxx   xx   xx  0  xx'+COLOR_END)
            print(COLOR_BLUE+'1   172.16.100.11           Tu0                    xx xxx   xx   xx  0  xx'+COLOR_END)
            print(COLOR_BLUE+'0   172.16.100.12           Tu0                    xx xxx   xx   xx  0  xx'+COLOR_END)
        case "CR3":
            print(COLOR_BLUE+'Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd'+COLOR_END)
            print(COLOR_BLUE+'EIGRP-IPv4 VR(WSC2024) Address-Family Neighbors for AS(100)'+COLOR_END)
            print(COLOR_BLUE+'H   Address                 Interface              Hold Uptime   SRTT   RTO  Q Cnt  Seq No'+COLOR_END)
            print(COLOR_BLUE+'0   10.10.0.205             Gi0/3                   xx xxx   xx   xx  0  xx'+COLOR_END)
            print(COLOR_BLUE+'3   10.10.0.226             Gi0/2                   xx xxx   xx   xx  0  xx'+COLOR_END)
            print(COLOR_BLUE+'2   10.10.0.222             Gi0/1                   xx xxx   xx   xx  0  xx'+COLOR_END)
            print(COLOR_BLUE+'1   10.10.0.214             Gi0/0                   xx xxx   xx   xx  0  xx'+COLOR_END)
        case "CR4":
            print(COLOR_BLUE+'Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd'+COLOR_END)
            print(COLOR_BLUE+'EIGRP-IPv4 VR(WSC2024) Address-Family Neighbors for AS(100)'+COLOR_END)
            print(COLOR_BLUE+'H   Address                 Interface              Hold Uptime   SRTT   RTO  Q Cnt  Seq No'+COLOR_END)
            print(COLOR_BLUE+'0   10.10.0.209             Gi0/3                   xx xxx   xx   xx  0  xx'+COLOR_END)
            print(COLOR_BLUE+'3   10.10.0.234             Gi0/2                   xx xxx   xx   xx  0  xx'+COLOR_END)
            print(COLOR_BLUE+'2   10.10.0.230             Gi0/1                   xx xxx   xx   xx  0  xx'+COLOR_END)
            print(COLOR_BLUE+'1   10.10.0.213             Gi0/0                   xx xxx   xx   xx  0  xx'+COLOR_END)
        case "DS3":
            print(COLOR_BLUE+'Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd'+COLOR_END)
            print(COLOR_BLUE+'EIGRP-IPv4 VR(WSC2024) Address-Family Neighbors for AS(100)'+COLOR_END)
            print(COLOR_BLUE+'H   Address                 Interface              Hold Uptime   SRTT   RTO  Q Cnt  Seq No'+COLOR_END)
            print(COLOR_BLUE+'2   10.10.0.242             Vl999                   xx xxx   xx   xx  0  xx'+COLOR_END)
            print(COLOR_BLUE+'1   10.10.0.221             Gi0/0                   xx xxx   xx   xx  0  xx'+COLOR_END)
            print(COLOR_BLUE+'0   10.10.0.229             Gi0/1                   xx xxx   xx   xx  0  xx'+COLOR_END)
        case "DS4":
            print(COLOR_BLUE+'Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd'+COLOR_END)
            print(COLOR_BLUE+'EIGRP-IPv4 VR(WSC2024) Address-Family Neighbors for AS(100)'+COLOR_END)
            print(COLOR_BLUE+'H   Address                 Interface              Hold Uptime   SRTT   RTO  Q Cnt  Seq No'+COLOR_END)
            print(COLOR_BLUE+'2   10.10.0.241             Vl999                    xx xxx   xx   xx  0  xx'+COLOR_END)
            print(COLOR_BLUE+'1   10.10.0.225             Gi0/0                    xx xxx   xx   xx  0  xx'+COLOR_END)
            print(COLOR_BLUE+'0   10.10.0.233             Gi0/1                    xx xxx   xx   xx  0  xx'+COLOR_END)
    connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")

print('\n')
print('########## C3 - M1 - 3.3.2 : EIGRP Router ID ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'EIGRP for IPv4 configurations to comply with below requirement '+COLOR_END)
print(COLOR_BLUE+'a. Use autonomous system number 100.'+COLOR_END)
print(COLOR_BLUE+'b. Makesure loopback 1 IP address become EIGRP router-id'+COLOR_END)
NODES = [ 'IR2', 'CR3', 'CR4', 'DS3', 'DS4' , 'BR1', 'BR2' ]
command_set = [ 'do sh ip protocols | in eigrp 100|Router-ID' ]
for LAB_NODE in NODES:
    print('\n')
    temp=input("Press Enter to Next Requirement:")
    print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
    match LAB_NODE:
        case "IR2":
            print(COLOR_BLUE+'Routing Protocol is "eigrp 100"'+COLOR_END)
            print(COLOR_BLUE+'    Router-ID: 10.10.0.11'+COLOR_END)
        case "CR3":
            print(COLOR_BLUE+'Routing Protocol is "eigrp 100"'+COLOR_END)
            print(COLOR_BLUE+'    Router-ID: 10.10.0.12'+COLOR_END)
        case "CR4":
            print(COLOR_BLUE+'Routing Protocol is "eigrp 100"'+COLOR_END)
            print(COLOR_BLUE+'    Router-ID: 10.10.0.13'+COLOR_END)
        case "DS3":
            print(COLOR_BLUE+'Routing Protocol is "eigrp 100"'+COLOR_END)
            print(COLOR_BLUE+'    Router-ID: 10.10.0.14'+COLOR_END)
        case "DS4":
            print(COLOR_BLUE+'Routing Protocol is "eigrp 100"'+COLOR_END)
            print(COLOR_BLUE+'    Router-ID: 10.10.0.15'+COLOR_END)
        case "BR1":
            print(COLOR_BLUE+'Routing Protocol is "eigrp 100"'+COLOR_END)
            print(COLOR_BLUE+'    Router-ID: 10.10.0.21'+COLOR_END)
        case "BR2":
            print(COLOR_BLUE+'Routing Protocol is "eigrp 100"'+COLOR_END)
            print(COLOR_BLUE+'    Router-ID: 10.10.0.22'+COLOR_END)
    connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")

print('\n')
print('########## C3 - M2 - 3.3.3 : EIGRP Route Advertisement ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Advertise all loopback and /30 P2P (point-to-point/) networks into EIGRP on IR2, CR3, CR4, DS3 and DS4'+COLOR_END)
print(COLOR_BLUE+'a. Advertise vlan 100-103 networks into EIGRP in DS3 and DS4'+COLOR_END)
NODES = [ 'IR2', 'CR3', 'CR4', 'DS3', 'DS4', 'BR1', 'BR2' ]
command_set = [ 'do sh ip route eigrp | in D        10.10.0|D        10.11.10' ]
for LAB_NODE in NODES:
    print('\n')
    temp=input("Press Enter to Next Requirement:")
    print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
    match LAB_NODE:
        case "IR2":
            print(COLOR_BLUE+'D        10.10.0.12/32 '+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.13/32'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.14/32'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.15/32'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.21/32 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.22/32 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.116/30'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.136/30'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.212/30'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.220/30'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.224/30'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.228/30'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.232/30'+COLOR_END) 
            print(COLOR_BLUE+'D        10.10.0.240/30'+COLOR_END)
            print(COLOR_BLUE+'D        10.11.100.0/22'+COLOR_END)
        case "CR3":
            print(COLOR_BLUE+'D        10.10.0.11/32 '+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.13/32'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.14/32'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.15/32'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.21/32'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.22/32'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.116/30'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.208/30'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.228/30'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.232/30'+COLOR_END) 
            print(COLOR_BLUE+'D        10.10.0.240/30'+COLOR_END)
            print(COLOR_BLUE+'D        10.11.100.0/22 is a summary, xxx, Null0'+COLOR_END)
            print(COLOR_BLUE+'D        10.11.100.0/24'+COLOR_END)
            print(COLOR_BLUE+'D        10.11.101.0/24'+COLOR_END) 
            print(COLOR_BLUE+'D        10.11.102.0/24'+COLOR_END)
            print(COLOR_BLUE+'D        10.11.103.0/24'+COLOR_END)
        case "CR4":
            print(COLOR_BLUE+'D        10.10.0.11/32 '+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.12/32'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.14/32'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.15/32'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.21/32'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.22/32'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.136/30'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.204/30'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.220/30'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.224/30'+COLOR_END) 
            print(COLOR_BLUE+'D        10.10.0.240/30'+COLOR_END)
            print(COLOR_BLUE+'D        10.11.100.0/22 is a summary, xxx, Null0'+COLOR_END)
            print(COLOR_BLUE+'D        10.11.100.0/24'+COLOR_END)
            print(COLOR_BLUE+'D        10.11.101.0/24'+COLOR_END) 
            print(COLOR_BLUE+'D        10.11.102.0/24'+COLOR_END)
            print(COLOR_BLUE+'D        10.11.103.0/24'+COLOR_END)
        case "DS3":
            print(COLOR_BLUE+'D        10.10.0.11/32 '+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.12/32'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.13/32'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.15/32 xxx '+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.21/32'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.22/32'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.116/30'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.136/30'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.204/30'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.208/30'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.212/30'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.224/30 xxx'+COLOR_END) 
            print(COLOR_BLUE+'D        10.10.0.232/30 xxx'+COLOR_END)
        case "DS4":
            print(COLOR_BLUE+'D        10.10.0.11/32 '+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.12/32'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.13/32'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.14/32 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.21/32'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.22/32'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.116/30'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.136/30'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.204/30'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.208/30'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.212/30'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.220/30 xxx'+COLOR_END) 
            print(COLOR_BLUE+'D        10.10.0.228/30 xxx'+COLOR_END)
        case "BR1":
            print(COLOR_BLUE+'D        10.10.0.11/32 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.12/32 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.13/32 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.14/32 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.15/32 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.22/32 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.116/30 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.136/30 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.204/30 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.208/30 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.212/30 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.220/30 xxx'+COLOR_END) 
            print(COLOR_BLUE+'D        10.10.0.224/30 xxx'+COLOR_END) 
            print(COLOR_BLUE+'D        10.10.0.228/30 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.232/30 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.240/30 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.11.100.0/22 xxx'+COLOR_END)  
        case "BR2":
            print(COLOR_BLUE+'D        10.10.0.11/32 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.12/32 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.13/32 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.14/32 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.15/32 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.21/32 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.116/30 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.136/30 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.204/30 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.208/30 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.212/30 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.220/30 xxx'+COLOR_END) 
            print(COLOR_BLUE+'D        10.10.0.224/30 xxx'+COLOR_END) 
            print(COLOR_BLUE+'D        10.10.0.228/30 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.232/30 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.10.0.240/30 xxx'+COLOR_END)
            print(COLOR_BLUE+'D        10.11.100.0/22 xxx'+COLOR_END) 
    connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")



print('\n')
print('########## C3 - M3 - 3.3.4 : EIGRP Hello Messages Suppression ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'By default, all EIGRP hello messages should be suppressed in all interfaces'+COLOR_END)
print(COLOR_BLUE+'a. Only enable it on interfaces where EIGRP adjacencies requried.'+COLOR_END)
NODES = [ 'IR2', 'CR3', 'CR4', 'DS3', 'DS4', 'BR1', 'BR2' ]
command_set = [ 'do sh ip eigrp interfaces' ]
for LAB_NODE in NODES:
    print('\n')
    temp=input("Press Enter to Next Requirement:")
    print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
    match LAB_NODE:
        case "IR2":
            print(COLOR_BLUE+'Gi0/1                    1        0/0       0/0          xx       x/x          xx           0'+COLOR_END)
            print(COLOR_BLUE+'Gi0/2                    1        0/0       0/0          xx       x/x          xx           0'+COLOR_END)
            print(COLOR_BLUE+'Tu0                      2        0/0       0/0          xx       x/x          xx           0'+COLOR_END)
        case "CR3":
            print(COLOR_BLUE+'Gi0/0                    1        0/0       0/0          xx       x/x          xx           0'+COLOR_END)
            print(COLOR_BLUE+'Gi0/1                    1        0/0       0/0          xx       x/x          xx           0'+COLOR_END)
            print(COLOR_BLUE+'Gi0/2                    1        0/0       0/0          xx       x/x          xx           0'+COLOR_END)
            print(COLOR_BLUE+'Gi0/3                    1        0/0       0/0          xx       x/x          xx           0'+COLOR_END)
        case "CR4":
            print(COLOR_BLUE+'Gi0/0                    1        0/0       0/0          xx       x/x          xx           0'+COLOR_END)
            print(COLOR_BLUE+'Gi0/1                    1        0/0       0/0          xx       x/x          xx           0'+COLOR_END)
            print(COLOR_BLUE+'Gi0/2                    1        0/0       0/0          xx       x/x         xx           0'+COLOR_END)
            print(COLOR_BLUE+'Gi0/3                    1        0/0       0/0          xx       x/x          xx           0'+COLOR_END)
        case "DS3":
            print(COLOR_BLUE+'Gi0/0                    1        0/0       0/0          xx       x/x          xx           0'+COLOR_END)
            print(COLOR_BLUE+'Gi0/1                    1        0/0       0/0          xx       x/x          xx           0'+COLOR_END)
            print(COLOR_BLUE+'Vl999                    1        0/0       0/0          xx       x/x          xx           0'+COLOR_END)
        case "DS4":
            print(COLOR_BLUE+'Gi0/0                    1        0/0       0/0          xx       x/x          xx           0'+COLOR_END)
            print(COLOR_BLUE+'Gi0/1                    1        0/0       0/0          xx       x/x          xx           0'+COLOR_END)
            print(COLOR_BLUE+'Vl999                    1        0/0       0/0          xx       x/x          xx           0'+COLOR_END)
        case "BR1":
            print(COLOR_BLUE+'Tu0                   1        0/0       0/0          xx       x/x          xx           0'+COLOR_END) 
        case "BR2":
            print(COLOR_BLUE+'Tu0                   1        0/0       0/0          xx       x/x          xx           0'+COLOR_END)
    connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")

print('\n')
print('########## C3 - M4 - 3.3.5 : EIGRP Default Route ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'IR2 to advertise default route into EIGRP if it receives a default route from ISP1 via BGP'+COLOR_END)
print('\n')
LAB_NODE = 'IR2'
command_set = [ 'do sh ip route 0.0.0.0' ]
connect(LAB_NODE, command_set)
print(COLOR_RED+'Look for "Know via BGP 6500.3" and "Redistributing via eigrp 100" : '+COLOR_END)
print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
print(COLOR_BLUE+'Routing entry for 0.0.0.0/0, supernet'+COLOR_END)
print(COLOR_BLUE+'  Known via "bgp 65000.3", distance 20, metric 0, candidate default path'+COLOR_END)
print(COLOR_BLUE+'  Tag 4259840001, type external'+COLOR_END)
print(COLOR_BLUE+'  Redistributing via eigrp 100'+COLOR_END)
print(COLOR_BLUE+'  Advertised by eigrp 100 metric 1000000 1000 255 1 1500 route-map DEFAULT'+COLOR_END)
temp=input("Press Enter to Next Aspect:")

print('\n')
print('########## C3 - 3.3.6 : EIGRP Administrative Distance ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Modify administrative distane of external EIGRP learned route to 100 on CR3 and CR4'+COLOR_END)
NODES = [ 'CR3', 'CR4' ]
command_set = [ 'do sh ip protocols | in external ' ]
for LAB_NODE in NODES:
    print('\n')
    temp=input("Press Enter to Next Requirement:")
    print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
    match LAB_NODE:
        case "CR3":
            print(COLOR_BLUE+'      Distance: internal 90 external 100'+COLOR_END)
        case "CR4":
            print(COLOR_BLUE+'      Distance: internal 90 external 100'+COLOR_END)
    connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")

print('\n')
print('########## C3 - 3.3.7 : EIGRP Route Summary ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'On Router CR3 and CR4, summarize HQ2 vlan 100-103 subnets and advertise it via EIGRP to IR2'+COLOR_END)
NODES = [ 'IR2' ]
command_set = [ 'do sh ip route eigrp 100 | sec 10.11.100.0 ' ]
for LAB_NODE in NODES:
    print('\n')
    temp=input("Press Enter to Next Requirement:")
    print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
    match LAB_NODE:
        case "IR2":
            print(COLOR_BLUE+'D        10.11.100.0/22'+COLOR_END)
            print(COLOR_BLUE+'           [90/20480] via 10.10.0.210, xxx, GigabitEthernet0/2'+COLOR_END)
            print(COLOR_BLUE+'           [90/20480] via 10.10.0.206, xxx, GigabitEthernet0/1'+COLOR_END)
    connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")

print('\n')
print('########## C3 - 3.3.8 : EIGRP-IPv6 ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Configure EIGRP on IPv6 on HQ2 '+COLOR_END)
print(COLOR_BLUE+'a. Use same EIGRP instance WSC2024 configured in the above.'+COLOR_END)
print(COLOR_BLUE+'b. Use autonomous system number 100 for IPv6 as well.'+COLOR_END)
print(COLOR_BLUE+'c. On DS3 and DS4, IPv6 EIGRP adjacencies should not established across vlan 100,101,102 or vlan 103.'+COLOR_END)
print(COLOR_BLUE+'d. Verify you can ping IR2 loopback 1 address (2001:DB8:0:11::1/64) from HQ2-CLI1'+COLOR_END)
NODES = [  'DS3', 'DS4'  ]
command_set = [ 'do sh ipv6 eigrp neighbors' ]
for LAB_NODE in NODES:
    print('\n')
    temp=input("Press Enter to Next Requirement:")
    print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
    match LAB_NODE:
        case "DS3":
            print(COLOR_BLUE+'2   Link-local address:     Vl999               xx xxx    xx   100  0  xxx  FE80::5054:FF:FE19:83E7'+COLOR_END)
            print(COLOR_BLUE+'1   Link-local address:     Gi0/0               xx xxx    xx   100  0  xxx  FE80::5054:FF:FE13:FF62'+COLOR_END)
            print(COLOR_BLUE+'0   Link-local address:     Gi0/1               xx xxx    xx   100  0  xxx  FE80::5054:FF:FE1F:786F'+COLOR_END)
        case "DS4":
            print(COLOR_BLUE+'2   Link-local address:     Vl999               xx xxx    xx   100  0  xxx  FE80::5054:FF:FE1E:83E7'+COLOR_END)
            print(COLOR_BLUE+'1   Link-local address:     Gi0/0               xx xxx    xx   100  0  xxx  FE80::5054:FF:FE12:6161'+COLOR_END)
            print(COLOR_BLUE+'0   Link-local address:     Gi0/1               xx xxx    xx   100  0  xxx  FE80::5054:FF:FE16:E4B2'+COLOR_END)
    connect(LAB_NODE, command_set)
LAB_NODE = 'HQ2-CLI1'
print(COLOR_RED+'Evaluators: Login to '+ LAB_NODE + ' using admin/Skill39@Lyon password and check ping -6  2001:DB8:0:11::1.'+COLOR_END)
command_set = [ 'ping -6  2001:DB8:0:11::1 ' ]
print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
print(COLOR_BLUE+'ping -6  2001:DB8:0:11::1 should be successful '+ LAB_NODE + COLOR_END)
print(COLOR_BLUE+'64 bytes from 2001:db8:0:11::1: seq=0 ttl=62 time=13.053 ms'+COLOR_END)
print('\n')
temp=input(COLOR_RED+"Press Enter to End C3: "+COLOR_END)