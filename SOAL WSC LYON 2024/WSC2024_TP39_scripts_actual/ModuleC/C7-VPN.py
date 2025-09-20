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

print('########## C7 - J1 - 3.7.4 : SSH in IR1 and IR2  ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Enable SSH on IR1 and IR2 routers to meet requirements given below'+COLOR_END)
print(COLOR_BLUE+'a. Use most secure SSH version.'+COLOR_END)
print(COLOR_BLUE+'b. Use admin/Skill39@Lyon credential'+COLOR_END)
print(COLOR_BLUE+'c. Telnet should not be allowed when accessing network devices'+COLOR_END)
print(COLOR_BLUE+'d. In IR1 and IR2, increase SSH security by limiting SSH MAC algorithm to hmac-sha2-512 and hmac-sha2-256'+COLOR_END)
print('\n')
NODES = [ 'IR1', 'IR2' ]
command_set = [ 'do sh ip ssh' ]
for LAB_NODE in NODES:
    print('\n')
    temp=input("Press Enter to Next Requirement:")
    print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
    match LAB_NODE:
        case "IR1":
            print(COLOR_BLUE+'SSH Enabled - version 2.0'+COLOR_END)
            print(COLOR_BLUE+'MAC Algorithms:hmac-sha2-512,hmac-sha2-256'+COLOR_END)
        case "IR1":
            print(COLOR_BLUE+'SSH Enabled - version 2.0'+COLOR_END)
            print(COLOR_BLUE+'MAC Algorithms:hmac-sha2-512,hmac-sha2-256'+COLOR_END)
    connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")


print('\n')
print('########## C7 - J2 - 3.7.7 : ACL  ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Implement an ACL to block vlan 102 users in HQ1, HQ2, BR1 and BR2 to HQ1-SVR1 server'+COLOR_END)
print(COLOR_BLUE+'This should not break any previously configured access from HQ1-SVR1 to other devices'+COLOR_END)
print('\n')
print(COLOR_RED+'Make sure HQ1-SVR1 got IP address 10.10.100.101:'+COLOR_END)
print('From HQ1-SVR1:')
print('HQ1-SVR1:~$ifconfig')
temp=input("Run this command in HQ1-SVR1 and then Press Enter:")

print(COLOR_RED+'You should NOT be able to ping vlan 101 IPs (in BR1, BR2, HQ1 or HQ2) from HQ1-SVR1'+COLOR_END)
print('From HQ1-SVR1:')
print('HQ1-SVR1:~$ping 10.1.102.10')
temp=input("Run above commands in HQ1-SVR1 and make sure no success. Then Press Enter:")
print('HQ1-SVR1:~$ping 10.2.102.10')
temp=input("Run above commands in HQ1-SVR1 and make sure no success. Then Press Enter:")
print('HQ1-SVR1:~$ping 10.10.102.10')
temp=input("Run above commands in HQ1-SVR1, even ping responded it is ok (ACL may applied out direction on vlan 100). Then Press Enter:")
print('HQ1-SVR1:~$ping 10.11.102.10')
temp=input("Run above commands in HQ1-SVR1 and make sure no success. Then Press Enter:")

