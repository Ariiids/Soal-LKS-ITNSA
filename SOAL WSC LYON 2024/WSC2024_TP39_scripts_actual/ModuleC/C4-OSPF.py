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
print('########## C4 - J1 - 3.4.5 : OSPF Default Route ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Ensure IR1 is advertise default route to other OSPF routers if it receives a default route from ISP1. This should apper as Type 2 route with metric value of 5000'+COLOR_END)
print(COLOR_BLUE+'a. Advertise a default route into OSPF on CR4 with metric value 4000.'+COLOR_END)
print(COLOR_BLUE+'b. CR4 should inject the default route into OSPF only if 10.10.0.208/30 network (ie G 0/3 interface is up) on their routing table'+COLOR_END)
print('\n')
LAB_NODE = 'CR1'
print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
print(COLOR_BLUE+'Routing entry for 0.0.0.0/0, supernet'+COLOR_END)
print(COLOR_BLUE+' Known via "ospf 100", distance 110, metric 4000, candidate default path'+COLOR_END)
print(COLOR_BLUE+'* 10.10.0.118, from 10.10.0.13, xxx ago, via GigabitEthernet0/4 Route metric is 4000, traffic share count is 1'+COLOR_END)
print(COLOR_RED+'Evaluators:Verify metric value 4000.'+COLOR_END)
command_set = [ 'do sh ip route 0.0.0.0' ]
connect(LAB_NODE, command_set)
print('\n')
print(COLOR_RED+'Evaluators: Login to CR4 using Skill39@Lyon and shudown G0/3 interface.'+COLOR_END)
print(COLOR_RED+'Evaluators: Login to IR2 using Skill39@Lyon and shudown G0/2 interface.'+COLOR_END)
print(COLOR_RED+'Evaluators: Once both interfaces down, check again default route on CR1 to verify metric value 5000.'+COLOR_END)
temp=input("Press Enter to check default route on CR1 :")
print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
print(COLOR_BLUE+'Routing entry for 0.0.0.0/0, supernet'+COLOR_END)
print(COLOR_BLUE+' Known via "ospf 100", distance 110, metric 5000, candidate default path'+COLOR_END)
print(COLOR_BLUE+'* 10.10.0.105, from 10.10.0.1, xxx ago, via GigabitEthernet0/3 Route metric is 5000, traffic share count is 1'+COLOR_END) 
command_set = [ 'do sh ip route 0.0.0.0' ]
connect(LAB_NODE, command_set) 
print(COLOR_RED+'Evaluators: Login to CR4 using Skill39@Lyon and enable G0/3 interface.'+COLOR_END)
print(COLOR_RED+'Evaluators: Login to IR2 using Skill39@Lyon and enable G0/2 interface.'+COLOR_END)
temp=input("Press Enter to check OSPF config for default route injection on IR1 :")
LAB_NODE = 'IR1'
print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
print(COLOR_RED+'prfix-list or route-map names to filter default can be any name'+COLOR_END)
print(COLOR_BLUE+'ip prefix-list DEFAULT_PREFIX seq 5 permit 0.0.0.0/0'+COLOR_END)
print(COLOR_BLUE+'route-map INJECT_DEFAULT permit 10'+COLOR_END)
print(COLOR_BLUE+' match ip address prefix-list DEFAULT_PREFIX'+COLOR_END)
print(COLOR_BLUE+'router ospf 100'+COLOR_END)
print(COLOR_BLUE+' default-information originate metric 5000 route-map INJECT_DEFAULT'+COLOR_END)
command_set = [ 'do sh run | sec prefix-list','do sh run | sec route-map', 'do sh run | sec router ospf' ]
connect(LAB_NODE, command_set)
print('\n')
temp=input("Press Enter to check OSPF config for default route injection on CR4 :")
LAB_NODE = 'CR4'
print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
print(COLOR_RED+'prfix-list or route-map names to filter default or 10.10.0.208/30 can be any name'+COLOR_END)
print(COLOR_BLUE+'ip prefix-list DEFAULT_PREFIX seq 5 permit 0.0.0.0/0'+COLOR_END)
print(COLOR_BLUE+'ip prefix-list IR2 seq 5 permit 10.10.0.208/30'+COLOR_END)
print(COLOR_BLUE+'route-map INJECT_DEFAULT permit 10'+COLOR_END)
print(COLOR_BLUE+' match ip address prefix-list IR2'+COLOR_END)
print(COLOR_BLUE+'router ospf 100'+COLOR_END)
print(COLOR_BLUE+' default-information originate metric 4000 route-map INJECT_DEFAULT'+COLOR_END)
command_set = [ 'do sh run | sec prefix-list','do sh run | sec route-map', 'do sh run | sec router ospf' ]
connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")

