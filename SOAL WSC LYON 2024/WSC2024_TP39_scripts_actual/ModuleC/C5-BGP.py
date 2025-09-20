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
print('########## C5 - M1 - 3.5.1 : eBGP-Basic Config ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Configure eBGP sessions on IR1 and IR2 (both in AS#6500.3) with ISP router G0/1 and G0/2 IPs (192.0.2.101 and 192.0.2.201 IPs)'+COLOR_END)
print(COLOR_BLUE+'a. Keepalive interval 10s and Holddown time of 30s.'+COLOR_END)
print(COLOR_BLUE+'b. Authentication password Skill39@Lyon'+COLOR_END)
NODES = [ 'IR1', 'IR2' ]
command_set = [ 'do sh ip bgp su | be Nei' ]
for LAB_NODE in NODES:
    print('\n')
    temp=input("Press Enter to Next Requirement:")
    print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
    match LAB_NODE:
        case "IR1":
            print(COLOR_BLUE+'Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd'+COLOR_END)
            print(COLOR_BLUE+'192.0.2.101     4      65000.1     xxx     xxx       xx    0    0 xxx        3'+COLOR_END)
        case "IR2":
            print(COLOR_BLUE+'Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd'+COLOR_END)
            print(COLOR_BLUE+'192.0.2.201     4      65000.1     xxx     xxx       xx    0    0 xxx        3'+COLOR_END)
    connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")

print('\n')
print('########## C5 - M2 - 3.5.2 : iBGP-Peer Group ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Configure an iBGP peer group named “WSC2024” on on IR1 and IR2 to establish iBGP peering among themselves. It requires following settings'+COLOR_END)
print(COLOR_BLUE+'a. Keepalive interval 10s and Holddown time of 30s.'+COLOR_END)
print(COLOR_BLUE+'b. Authenticate each iBGP sessions with password  Skill39@Lyon'+COLOR_END)
print(COLOR_BLUE+'c. BGP peering to use loopback1 interface IP'+COLOR_END)
NODES = [ 'IR1', 'IR2' ]
command_set = [ 'do sh ip bgp su | be Nei' ]
for LAB_NODE in NODES:
    print('\n')
    temp=input("Press Enter to Next Requirement:")
    print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
    match LAB_NODE:
        case "IR1":
            print(COLOR_BLUE+'Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd'+COLOR_END)
            print(COLOR_BLUE+'10.10.0.11      4      65000.3     xxx     xxx       xx    0    0 xxx        3'+COLOR_END)
        case "IR2":
            print(COLOR_BLUE+'Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd'+COLOR_END)
            print(COLOR_BLUE+'10.10.0.1       4      65000.3     xxx     xxx       xx    0    0 xxx        4'+COLOR_END)
    connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")

print('\n')
print('########## C5 - M3 - 3.5.3 : BGP Route Advertisement ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Advertise 10.10.100.0/22 and 10.11.100.0/22 routes into BGP on IR1 and IR2'+COLOR_END)
print(COLOR_BLUE+'a. ISP should not receive any accidental routes from IR1 or IR2 other than above summary routes.'+COLOR_END)
print(COLOR_BLUE+'b. Use a route-map named ISPV4_EXPORT to control it.'+COLOR_END)
LAB_NODE = 'IR1'
command_set = [ 'do sh ip bgp neighbors 192.0.2.101 advertised-routes | beg Network' ]
print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
print(COLOR_BLUE+'     Network          Next Hop            Metric LocPrf Weight Path'+COLOR_END)
print(COLOR_BLUE+' *>   10.10.100.0/22   10.10.0.110             xx         32768 i'+COLOR_END)
print(COLOR_BLUE+' *>   10.11.100.0/22   10.10.0.110             xx         32768 i'+COLOR_END)
connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Requirement:")

LAB_NODE = 'IR2'
command_set = [ 'do sh ip bgp neighbors 192.0.2.201 advertised-routes | beg Network' ]
print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
print(COLOR_BLUE+'     Network          Next Hop            Metric LocPrf Weight Path'+COLOR_END)
print(COLOR_BLUE+' *>   10.10.100.0/22   10.10.0.206             xx         32768 i'+COLOR_END)
print(COLOR_BLUE+' *>   10.11.100.0/22   10.10.0.210             xx         32768 i'+COLOR_END)
connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")