print(COLOR_RED+'You should be able to ping vlan 102 IPs (in BR1, BR2, HQ1 or HQ2) from HQ1-SVR1'+COLOR_END)
print('From HQ1-SVR1:')
print('HQ1-SVR1:~$ping 10.1.101.10')
print(COLOR_BLUE+'Expected Output'+COLOR_END)
print(COLOR_BLUE+'PING 10.1.101.10 (10.1.101.10): 56 data bytes'+COLOR_END)
print(COLOR_BLUE+'64 bytes from 10.1.101.10: seq=0 ttl=xxx time=xxx'+COLOR_END)
temp=input("Run above commands in HQ1-SVR1 and make sure successfull ping results. Then Press Enter:")
print('HQ1-SVR1:~$ping 10.2.101.10')
print(COLOR_BLUE+'Expected Output'+COLOR_END)
print(COLOR_BLUE+'PING 10.2.101.10 (10.2.101.10): 56 data bytes'+COLOR_END)
print(COLOR_BLUE+'64 bytes from 10.2.101.10: seq=0 ttl=xxx time=xxx'+COLOR_END)
temp=input("Run above commands in HQ1-SVR1 and make sure successfull ping results. Then Press Enter:")
print('HQ1-SVR1:~$ping 10.10.101.10')
print(COLOR_BLUE+'Expected Output'+COLOR_END)
print(COLOR_BLUE+'PING 10.10.101.10 (10.10.101.10): 56 data bytes'+COLOR_END)
print(COLOR_BLUE+'64 bytes from 10.10.101.10: seq=0 ttl=xxx time=xxx'+COLOR_END)
temp=input("Run above commands in HQ1-SVR1 and make sure successfull ping results. Then Press Enter:")
print('HQ1-SVR1:~$ping 10.11.101.10')
print(COLOR_BLUE+'Expected Output'+COLOR_END)
print(COLOR_BLUE+'PING 10.11.101.10 (10.11.101.10): 56 data bytes'+COLOR_END)
print(COLOR_BLUE+'64 bytes from 10.11.101.10: seq=0 ttl=xxx time=xxx'+COLOR_END)
temp=input("Run above commands in HQ1-SVR1 and make sure successfull ping results. Then Press Enter:")
print('\n')
temp=input("Press Enter to Next Aspect:")


print('########## C7 - M1 - 3.7.1 DMVPN HUB ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Configure IR2 as DMVPN Hub for branch sites connectivity. You require to consider below when cconfiguring IR2'+COLOR_END)
print(COLOR_BLUE+'a. Use network-id 2024.'+COLOR_END)
print(COLOR_BLUE+'b. Tunnel interface 0 to use 172.16.100.1/24 IP address'+COLOR_END)
print(COLOR_BLUE+'c. Use string WSC2024 to identify NHRP domain when establishing VPN connecivity'+COLOR_END)

LAB_NODE = 'IR2'
command_set = [ 'do sh dmvpn detail | be Inter ' ]
connect(LAB_NODE, command_set)
print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
print(COLOR_BLUE+'interface Tunnel0 is up/up, Addr. is 172.16.100.1, VRF "" '+COLOR_END)
print(COLOR_BLUE+'   Tunnel Src./Dest. addr: 192.0.2.202/Multipoint, Tunnel VRF ""'+COLOR_END)
print(COLOR_BLUE+'   Protocol/Transport: "multi-GRE/IP", Protect ""'+COLOR_END)
print(COLOR_BLUE+'   Tunnel Src./Dest. addr: 192.0.2.202/Multipoint, Tunnel VRF ""'+COLOR_END)
print(COLOR_BLUE+'Type:Hub, Total NBMA Peers (v4/v6): 2'+COLOR_END)
print(COLOR_BLUE+'# Ent  Peer NBMA Addr Peer Tunnel Add State  UpDn Tm Attrb    Target Network'+COLOR_END)
print(COLOR_BLUE+'----- --------------- --------------- ----- -------- ----- -----------------'+COLOR_END)
print(COLOR_BLUE+'1 192.0.2.2         172.16.100.11    UP xxx     D   172.16.100.11/32'+COLOR_END)
print(COLOR_BLUE+'1 192.0.2.6         172.16.100.12    UP xxx     D   172.16.100.12/32'+COLOR_END)
temp=input("Press Enter to Next Aspect:")