print('########## C4 - M1 - 3.4.1 : OSPF Basic Config ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Configure OSPF protocol in HQ1 (IR1, CR1, CR2, DS1 and DS2 devices) to achieve the following requirements'+COLOR_END)
print(COLOR_BLUE+'a. Configure OSPF process 100 in each of those devices. Use Loopback 1 interface as router-id in each of those devices.'+COLOR_END)
NODES = [ 'IR1', 'CR1', 'CR2', 'DS1', 'DS2' ]
command_set = [ 'do sh ip ospf int lo1' ]
for LAB_NODE in NODES:
    print('\n')
    temp=input("Press Enter to Next Requirement:")
    print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
    match LAB_NODE:
        case "IR1":
            print(COLOR_BLUE+'Loopback1 is up, line protocol is up '+COLOR_END)
            print(COLOR_BLUE+'Internet Address 10.10.0.1/32, Area 0, Attached via Network Statement Process ID 100, Router ID 10.10.0.1, Network Type LOOPBACK, Cost: 1'+COLOR_END)
        case "CR1":
            print(COLOR_BLUE+'Loopback1 is up, line protocol is up '+COLOR_END)
            print(COLOR_BLUE+'Internet Address 10.10.0.2/32, Area 0, Attached via Network Statement Process ID 100, Router ID 10.10.0.2, Network Type LOOPBACK, Cost: 1'+COLOR_END)
        case "CR2":
            print(COLOR_BLUE+'Loopback1 is up, line protocol is up '+COLOR_END)
            print(COLOR_BLUE+'Internet Address 10.10.0.3/32, Area 0, Attached via Network Statement Process ID 100, Router ID 10.10.0.3, Network Type LOOPBACK, Cost: 1'+COLOR_END)
        case "DS1":
            print(COLOR_BLUE+'Loopback1 is up, line protocol is up '+COLOR_END)
            print(COLOR_BLUE+'Internet Address 10.10.0.4/32, Area 0, Attached via Network Statement Process ID 100, Router ID 10.10.0.4, Network Type LOOPBACK, Cost: 1'+COLOR_END)
        case "DS2":
            print(COLOR_BLUE+'Loopback1 is up, line protocol is up '+COLOR_END)
            print(COLOR_BLUE+'Internet Address 10.10.0.5/32, Area 0, Attached via Network Statement Process ID 100, Router ID 10.10.0.5, Network Type LOOPBACK, Cost: 1'+COLOR_END)
    connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")

