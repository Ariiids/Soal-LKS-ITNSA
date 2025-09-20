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
            # print('\n')
    
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
print('########## C2 - J1 - 3.2.3: STP ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'STP is configured as per requirement:'+COLOR_END)
print(COLOR_BLUE+'a. In HQ1, DS1 should be the STP root bridge for all vlans (including future vlans) and DS2 should become the root bridge if DS1 is down.'+COLOR_END)
print(COLOR_BLUE+'b. In HQ2, DS3 should be the STP root bridge for all vlans (including future vlans) and DS4 should become the root bridge if DS3 is down.'+COLOR_END)
print(COLOR_BLUE+'c. These STP convergences require to happen as quickly as possible. Choose the right STP mode to achieve that outcome.'+COLOR_END)
NODES = [ 'DS1', 'DS2', 'DS3', 'DS4' ]
command_set = [ 'do sh spanning-tree summary | i Switch is|Root' ]
for LAB_NODE in NODES:
    print('\n')
    temp=input("Press Enter to continue:")
    print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
    match LAB_NODE:
        case "DS1":
            print(COLOR_BLUE+'Switch is in rapid-pvst mode'+COLOR_END)
            print(COLOR_BLUE+'Root bridge for: VLAN0001, VLAN0100-VLAN0103, VLAN0999'+COLOR_END)
        case "DS2":
            print(COLOR_BLUE+'Switch is in rapid-pvst mode'+COLOR_END)
            print(COLOR_BLUE+'Root bridge for: none'+COLOR_END)
        case "DS3":
            print(COLOR_BLUE+'Switch is in rapid-pvst mode'+COLOR_END)
            print(COLOR_BLUE+'Root bridge for: VLAN0001, VLAN0100-VLAN0103, VLAN0999'+COLOR_END)
        case "DS4":
            print(COLOR_BLUE+'Switch is in rapid-pvst mode'+COLOR_END)
            print(COLOR_BLUE+'Root bridge for: none'+COLOR_END)
    connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")

###
print('\n')
print('########## C2 - J2 - 3.2.7: HSRP-IPv4 ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'HSRP for the 4 vlans (100-103) have been configured with the following requirements on DS1-DS4:'+COLOR_END)
print(COLOR_BLUE+'a. Default gateway IP address is ended with .10 in each /24 vlan.'+COLOR_END)
print(COLOR_BLUE+'b. Vlan number is used as HSRP group.'+COLOR_END)
print(COLOR_BLUE+'c. DS1 should be the HSRP active for HQ1 and DS3 should be the HSRP active for HQ2.'+COLOR_END)
print(COLOR_BLUE+'d. In case of active device (DS1 or DS3) goes down DS2 or DS4 should act as active device in each site. When DS1 or DS3 comes back after failure, it shoud take over HSRP active role once it is operational.'+COLOR_END)
print(COLOR_BLUE+'You can use ""show standby brief"" CLI output for verification, P indicates configured to preempt.'+COLOR_END)
print(COLOR_RED+'Look for Priority value and "P" for Premption in the output:'+COLOR_END)
NODES = [ 'DS1', 'DS2', 'DS3', 'DS4' ]
command_set = [ 'do sh standby brief | ex FE80' ]
for LAB_NODE in NODES:
    print('\n')
    temp=input("Press Enter to continue:")
    print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
    match LAB_NODE:
        case "DS1":
            print(COLOR_BLUE+'Interface   Grp  Pri P State   Active          Standby         Virtual IP'+COLOR_END)
            print(COLOR_BLUE+'Vl100       100  110 P Active  local           10.10.100.12    10.10.100.10'+COLOR_END)
            print(COLOR_BLUE+'Vl101       101  110 P Active  local           10.10.101.12    10.10.101.10'+COLOR_END)
            print(COLOR_BLUE+'Vl102       102  110 P Active  local           10.10.102.12    10.10.102.10'+COLOR_END)
            print(COLOR_BLUE+'Vl103       103  110 P Active  local           10.10.103.12    10.10.103.10'+COLOR_END)
        case "DS2":
            print(COLOR_BLUE+'Interface   Grp  Pri P State   Active          Standby         Virtual IP'+COLOR_END)
            print(COLOR_BLUE+'Vl100       100  100   Standby 10.10.100.11    local           10.10.100.10'+COLOR_END)
            print(COLOR_BLUE+'Vl101       101  100   Standby 10.10.101.11    local           10.10.101.10'+COLOR_END)
            print(COLOR_BLUE+'Vl102       102  100   Standby 10.10.102.11    local           10.10.102.10'+COLOR_END)
            print(COLOR_BLUE+'Vl103       103  100   Standby 10.10.103.11    local           10.10.103.10'+COLOR_END)
        case "DS3":
            print(COLOR_BLUE+'Interface   Grp  Pri P State   Active          Standby         Virtual IP'+COLOR_END)
            print(COLOR_BLUE+'Vl100       100  110 P Active  local           10.11.100.12    10.11.100.10'+COLOR_END)
            print(COLOR_BLUE+'Vl101       101  110 P Active  local           10.11.101.12    10.11.101.10'+COLOR_END)
            print(COLOR_BLUE+'Vl102       102  110 P Active  local           10.11.102.12    10.11.102.10'+COLOR_END)
            print(COLOR_BLUE+'Vl103       103  110 P Active  local           10.11.103.12    10.11.103.10'+COLOR_END)
        case "DS4":
            print(COLOR_BLUE+'Interface   Grp  Pri P State   Active          Standby         Virtual IP'+COLOR_END)
            print(COLOR_BLUE+'Vl100       100  100   Standby 10.11.100.11    local           10.11.100.10'+COLOR_END)
            print(COLOR_BLUE+'Vl101       101  100   Standby 10.11.101.11    local           10.11.101.10'+COLOR_END)
            print(COLOR_BLUE+'Vl102       102  100   Standby 10.11.102.11    local           10.11.102.10'+COLOR_END)
            print(COLOR_BLUE+'Vl103       103  100   Standby 10.11.103.11    local           10.11.103.10'+COLOR_END)
    connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")

print('\n')
print('########## C2 - M1 - 3.2.1: VTP - Configuration ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'VTP Domain Name                 : WSC2024'+COLOR_END)
print(COLOR_BLUE+'VTP Operating Mode                : Off'+COLOR_END)
NODES = [ 'DS1', 'DS2', 'DS3', 'DS4', 'AS1', 'AS2', 'AS3', 'AS4' ]
LAB_NODE = random.choice(NODES)
command_set = [ 'do sh vtp status | i Domain|Operating' ]
connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")

print('\n')
print('########## C2 - M2 - 3.2.2: VLAN Configuration ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Randomly choose one IOS device from from AS1-4, check vlan 100-103 are configured with correct Name.'+COLOR_END)
print(COLOR_BLUE+'ASx#sh vlan brief | ex default'+COLOR_END)
print(COLOR_BLUE+'VLAN Name                             Status    Ports'+COLOR_END)
print(COLOR_BLUE+'---- -------------------------------- --------- -------------------------------'+COLOR_END)
print(COLOR_BLUE+'100  SERVER                           active    xxxx'+COLOR_END)
print(COLOR_BLUE+'101  CLIENT_1                         active    xxxx'+COLOR_END)
print(COLOR_BLUE+'102  CLIENT_2                         active    xxxx'+COLOR_END)
print(COLOR_BLUE+'103  MGMT                             active    xxxx'+COLOR_END)
print(COLOR_BLUE+'150  VOIP                             active    xxxx'+COLOR_END)
temp=input("Press Enter to continue:")
NODES = [ 'AS1', 'AS2', 'AS3', 'AS4' ]
LAB_NODE = random.choice(NODES)
command_set = [ 'do sh vlan brief | ex default' ]
connect(LAB_NODE, command_set)
temp=input("Press Enter to continue:")

print(COLOR_BLUE+'Randomly choose one IOS device from from DS1-4, check vlan 100-103, 999 are configured with correct Name.'+COLOR_END)
print(COLOR_BLUE+'DSx#sh vlan brief | ex default'+COLOR_END)
print(COLOR_BLUE+'VLAN Name                             Status    Ports'+COLOR_END)
print(COLOR_BLUE+'---- -------------------------------- --------- -------------------------'+COLOR_END)
print(COLOR_BLUE+'100  SERVER                           active    xxxx'+COLOR_END)
print(COLOR_BLUE+'101  CLIENT_1                         active    xxxx'+COLOR_END)
print(COLOR_BLUE+'102  CLIENT_2                         active    xxxx'+COLOR_END)
print(COLOR_BLUE+'103  MGMT                             active    xxxx'+COLOR_END)
print(COLOR_BLUE+'999  L3_P2P                           active    xxxx'+COLOR_END)
temp=input("Press Enter to continue:")
NODES = [ 'DS1', 'DS2', 'DS3', 'DS4' ]
LAB_NODE = random.choice(NODES)
command_set = [ 'do sh vlan brief | ex default' ]
connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")

print('\n')
print('########## C2 - M3 - 3.2.4: 802.1Q Trunk ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Verify G0/3 interface on DS1-DS4 are trunk ports with native vlan 888'+COLOR_END)
print(COLOR_BLUE+'Verify G0/1 and G0/2 of AS1-AS2 are trunk ports with native vlan 888'+COLOR_END)
print(COLOR_BLUE+'Verify G0/0 of AS3-AS4 are trunk ports with native vlan 1'+COLOR_END)


command_set = [ 'do sh int trunk' ]
print('\n')
NODES = [ 'DS1', 'DS2', 'DS3', 'DS4']
print(COLOR_BLUE+'Expected Output for DS1-DS4:'+ COLOR_END)
print(COLOR_BLUE+'Type "sh int trunk" on DS1-DS4, the output show Gi0/3 is in 802.1Q with Native vlan of 888:'+ COLOR_END)
print(COLOR_BLUE+'Port        Mode             Encapsulation  Status        Native vlan'+ COLOR_END)
print(COLOR_BLUE+'Gi0/3       on               802.1q         trunking      888'+ COLOR_END)
print(COLOR_RED+'Look for "Mode = on" and Native vlan value of 888":'+COLOR_END)
for LAB_NODE in NODES:
    temp=input("Press Enter to continue:")
    connect(LAB_NODE, command_set)

print('\n')
NODES = [ 'AS1', 'AS2' ]
print(COLOR_BLUE+'Expected Output for AS1-AS2:'+ COLOR_END)
print(COLOR_BLUE+'Type "sh int trunk" on AS1-AS2, the output show Gi0/1 and Gi0/2 are in 802.1Q with Native vlan of 888:'+ COLOR_END)
print(COLOR_BLUE+'Port        Mode             Encapsulation  Status        Native vlan'+ COLOR_END)
print(COLOR_BLUE+'Gi0/1       on               802.1q         trunking      888'+ COLOR_END)
print(COLOR_BLUE+'Gi0/2       on               802.1q         trunking      888'+ COLOR_END)
for LAB_NODE in NODES:
    temp=input("Press Enter to continue:")    
    connect(LAB_NODE, command_set)

print('\n')
NODES = [ 'AS3', 'AS4' ]
print(COLOR_BLUE+'Expected Output for AS3-AS4:'+ COLOR_END)
print(COLOR_BLUE+'Type "sh int trunk" on AS3-AS4, the output show Gi0/0 is in 802.1Q with Native vlan of 1:'+ COLOR_END)
print(COLOR_BLUE+'Port        Mode             Encapsulation  Status        Native vlan'+ COLOR_END)
print(COLOR_BLUE+'Gi0/0       on               802.1q         trunking      1'+ COLOR_END)
print(COLOR_RED+'Look for "Mode = on" and Native vlan value of "1":'+COLOR_END)
for LAB_NODE in NODES:
    temp=input("Press Enter to continue:")
    connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")

print('\n')
print('########## C2 - M4 - 3.2.5:EtherChannel LACP ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Check Port-channel 12 is created on both DS1 and DS2 with G0/2 and G1/0 added.'+COLOR_END)
print(COLOR_BLUE+'Check LACP protocol is configured and both switches are able to initiate the negotiation.'+COLOR_END)
print(COLOR_BLUE+'Traffic should be loadbalance across both links based on source and detination IP addresses.'+COLOR_END)
print(COLOR_BLUE+'Expected Output for DS1-DS2:'+ COLOR_END)
print(COLOR_BLUE+'Group  Port-channel  Protocol    Ports'+COLOR_END)
print(COLOR_BLUE+'------+-------------+-----------+-----------------------------------------------'+COLOR_END)
print(COLOR_BLUE+'12     Po12(SU)        LACP      Gi0/2(P)    Gi1/0(P)'+COLOR_END)
print(COLOR_BLUE+'EtherChannel Load-Balancing Configuration:'+COLOR_END)
print(COLOR_BLUE+'        src-dst-ip'+COLOR_END)
print(COLOR_RED+'Look for "Protocol = LACP" and status is up Po12(SU) and "src-dst-ip" loadbalance :'+COLOR_END)
NODES = [ 'DS1', 'DS2' ]
command_set = [ 'do sh etherchannel summary | sec Group|--|12', 'do sh etherchannel load-balance | sec Configuration' ]
for LAB_NODE in NODES:
    temp=input("Press Enter to continue:")
    connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")

print('\n')
print('########## C2 - M5 - 3.2.6:EtherChannel Static ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Check Port-channel 34 is created on both DS3 and DS4 with G0/2 and G1/0 added.'+COLOR_END)
print(COLOR_BLUE+'Check that the Etherchannel is configured and both switches with static configuration.'+COLOR_END)
print(COLOR_BLUE+'Expected Output for DS3-DS4:'+ COLOR_END)
print(COLOR_BLUE+'Group  Port-channel  Protocol    Ports'+ COLOR_END)
print(COLOR_BLUE+'------+-------------+-----------+-----------------------------------------------'+ COLOR_END)
print(COLOR_BLUE+'34     Po34(SU)         -        Gi0/2(P)    Gi1/0(P)'+ COLOR_END)
print(COLOR_BLUE+'EtherChannel Load-Balancing Configuration:'+COLOR_END)
print(COLOR_BLUE+'        src-dst-ip'+COLOR_END)
print(COLOR_RED+'Look for "Protocol = "-" and status is up Po34(SU) and "src-dst-ip" loadbalance :'+COLOR_END)
NODES = [ 'DS3', 'DS4' ]
command_set = [ 'do sh etherchannel summary | sec Group|--|34', 'do sh etherchannel load-balance | sec Configuration' ]
for LAB_NODE in NODES:
    temp=input("Press Enter to continue:")
    connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")

print('########## C2 - M6 - 3.2.8: HSRP-IPv6 ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'HSRP for the 2 vlans (101-102) have been configured with the following requirements on DS3-DS4:'+COLOR_END)
print(COLOR_BLUE+'a. HSRP Virtual IP address should be FE80::10 for both vlans.'+COLOR_END)
print(COLOR_BLUE+'b. HSRP group number is 1101 for vlan1 and 1102 for vlan 102.'+COLOR_END)
print(COLOR_RED+'Look for 1101 and 1102 group number and FE80:10 IP for virtual IP in each vlan interface:'+COLOR_END)
NODES = [ 'DS3', 'DS4' ]
command_set = [ 'do sh standby brief | in FE80' ]
for LAB_NODE in NODES:
    print('\n')
    temp=input("Press Enter to continue:")
    print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
    match LAB_NODE:
        case "DS3":
            print(COLOR_BLUE+'Interface   Grp  Pri P State   Active          Standby         Virtual IP'+COLOR_END)
            print(COLOR_BLUE+'Vl101       1101 110 P Active  local           FE80::5054:FF:FE19:8065'+COLOR_END)
            print(COLOR_BLUE+'                                                               FE80::10'+COLOR_END)
            print(COLOR_BLUE+'Vl102       1102 110 P Active  local           FE80::5054:FF:FE19:8066'+COLOR_END)
            print(COLOR_BLUE+'                                                               FE80::10'+COLOR_END)       
        case "DS4":
            print(COLOR_BLUE+'Interface   Grp  Pri P State   Active          Standby         Virtual IP'+COLOR_END)
            print(COLOR_BLUE+'Vl101       1101 100   Standby FE80::5054:FF:FE1E:8065'+COLOR_END)
            print(COLOR_BLUE+'                                               local           FE80::10'+COLOR_END)
            print(COLOR_BLUE+'Vl102       1102 100   Standby FE80::5054:FF:FE1E:8066'+COLOR_END)
            print(COLOR_BLUE+'                                               local           FE80::10'+COLOR_END)
    connect(LAB_NODE, command_set)
temp=input(COLOR_RED+"Press Enter to End C2: "+COLOR_END)
###