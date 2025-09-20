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
print('########## C6 - M1 - 3.6.1 : Dynamic NAT - IR1 ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'When vlan 101-102 users (~400 in total users and require simultaneous internet access) in HQ1, HQ2, BR1 and BR2 communicate with internet (You can use 8.8.8.8 IP for testing) their addresses should be translated to following addresses depend on the internet router it goes through.'+COLOR_END)
print(COLOR_BLUE+'a. Traffic goes via IR1 -> 192.0.2.104 -192.0.2.110'+COLOR_END)
print('\n')
print(COLOR_RED+'Login to CR3 and CR4 and Shutdown G0/3 interfaces:'+COLOR_END)
print('From HQ1-CLI1 and HQ2-CLI1:')
print('>ping 8.8.8.8')
temp=input("Run this command in HQ1-CLI1, HQ2-CLI1 and then Press Enter:")

print('\n')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'icmp 192.0.2.104:xxx        10.10.101.101:xxx       8.8.8.8:xxx             8.8.8.8:xxx'+COLOR_END)
print(COLOR_BLUE+'icmp 192.0.2.104:xxx        10.11.102.101:xxx       8.8.8.8:xxx             8.8.8.8:xxx'+COLOR_END)
LAB_NODE = 'IR1'
command_set = [ 'do show ip nat translations | include icmp' ]
connect(LAB_NODE, command_set)
print(COLOR_RED+'Login to CR3 and CR4 and enable G0/3 interfaces:'+COLOR_END)
temp=input("Press Enter to Next Aspect:")