print('\n')
print('########## C4 - M2 - 3.4.2 : OSPF Route Advertisement ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Advertise all /30. P2P links and Loopback 1 interfaces to OSPF area 0'+COLOR_END)
print(COLOR_BLUE+'a. DS1 and DS2, configure vlan 100-103 network in OSPF area 10.'+COLOR_END)
NODES = [ 'DS1', 'DS2' ]
command_set = [ 'do sh ip ospf int brief' ]
for LAB_NODE in NODES:
    print('\n')
    temp=input("Press Enter to Next Requirement:")
    print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
    match LAB_NODE:
        case "DS1":
            print(COLOR_BLUE+'Lo1          100   0               10.10.0.4/32       1     LOOP  0/0'+COLOR_END)
            print(COLOR_BLUE+'Vl999        100   0               10.10.0.141/30     1     P2P   1/1'+COLOR_END)
            print(COLOR_BLUE+'Gi0/1        100   0               10.10.0.130/30     1     P2P   1/1'+COLOR_END)
            print(COLOR_BLUE+'Gi0/0        100   0               10.10.0.122/30     1     P2P   1/1'+COLOR_END)
            print(COLOR_BLUE+'Vl103        100   10              10.10.103.11/24    1     DR    0/0'+COLOR_END)
            print(COLOR_BLUE+'Vl102        100   10              10.10.102.11/24    1     DR    0/0'+COLOR_END)
            print(COLOR_BLUE+'Vl101        100   10              10.10.101.11/24    1     DR    0/0'+COLOR_END)
            print(COLOR_BLUE+'Vl100        100   10              10.10.100.11/24    1     DR    0/0'+COLOR_END)
        case "DS2":
            print(COLOR_BLUE+'Lo1          100   0               10.10.0.5/32       1     LOOP  0/0'+COLOR_END)
            print(COLOR_BLUE+'Vl999        100   0               10.10.0.142/30     1     P2P   1/1'+COLOR_END)
            print(COLOR_BLUE+'Gi0/1        100   0               10.10.0.134/30     1     P2P   1/1'+COLOR_END)
            print(COLOR_BLUE+'Gi0/0        100   0               10.10.0.126/30     1     P2P   1/1'+COLOR_END)
            print(COLOR_BLUE+'Vl103        100   10              10.10.103.12/24    1     DR    0/0'+COLOR_END)
            print(COLOR_BLUE+'Vl102        100   10              10.10.102.12/24    1     DR    0/0'+COLOR_END)
            print(COLOR_BLUE+'Vl101        100   10              10.10.101.12/24    1     DR    0/0'+COLOR_END)
            print(COLOR_BLUE+'Vl100        100   10              10.10.100.12/24    1     DR    0/0'+COLOR_END)
    connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")