print('\n')
print('########## C7 - M2 - 3.7.2 DMVPN Spoke BR1/BR2 ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Configure BR1 & BR2 as DMVP Spoke sites'+COLOR_END)
print(COLOR_BLUE+'a.You are allowed to add following static routes in BR1 and BR2'+COLOR_END)
print(COLOR_BLUE+'[BR1] ip route 192.0.2.96 255.255.255.240 192.0.2.1'+COLOR_END)
print(COLOR_BLUE+'[BR1] ip route 192.0.2.192 255.255.255.240 192.0.2.1'+COLOR_END)
print(COLOR_BLUE+'[BR2] ip route 192.0.2.96 255.255.255.240 192.0.2.5'+COLOR_END)
print(COLOR_BLUE+'[BR2] ip route 192.0.2.192 255.255.255.240 192.0.2.5'+COLOR_END)
print(COLOR_BLUE+'b.BR1 tunnel interface 0 to use 172.16.100.11/24 IP address'+COLOR_END)
print(COLOR_BLUE+'c.BR2 tunnel interface 0 to use 172.16.100.12/24 IP address'+COLOR_END)
print(COLOR_BLUE+'d.BR1 and BR2 should establish dynamic tunnel between then when communicating each other'+COLOR_END)
print('\n')
print(COLOR_RED+'Go to BR1 console and issue "ping 10.10.0.22 source loopback 1"- Before hit Enter'+COLOR_END)
NODES = [ 'IR2', 'BR1', 'BR2' ]
command_set = [ 'do sh dmvpn | be Inter' ]
for LAB_NODE in NODES:
    print('\n')
    temp=input("Press Enter to Next Requirement:")
    print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
    match LAB_NODE:
        case "IR2":
            print(COLOR_BLUE+' # Ent  Peer NBMA Addr Peer Tunnel Add State  UpDn Tm Attrb'+COLOR_END)
            print(COLOR_BLUE+' ----- --------------- --------------- ----- -------- -----'+COLOR_END)
            print(COLOR_BLUE+'     1 192.0.2.2         172.16.100.11    UP xxx     D'+COLOR_END)
            print(COLOR_BLUE+'     1 192.0.2.6         172.16.100.12    UP xxx     D'+COLOR_END)
        case "BR1":
            print(COLOR_BLUE+' # Ent  Peer NBMA Addr Peer Tunnel Add State  UpDn Tm Attrb'+COLOR_END)
            print(COLOR_BLUE+' ----- --------------- --------------- ----- -------- -----'+COLOR_END)
            print(COLOR_BLUE+'     1 192.0.2.202       172.16.100.1     UP xxx     S'+COLOR_END)
            print(COLOR_BLUE+'     1 192.0.2.6         172.16.100.12    UP xxx     D'+COLOR_END)
        case "BR2":
            print(COLOR_BLUE+' # Ent  Peer NBMA Addr Peer Tunnel Add State  UpDn Tm Attrb'+COLOR_END)
            print(COLOR_BLUE+' ----- --------------- --------------- ----- -------- -----'+COLOR_END)
            print(COLOR_BLUE+'     1 192.0.2.202       172.16.100.1     UP xxx     S'+COLOR_END)
            print(COLOR_BLUE+'     1 192.0.2.2         172.16.100.11    UP xxx     D'+COLOR_END)
    connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")

print('\n')
print('########## C7 - M3 - 3.7.3 EIGRP Summary Route - BR1/BR2 ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Configure EIGRP between BR1, BR2 and IR2'+COLOR_END)
print(COLOR_BLUE+'a. BR1 and BR2 to advertise a summary route for networks corresponds to vlan 100-103 networks at that site'+COLOR_END)
NODES = [ 'IR2' ]
command_set = [ 'do sh ip route | in 10.1.10', 'do sh ip route | in 10.2.10' ]
for LAB_NODE in NODES:
    print('\n')
    temp=input("Press Enter to Next Requirement:")
    print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
    match LAB_NODE:
        case "IR2":
            print(COLOR_BLUE+'D        10.1.100.0/22 [90/76805120] via 172.16.100.11, xx, Tunnel0'+COLOR_END)
            print(COLOR_BLUE+'D        10.2.100.0/22 [90/76805120] via 172.16.100.11, xx, Tunnel0'+COLOR_END)
    connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")