print('\n')
print('########## C5 - M4 - 3.5.4 : BGP Path Attributes-Local Preference ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Configure BGP on IR1 and IR2 such a way all internet traffic is going out via IR2 as primary path and only go via IR1 in case of a failure in the primary path'+COLOR_END)
print(COLOR_BLUE+'a. Use “local preference” BGP attribute to achieve this task.'+COLOR_END)
LAB_NODE = 'IR2'
command_set = [ 'do sh ip bgp ' ]
connect(LAB_NODE, command_set)
print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
print(COLOR_BLUE+'IR2 should have higher (>100) local preference when it received routes from ISP1 and default BGP routes exit via 192.0.2.201 '+ LAB_NODE + COLOR_END)
print(COLOR_BLUE+'     Network          Next Hop            Metric LocPrf Weight Path'+COLOR_END)
print(COLOR_BLUE+' *>   0.0.0.0          192.0.2.201              0    200      0 65000.1 7575 15169 i'+COLOR_END)
temp=input("Press Enter to Next Aspect:")

print('\n')
print('########## C5 - M5 - 3.5.5 : BGP Path Attributes-MED ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Configure BGP on IR1 and IR2 such a way all incoming internet traffic come via IR2 as primary path and come via IR1 in case of a failure in the primary path'+COLOR_END)
print(COLOR_BLUE+'a.ISP1 will not accept any routes that got “AS-PATH” prepending. Therefore, use another BGP attribute to achieve this task.'+COLOR_END)

print(COLOR_RED+'Evaluators: Login to ISP1 using Skill39Admin@Lyon password and issue "sh bgp | beg Network" and compare it with below output. '+COLOR_END) 

print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
print(COLOR_BLUE+'MED value to be lower from IR2 compare to IR1. Default MED value is 0. Even competitor only use higher MED value from IR1 (keeping default at IR2) is achieving the same outcome. On ISP1 router compare the MED values coming from IR1 and IR2'+ LAB_NODE + COLOR_END)
print(COLOR_BLUE+'     Network          Next Hop            Metric LocPrf Weight Path'+COLOR_END)
print(COLOR_BLUE+' *>   10.10.100.0/22   192.0.2.202            200             0 65000.3 i'+COLOR_END)
print(COLOR_BLUE+' *>   10.11.100.0/22   192.0.2.202            200             0 65000.3 i'+COLOR_END)
temp=input("Press Enter to Next Aspect:")