print('\n')
print('########## C6 - M2 - 3.6.1 : Dynamic NAT - IR2 ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'b. Traffic goes via IR2 -> 192.0.2.193 -192.0.2.199'+COLOR_END)
print('\n')
print('From HQ1-CLI1 and HQ2-CLI1:')
print('>ping 8.8.8.8')
temp=input("Run this command in HQ1-CLI1, HQ2-CLI1 and then Press Enter:")

print('\n')
print(COLOR_BLUE+'Expected Outcome:'+COLOR_END)
print(COLOR_BLUE+'icmp 192.0.2.194:xxx        10.10.101.101:xxx       8.8.8.8:xxx             8.8.8.8:xxx'+COLOR_END)
print(COLOR_BLUE+'icmp 192.0.2.194:xxx        10.11.102.101:xxx       8.8.8.8:xxx             8.8.8.8:xxx'+COLOR_END)
LAB_NODE = 'IR2'
command_set = [ 'do show ip nat translations | include icmp' ]
connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")


print('\n')
print('########## C6 - M3 3.6.2 : - Static NAT ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'When HQ1-SVR1 with IP address 10.10.100.101 goes to internet it should appear as 192.0.2.99 or 192.9.2.205 depend on if traffic goes via IR1 or IR2 respectively'+COLOR_END)
print(COLOR_BLUE+'HQ1-SVR1 has already configured with 10.10.100.101 statically'+COLOR_END)
print('\n')
print(COLOR_RED+'Login to CR3 and CR4 and Shutdown G0/3 interfaces:'+COLOR_END)
print('From HQ1-SVR1 :')
print('>ping 8.8.8.8')
temp=input("Issue ping 8.8.8.8 command in HQ1-SVR1 and then Press Enter:")

print('\n')
LAB_NODE = 'IR1'
print(COLOR_BLUE+'Expected Outcome:'+COLOR_END)
print(COLOR_BLUE+'icmp 192.0.2.99:xxx     10.10.100.101:xxx    8.8.8.8:xxx          8.8.8.8:xxx'+COLOR_END)
command_set = [ 'do show ip nat translations | include icmp' ]
connect(LAB_NODE, command_set)

temp=input("Press Enter to Next Requirement:")

print(COLOR_RED+'Login to CR3 and CR4 and "no shutdown" G0/3 interface:'+COLOR_END)
print('From HQ1-SVR1 :')
print('>ping 8.8.8.8')
temp=input("Run this command in From HQ1-SVR1 and then Press Enter:")

print('\n')
print(COLOR_BLUE+'Expected Outcome:'+COLOR_END)
print(COLOR_BLUE+'icmp 192.0.2.205:xxx     10.10.100.101:xxx    8.8.8.8:xxx          8.8.8.8:xxx'+COLOR_END)
LAB_NODE = 'IR2'
command_set = [ 'do show ip nat translations | include icmp' ]
connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")


print('\n')
print('########## C6 - M4 - 3.6.3 : NTP ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'IR1 and IR2 should get its time from ISP1 peering address 192.0.2.101 and 192.0.2.201 respectively. '+COLOR_END)
print(COLOR_BLUE+'a. All other devices in HQ1, HQ2, BR1 and BR2 should use IR1 (10.10.0.1) and IR2 (10.10.0.11) as their NTP servers'+COLOR_END)
print(COLOR_BLUE+'b. Use loopback address for NTP communication with IR1 and IR2. (Except AS1 to AS4 where you can use SVI 103 IP)'+COLOR_END)

NODES = [ 'IR1', 'IR2' ]
command_set = [ 'do sh ntp associations ' ]
for LAB_NODE in NODES:
    print('\n')
    temp=input("Press Enter to Next Requirement:")
    print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
    match LAB_NODE:
        case "IR1":
            print(COLOR_BLUE+'*~192.0.2.101     127.127.1.1      8     x     xx   xxx '+COLOR_END)
        case "IR2":
            print(COLOR_BLUE+'*~192.0.2.201     127.127.1.1      8     x     xx   xxx '+COLOR_END)
    connect(LAB_NODE, command_set)

NODES = [ 'IR1', 'IR2', 'CR1', 'CR2', 'CR3', 'CR4', 'DS1', 'DS2', 'DS3', 'DS4', 'AS1', 'AS2', 'AS3', 'AS4']
LAB_NODE = random.choice(NODES)
print('\n')
temp=input("Press Enter to Next Requirement:")
print(COLOR_BLUE+'Expected Output for '+ LAB_NODE + COLOR_END)
print(COLOR_BLUE+'*~10.10.0.1      192.0.2.101      9     x     xx   xxx '+COLOR_END)
print(COLOR_BLUE+'~10.10.0.11     192.0.2.201      9     x     xx   xxx '+COLOR_END)
command_set = [ 'do sh ntp associations' ]
connect(LAB_NODE, command_set)
temp=input("Press Enter to Next Aspect:")


print('\n')
print('########## C6 - M5 - 3.6.4 : DHCP in DS1 and DS3 ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Configure DHCP services on DS1 to meet requirements below'+COLOR_END)
print(COLOR_BLUE+'a. VL101 DHCP address scope 10.10.101.101-10.10.101.254 with default router of 10.10.101.10'+COLOR_END)
print(COLOR_BLUE+'b. VL102 DHCP address scope 10.10.102.101-10.10.102.254 with default router of 10.10.102.10'+COLOR_END)
print('\n')
print('From HQ1-CLI1:')
print('>ifconfig')
temp=input("Run this command in HQ1-CLI1 and then Press Enter:")
print(COLOR_BLUE+'Expected Outcome:'+COLOR_END)
print(COLOR_BLUE+'eth0      Link encap:Ethernet  HWaddr 52:54:00:1C:36:CD'+COLOR_END)
print(COLOR_BLUE+'          inet addr:10.10.101.10x  Bcast:0.0.0.0  Mask:255.255.255.0'+COLOR_END)
temp=input(" Press Enter:")  
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Configure DHCP services on DS3 to meet requirements below'+COLOR_END)
print(COLOR_BLUE+'c. VL101 DHCP address scope 10.11.101.101-10.11.101.254 with default router of 10.11.101.10'+COLOR_END)
print(COLOR_BLUE+'d. VL102 DHCP address scope 10.11.102.101-10.11.102.254 with default router of 10.11.102.10'+COLOR_END)
print('\n')
print('From HQ2-CLI1:')
print('>ifconfig')
temp=input("Run this command in HQ2-CLI1 and then Press Enter:")
print(COLOR_BLUE+'Expected Outcome:'+COLOR_END)
print(COLOR_BLUE+'eth0      Link encap:Ethernet  HWaddr 52:54:00:0B:BF:BF'+COLOR_END)
print(COLOR_BLUE+'          inet addr:10.11.102.10x  Bcast:0.0.0.0  Mask:255.255.255.0'+COLOR_END)
print('\n')
temp=input("Press Enter to Next Aspect:")


print('########## C6 - M6 - 3.6.5 : DHCP in BR1 and BR2 ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Configure DHCP services BR1 and BR2 in a way clients BR1-CLI1 get IP address from vlan 101 and BR2-CLI1 get IP address from vlan 102'+COLOR_END)
print(COLOR_BLUE+'a. BR1- VL101 DHCP address scope 10.1.101.101-10.1.101.254 with default-gateway 10.1.101.10'+COLOR_END)
print(COLOR_BLUE+'b. BR2- VL102 DHCP address scope 10.2.102.101-10.2.102.254 with default-gateway 10.2.102.10'+COLOR_END)
print('\n')
print('From BR1-CLI1:')
print('>ifconfig')
temp=input("Run this command in BR1-CLI1 and then Press Enter:")
print(COLOR_BLUE+'Expected Outcome:'+COLOR_END)
print(COLOR_BLUE+'eth0      Link encap:Ethernet  HWaddr 52:54:00:1A:6B:55'+COLOR_END)
print(COLOR_BLUE+'          inet addr:10.1.101.10x  Bcast:0.0.0.0  Mask:255.255.255.0'+COLOR_END)
temp=input(" Press Enter:")  
print('\n')
print('From BR2-CLI1:')
print('>ifconfig')
temp=input("Run this command in BR2-CLI1 and then Press Enter:")
print(COLOR_BLUE+'Expected Outcome:'+COLOR_END)
print(COLOR_BLUE+'eth0      Link encap:Ethernet  HWaddr 52:54:00:01:F3:4B'+COLOR_END)
print(COLOR_BLUE+'          inet addr:10.2.102.10x  Bcast:0.0.0.0  Mask:255.255.255.0'+COLOR_END)
print('\n')
temp=input("Press Enter to Next Aspect:")


print('########## C6 - M7 - 3.6.6 : DHCPv6 in DS3 ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Configure DS3 to give IPv6 addresses to clients on vlan 102 in HQ2'+COLOR_END)
print('\n')
print('From HQ2-CLI1:')
print('>ifconfig')
temp=input("Run this command in HQ2-CLI1 and then Press Enter:")
print(COLOR_BLUE+'Expected Outcome:'+COLOR_END)
print(COLOR_BLUE+'eth0      Link encap:Ethernet  HWaddr 52:54:00:0B:BF:BF'+COLOR_END)
print(COLOR_BLUE+'          inet6 addr: 2001:db8:11:102:5054:ff:fe0b:bfbf/64 Scope:Global'+COLOR_END)
print('\n')
temp=input(COLOR_RED+"Press Enter to End C6: "+COLOR_END)