print('\n')
print('########## C4 - M3 - 3.4.3 : OSPF Hello Messages  ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'OSPF hello messages should be only sent via /30 networks where devices are interconnected'+COLOR_END)
NODES = [ 'IR1', 'CR1', 'CR2', 'DS1', 'DS2' ]
command_set = [ 'do sh run | sec router ospf' ]
for LAB_NODE in NODES:
    print('\n')
    temp=input("Press Enter to Next Requirement:")
    print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
    match LAB_NODE:
        case "IR1":
            print(COLOR_BLUE+'router ospf 100'+COLOR_END)
            print(COLOR_BLUE+' passive-interface default'+COLOR_END)
            print(COLOR_BLUE+' no passive-interface GigabitEthernet0/1'+COLOR_END)
            print(COLOR_BLUE+' no passive-interface GigabitEthernet0/2'+COLOR_END)
        case "CR1":
            print(COLOR_BLUE+'router ospf 100'+COLOR_END)
            print(COLOR_BLUE+' passive-interface default'+COLOR_END)
            print(COLOR_BLUE+' no passive-interface GigabitEthernet0/0'+COLOR_END)
            print(COLOR_BLUE+' no passive-interface GigabitEthernet0/1'+COLOR_END)
            print(COLOR_BLUE+' no passive-interface GigabitEthernet0/2'+COLOR_END)
            print(COLOR_BLUE+' no passive-interface GigabitEthernet0/3'+COLOR_END)
            print(COLOR_BLUE+' no passive-interface GigabitEthernet0/4'+COLOR_END)
        case "CR2":
            print(COLOR_BLUE+'router ospf 100'+COLOR_END)
            print(COLOR_BLUE+' passive-interface default'+COLOR_END)
            print(COLOR_BLUE+' no passive-interface GigabitEthernet0/0'+COLOR_END)
            print(COLOR_BLUE+' no passive-interface GigabitEthernet0/1'+COLOR_END)
            print(COLOR_BLUE+' no passive-interface GigabitEthernet0/2'+COLOR_END)
            print(COLOR_BLUE+' no passive-interface GigabitEthernet0/3'+COLOR_END)
            print(COLOR_BLUE+' no passive-interface GigabitEthernet0/4'+COLOR_END)
        case "DS1":
            print(COLOR_BLUE+'router ospf 100'+COLOR_END)
            print(COLOR_BLUE+' passive-interface default'+COLOR_END)
            print(COLOR_BLUE+' no passive-interface GigabitEthernet0/0'+COLOR_END)
            print(COLOR_BLUE+' no passive-interface GigabitEthernet0/1'+COLOR_END)
            print(COLOR_BLUE+' no passive-interface Vlan999'+COLOR_END)
        case "DS2":
            print(COLOR_BLUE+'router ospf 100'+COLOR_END)
            print(COLOR_BLUE+' passive-interface default'+COLOR_END)
            print(COLOR_BLUE+' no passive-interface GigabitEthernet0/0'+COLOR_END)
            print(COLOR_BLUE+' no passive-interface GigabitEthernet0/1'+COLOR_END)
            print(COLOR_BLUE+' no passive-interface Vlan999'+COLOR_END)
    connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")

print('\n')
print('########## C34 - M4 - 3.4.4 : OSPF No DR/BDR election ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'5.	When establish OSPF adjacencies, devices should not elect DR/BDR'+COLOR_END)
NODES = [ 'IR1', 'CR1', 'CR2', 'DS1', 'DS2' ]
command_set = [ 'do sh ip osp int brief | in P2P' ]
for LAB_NODE in NODES:
    print('\n')
    temp=input("Press Enter to Next Requirement:")
    print(COLOR_RED+'Look for P2P interface type in expected Output for '+ LAB_NODE + COLOR_END)
    match LAB_NODE:
        case "IR1":
            print(COLOR_BLUE+'Gi0/2        100   0               10.10.0.109/30     1     P2P   1/1'+COLOR_END)
            print(COLOR_BLUE+'Gi0/1        100   0               10.10.0.105/30     1     P2P   1/1'+COLOR_END)
        case "CR1":
            print(COLOR_BLUE+'Gi0/4        100   0               10.10.0.117/30     1     P2P   1/1'+COLOR_END)
            print(COLOR_BLUE+'Gi0/3        100   0               10.10.0.106/30     1     P2P   1/1'+COLOR_END)
            print(COLOR_BLUE+'Gi0/2        100   0               10.10.0.125/30     1     P2P   1/1'+COLOR_END)
            print(COLOR_BLUE+'Gi0/1        100   0               10.10.0.121/30     1     P2P   1/1'+COLOR_END)
            print(COLOR_BLUE+'Gi0/0        100   0               10.10.0.113/30     1     P2P   1/1'+COLOR_END)
        case "CR2":
            print(COLOR_BLUE+'Gi0/4        100   0               10.10.0.137/30     1     P2P   1/1'+COLOR_END)
            print(COLOR_BLUE+'Gi0/3        100   0               10.10.0.110/30     1     P2P   1/1'+COLOR_END)
            print(COLOR_BLUE+'Gi0/2        100   0               10.10.0.133/30     1     P2P   1/1'+COLOR_END)
            print(COLOR_BLUE+'Gi0/1        100   0               10.10.0.129/30     1     P2P   1/1'+COLOR_END)
            print(COLOR_BLUE+'Gi0/0        100   0               10.10.0.114/30     1     P2P   1/1'+COLOR_END)
        case "DS1":
            print(COLOR_BLUE+'Vl999        100   0               10.10.0.141/30     1     P2P   1/1'+COLOR_END)
            print(COLOR_BLUE+'Gi0/1        100   0               10.10.0.130/30     1     P2P   1/1'+COLOR_END)
            print(COLOR_BLUE+'Gi0/0        100   0               10.10.0.122/30     1     P2P   1/1'+COLOR_END)
        case "DS2":
            print(COLOR_BLUE+'Vl999        100   0               10.10.0.142/30     1     P2P   1/1'+COLOR_END)
            print(COLOR_BLUE+'Gi0/1        100   0               10.10.0.134/30     1     P2P   1/1'+COLOR_END)
            print(COLOR_BLUE+'Gi0/0        100   0               10.10.0.126/30     1     P2P   1/1'+COLOR_END)
    connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")

print('\n')
print('########## C4 - M5 - 3.4.6 : OSPF Mutual Redistribution ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Configure mutual route redistribution between EIGRP and OSPF on CR3 and CR4 so that HQ1 can access HQ2 subnets (vice-versa)'+COLOR_END)
print(COLOR_BLUE+'a. Define IP prefix lists “HQ1-SUBNETS” and “HQ2-SUBNETS” to include loopback IPs, P2P and vlan100-103 IPs in HQ1 and HQ2.'+COLOR_END)
print(COLOR_BLUE+'b. When HQ2 routes go into OSPF they should come with tag value 34.'+COLOR_END)
print(COLOR_BLUE+'c. When HQ1 routes go into EIGRP they should come with tag value 12.'+COLOR_END)
print(COLOR_BLUE+'d. Prevent any routing loops while performing mutual route-redistribution.'+COLOR_END)
print(COLOR_RED+'All routers and switches loopback should be able to ping each other to complete this task successfully'+COLOR_END)
NODES = [ 'IR1', 'IR2', 'CR1', 'CR2', 'CR3', 'CR4', 'DS1', 'DS2', 'DS3', 'DS4']
LAB_NODE = random.choice(NODES)
ADDRESSES = ['10.10.0.1', '10.10.0.2', '10.10.0.3', '10.10.0.4', '10.10.0.5', '10.10.0.11', '10.10.0.12', '10.10.0.13', '10.10.0.14', '10.10.0.15',]
for ADDRESS in ADDRESSES:
    print('\n')
    temp=input("Press Enter to ping next device's loopback :")
    command_set = [ 'do ping ' + ADDRESS +' source l1' ]
    connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")

print('\n')
print('########## C4 - M6 - 3.4.7 : OSPF Route Summarization ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Configure OSPF summary routes on ABR and ASBR routers only 10.10.100.0/22 route being advertised'+COLOR_END)
NODES = [ 'CR2' ]
command_set = [ 'do sh ip route | in 10.10.10 ' ]
for LAB_NODE in NODES:
    print('\n')
    temp=input("Press Enter to Next Requirement:")
    print(COLOR_RED+'Only 10.10.100.0/22 entry is expected for '+ LAB_NODE + COLOR_END)
    match LAB_NODE:
        case "CR2":
            print(COLOR_BLUE+'O IA     10.10.100.0/22 [110/2] via 10.10.0.134 xxx'+COLOR_END)
    connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")

print('\n')
print('########## C4 - M7 - 3.4.8 : Route Summarization from BR1 and BR2 ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Ensure that summary routes (10.1.100.0/22 and 10.2.100.0/22) and loopback addresses (10.10.0.21/32 and 10.10.0.22/32) are available on HQ1 devices OSPF routing table'+COLOR_END)
NODES = [ 'IR1', 'CR1', 'CR2', 'DS1', 'DS2' ]
LAB_NODE = random.choice(NODES)
command_set = [ 'do sh ip route | in 10.10.0.2|10.1.100.|10.2.100.' ]
connect(LAB_NODE, command_set)
print(COLOR_BLUE+'O E2     10.1.100.0/22 [110/20] via xxx ' + COLOR_END)
print(COLOR_BLUE+'O E2     10.2.100.0/22 [110/20] via xxx ' + COLOR_END)
print(COLOR_BLUE+'O E2     10.10.0.21/32 [110/20] via xxx ' + COLOR_END)
print(COLOR_BLUE+'O E2     10.10.0.22/32 [110/20] via xxx ' + COLOR_END)
print('\n')
temp=input(COLOR_RED+"Press Enter to End C4: "+COLOR_END)