print('\n')
print('########## C5 - 3.5.6 : BGP Route Redistribution ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'On IR1 and IR2, you receive prefixes 198.51.100.0/24 and 203.0.113.0/24 from ISP1. You are required to configure IR1 as primary path (incoming and outgoing) for reaching to these prefixes from HQ1 and HQ2'+COLOR_END)
print(COLOR_BLUE+'a.You can use “198.51.100.1” and “203.0.113.1” IP addresses for reachability testing (ping and traceroute) from HQ-CLI1 and HQ2-CLI1'+COLOR_END)

NODES = [ 'HQ1-CLI1', 'HQ2-CLI1' ]
command_set = [ 'do ping 198.51.100.1' ]
for LAB_NODE in NODES:
    print('\n')
    temp=input("Press Enter to Next Requirement:")
    print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
    match LAB_NODE:
        case "HQ1-CLI1":
            print(COLOR_BLUE+'ping 198.51.100.1 (198.51.100.1): 56 data bytes'+COLOR_END)
            print(COLOR_BLUE+'64 bytes from 198.51.100.1: seq=0 ttl=42 time=xxx ms  *'+COLOR_END)
        case "HQ2-CLI1":
            print(COLOR_BLUE+'ping 198.51.100.1 (198.51.100.1): 56 data bytes'+COLOR_END)
            print(COLOR_BLUE+'64 bytes from 198.51.100.1: seq=0 ttl=42 time=xxx ms  *'+COLOR_END)
    print(COLOR_RED+'Evaluators: Login to '+ LAB_NODE + ' using admin/Skill39@Lyon password and check above output manually.'+COLOR_END)
temp=input("Press Enter to Next Requirement:")
NODES = [ 'HQ1-CLI1', 'HQ2-CLI1' ]
command_set = [ 'do traceroute 198.51.100.1' ]
for LAB_NODE in NODES:
    print('\n')
    temp=input("Press Enter to Next Requirement:")
    print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
    match LAB_NODE:
        case "HQ1-CLI1":
            print(COLOR_BLUE+'traceroute to 198.51.100.1 (198.51.100.1), 30 hops max, 46 byte packets'+COLOR_END)
            print(COLOR_BLUE+'1  10.10.101.11 (10.10.101.11)  xxx ms  xxx ms  xxx ms'+COLOR_END)
            print(COLOR_BLUE+'2  10.10.0.121 (10.10.0.121)  xxx ms  xxx ms  xxx ms'+COLOR_END)
            print(COLOR_BLUE+'3  10.10.0.105 (10.10.0.105)  xxx ms  xxx ms  xxx ms'+COLOR_END)
            print(COLOR_BLUE+'4  192.0.2.101 (192.0.2.101)  xxx ms  xxx ms  xxx ms'+COLOR_END)
        case "HQ2-CLI1":
            print(COLOR_BLUE+'traceroute to 198.51.100.1 (198.51.100.1), 30 hops max, 46 byte packets'+COLOR_END)
            print(COLOR_BLUE+'1  10.11.102.11 (10.11.102.11)  xxx ms  xxx ms  xxx ms'+COLOR_END)
            print(COLOR_BLUE+'2  10.10.0.221 (10.10.0.221)  xxx ms  xxx ms  xxx ms'+COLOR_END)
            print(COLOR_BLUE+'3  10.10.0.137 (10.10.0.137) xxx ms  xxx ms  xxx ms'+COLOR_END)
            print(COLOR_BLUE+'4  10.10.0.109 (10.10.0.109)  xxx ms  xxx ms  xxx ms'+COLOR_END)
            print(COLOR_BLUE+'5  192.0.2.101 (192.0.2.101))  xxx ms  xxx ms  xxx ms'+COLOR_END)
    print(COLOR_RED+'Evaluators: Login to '+ LAB_NODE + ' using admin/Skill39@Lyon password and check above output manually.'+COLOR_END)
temp=input("Press Enter to Next Aspect:")
print('\n')
print('########## C5 - 3.5.7 : BGP Failover ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Verifiy internet traffic is working in a scenario of failing primary internet router IR2'+COLOR_END)
print(COLOR_BLUE+'a. Simulate a failure of IR2 by shutting down G 0/3 interfaces of CR3 and CR4'+COLOR_END)
print(COLOR_BLUE+'b. Ping 8.8.8.8 from HQ1-CLI1 and ensure that it is successful. Traceroute output should confirm traffic go via IR1'+COLOR_END)
print(COLOR_BLUE+'c. Ping 8.8.8.8 from HQ2-CLI1 and ensure that it is successful. Traceroute output should confirm traffic go via IR1'+COLOR_END)
print(COLOR_RED+'Evaluators: Login to CR3 and CR4 using admin/Skill39@Lyon password and shutdown G0/3 interface before this evaluation.'+COLOR_END)
NODES = [ 'HQ1-CLI1', 'HQ2-CLI1' ]
command_set = [ 'do ping 198.51.100.1' ]
for LAB_NODE in NODES:
    print('\n')
    temp=input("Press Enter to Next Requirement:")
    print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
    match LAB_NODE:
        case "HQ1-CLI1":
            print(COLOR_BLUE+'traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 46 byte packets'+COLOR_END)
            print(COLOR_BLUE+' 1  10.10.101.11 (10.10.101.11) xxx ms  xxx ms  xxx ms'+COLOR_END)
            print(COLOR_BLUE+' 2  10.10.0.129 (10.10.0.129)   xxx ms  xxx ms  xxx ms'+COLOR_END)
            print(COLOR_BLUE+' 3  10.10.0.109 (10.10.0.109)   xxx ms  xxx ms  xxx ms'+COLOR_END)
            print(COLOR_BLUE+' 4  192.0.2.101 (192.0.2.101)   xxx ms  xxx ms  xxx ms'+COLOR_END)
        case "HQ2-CLI1":
            print(COLOR_BLUE+'traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 46 byte packets'+COLOR_END)
            print(COLOR_BLUE+' 1  10.10.101.11 (10.10.101.11) xxx ms  xxx ms  xxx ms'+COLOR_END)
            print(COLOR_BLUE+' 2  10.10.0.142 (10.10.0.142)   xxx ms  xxx ms  xxx ms'+COLOR_END)
            print(COLOR_BLUE+' 3  10.10.0.125 (10.10.0.125)   xxx ms  xxx ms  xxx ms'+COLOR_END)
            print(COLOR_BLUE+' 4  10.10.0.105 (10.10.0.105)   xxx ms  xxx ms  xxx ms'+COLOR_END)
            print(COLOR_BLUE+' 5  192.0.2.101 (192.0.2.101)   xxx ms  xxx ms  xxx ms'+COLOR_END)
    print(COLOR_RED+'Evaluators: Login to '+ LAB_NODE + ' using admin/Skill39@Lyon password and check above output manually.'+COLOR_END)
temp=input("Press Enter to Next Requirement:")
print(COLOR_RED+'Evaluators: Login to CR3 and CR4 using admin/Skill39@Lyon password and enable G0/3 interface before move forward.'+COLOR_END)
temp=input(COLOR_RED+"Press Enter to End C5: "+COLOR_END)