print('\n')
print('########## C7 - M4 - 3.7.5 SSH VTY ACL ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Limit only HQ1-SVR1(10.10.100.101/24) can SSH into IR1 and IR2'+COLOR_END)
print('\n')
print(COLOR_RED+':Login to HQ1-SVR1 and SSH into IR1 and IR2'+COLOR_END)
print('From HQ1-SVR1:')
print('# ssh -l admin 10.10.0.1')
print('# ssh -l admin 10.10.0.11')
print('\n')
temp=input("Press Enter to Next Requirement:")
print(COLOR_BLUE+'# Excpeted Output : Are you sure you want to continue connecting (yes/no/[fingerprint])? yes'+COLOR_END)
print(COLOR_BLUE+'# Warning: Permanently added 10.10.0.1 (RSA) to the list of known hosts. '+COLOR_END)
print(COLOR_BLUE+'Password: '+COLOR_END)
print(COLOR_BLUE+'IR1# '+COLOR_END)
print(COLOR_RED+'This message also accptable - Unable to negotiate with 10.10.0.1 port 22: no matching key exchange method found: '+COLOR_END)
print('\n')
temp=input("Press Enter to Next Requirement:")
print(COLOR_RED+':Login to HQ1-CLI1 and SSH into IR1 and IR2'+COLOR_END)
print('From HQ1-CLI1:')
print('# ssh -l admin 10.10.0.1')
print('# ssh -l admin 10.10.0.11')
print('\n')
temp=input("Press Enter to Next Requirement:")
print(COLOR_BLUE+'# Excpeted Output : ssh: connect to host 10.10.0.1 port 22: Connection refused'+COLOR_END)
temp=input("Press Enter to Next Aspect:")


print('\n')
print('########## C7 - M5 - 3.7.6 Port Security ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Enable port security on HQ1-CLI and HQ2-CLI1 connected switchports. There is a plan to deploy VOIP handsets in HQ1 and HQ2 on vlan 150. You can define VLAN150 (named VOIP) on AS1 and AS2 for this task'+COLOR_END)
print(COLOR_BLUE+'a. Limit the mac addreses to minimum required if those PCs go behind VOIP phone.'+COLOR_END)
print(COLOR_BLUE+'b. In case of port security violation, port should be disabled and syslog message to be generated.'+COLOR_END)
print(COLOR_BLUE+'c. Port should be automatically recovered in 3 minutes.'+COLOR_END)
NODES = [ 'AS1', 'AS2' ]
command_set = [ 'do show port-security interface g0/0', 'do sh errdisable recovery | inc security-violation', 'do sh errdisable recovery | inc Timer interval' ]
for LAB_NODE in NODES:
    print('\n')
    temp=input("Press Enter to Next Requirement:")
    print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
    match LAB_NODE:
        case "AS1":
            print(COLOR_BLUE+'AS1#sh port-security interface g0/0'+COLOR_END)
            print(COLOR_BLUE+'Port Security              : Enabled'+COLOR_END)
            print(COLOR_BLUE+'Violation Mode             : Shutdown'+COLOR_END)
            print(COLOR_BLUE+'Maximum MAC Addresses      : 2'+COLOR_END)
            print(COLOR_BLUE+'AS1#sh errdisable recovery | inc security-violation'+COLOR_END)
            print(COLOR_BLUE+'security-violation           Enabled'+COLOR_END)
            print(COLOR_BLUE+'AS1#sh errdisable recovery | inc Timer interval'+COLOR_END)
            print(COLOR_BLUE+'Timer interval: 180 seconds'+COLOR_END)
        case "AS2":
            print(COLOR_BLUE+'AS2#sh port-security interface g0/0'+COLOR_END)
            print(COLOR_BLUE+'Port Security              : Enabled'+COLOR_END)
            print(COLOR_BLUE+'Violation Mode             : Shutdown'+COLOR_END)
            print(COLOR_BLUE+'Maximum MAC Addresses      : 2'+COLOR_END)
            print(COLOR_BLUE+'AS2#sh errdisable recovery | inc security-violation'+COLOR_END)
            print(COLOR_BLUE+'security-violation           Enabled'+COLOR_END)
            print(COLOR_BLUE+'AS2#sh errdisable recovery | inc Timer interval'+COLOR_END)
            print(COLOR_BLUE+'Timer interval: 180 seconds'+COLOR_END)
    connect(LAB_NODE, command_set)
print('\n')
temp=input(COLOR_RED+"Press Enter to End C7: "+COLOR_END)