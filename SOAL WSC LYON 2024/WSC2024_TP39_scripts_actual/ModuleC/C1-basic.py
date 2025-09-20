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
            #print('\n')
    
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
print('########## C1 - M1 - 3.1.1:IPv4 Addressing - DS1 ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Interface              IP-Address      OK? Method Status                Protocol'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/0     10.10.0.122     YES manual up                    up'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/1     10.10.0.130     YES manual up                    up'+COLOR_END)
print(COLOR_BLUE+'Loopback1              10.10.0.4       YES NVRAM  up                    up'+COLOR_END)
print(COLOR_BLUE+'Vlan100                10.10.100.11    YES NVRAM  up                    up'+COLOR_END)
print(COLOR_BLUE+'Vlan101                10.10.101.11    YES NVRAM  up                    up'+COLOR_END)
print(COLOR_BLUE+'Vlan102                10.10.102.11    YES NVRAM  up                    up'+COLOR_END)
print(COLOR_BLUE+'Vlan103                10.10.103.11    YES NVRAM  up                    up'+COLOR_END)
print(COLOR_BLUE+'Vlan999                10.10.0.141     YES NVRAM  up                    up'+COLOR_END)
print('\n')
LAB_NODE = 'DS1'
command_set = [ 'do sh ip int brief | ex un' ]
connect(LAB_NODE, command_set)
temp=input(COLOR_BLUE+"Press Enter to Next Aspect: "+COLOR_END)

print('\n')
print('########## C1 - M2 - 3.1.1:IPv4 Addressing - DS2 ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Interface              IP-Address      OK? Method Status                Protocol'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/0     10.10.0.126     YES NVRAM  up                    up'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/1     10.10.0.134     YES NVRAM  up                    up'+COLOR_END)
print(COLOR_BLUE+'Loopback1              10.10.0.5       YES NVRAM  up                    up'+COLOR_END)
print(COLOR_BLUE+'Vlan100                10.10.100.12    YES NVRAM  up                    up'+COLOR_END)
print(COLOR_BLUE+'Vlan101                10.10.101.12    YES NVRAM  up                    up'+COLOR_END)
print(COLOR_BLUE+'Vlan102                10.10.102.12    YES NVRAM  up                    up'+COLOR_END)
print(COLOR_BLUE+'Vlan103                10.10.103.12    YES NVRAM  up                    up'+COLOR_END)
print(COLOR_BLUE+'Vlan999                10.10.0.142     YES NVRAM  up                    up'+COLOR_END)
print('\n')
LAB_NODE = 'DS2'
command_set = [ 'do sh ip int brief | ex un' ]
connect(LAB_NODE, command_set)
temp=input(COLOR_BLUE+"Press Enter to Next Aspect: "+COLOR_END)

print('\n')
print('########## C1 - M3 - 3.1.1:IPv4 Addressing - DS3 ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Interface              IP-Address      OK? Method Status                Protocol'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/0     10.10.0.222     YES NVRAM  up                    up'+COLOR_END)      
print(COLOR_BLUE+'GigabitEthernet0/1     10.10.0.230     YES NVRAM  up                    up'+COLOR_END)      
print(COLOR_BLUE+'Loopback1              10.10.0.14      YES NVRAM  up                    up'+COLOR_END)      
print(COLOR_BLUE+'Vlan100                10.11.100.11    YES NVRAM  up                    up'+COLOR_END)      
print(COLOR_BLUE+'Vlan101                10.11.101.11    YES NVRAM  up                    up'+COLOR_END)      
print(COLOR_BLUE+'Vlan102                10.11.102.11    YES NVRAM  up                    up'+COLOR_END)      
print(COLOR_BLUE+'Vlan103                10.11.103.11    YES NVRAM  up                    up'+COLOR_END)      
print(COLOR_BLUE+'Vlan999                10.10.0.241     YES NVRAM  up                    up'+COLOR_END)      
print('\n')
LAB_NODE = 'DS3'
command_set = [ 'do sh ip int brief | ex un' ]
connect(LAB_NODE, command_set)
temp=input(COLOR_BLUE+"Press Enter to Next Aspect: "+COLOR_END)

print('\n')
print('########## C1 - M4 - 3.1.1:IPv4 Addressing - DS4 ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Interface              IP-Address      OK? Method Status                Protocol'+COLOR_END) 
print(COLOR_BLUE+'GigabitEthernet0/0     10.10.0.226     YES NVRAM  up                    up'+COLOR_END)       
print(COLOR_BLUE+'GigabitEthernet0/1     10.10.0.234     YES NVRAM  up                    up'+COLOR_END)       
print(COLOR_BLUE+'Loopback1              10.10.0.15      YES NVRAM  up                    up'+COLOR_END)       
print(COLOR_BLUE+'Vlan100                10.11.100.12    YES NVRAM  up                    up'+COLOR_END)       
print(COLOR_BLUE+'Vlan101                10.11.101.12    YES NVRAM  up                    up'+COLOR_END)       
print(COLOR_BLUE+'Vlan102                10.11.102.12    YES NVRAM  up                    up'+COLOR_END)       
print(COLOR_BLUE+'Vlan103                10.11.103.12    YES NVRAM  up                    up'+COLOR_END)       
print(COLOR_BLUE+'Vlan999                10.10.0.242     YES NVRAM  up                    up'+COLOR_END)
print('\n')
LAB_NODE = 'DS4'
command_set = [ 'do sh ip int brief | ex un' ]
connect(LAB_NODE, command_set)
temp=input(COLOR_BLUE+"Press Enter to Next Aspect: "+COLOR_END)

print('\n')
print('########## C1 - M5 - 3.1.1:IPv4 Addressing - AS1 ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Interface              IP-Address      OK? Method Status                Protocol'+COLOR_END)
print(COLOR_BLUE+'Vlan103                10.10.103.1     YES NVRAM  up                    up'+COLOR_END)
print('\n')
LAB_NODE = 'AS1'
command_set = [ 'do sh ip int brief | ex un' ]
connect(LAB_NODE, command_set)
temp=input(COLOR_BLUE+"Press Enter to Next Aspect: "+COLOR_END)

print('\n')
print('########## C1 - M6 - 3.1.1:IPv4 Addressing - AS2 ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Interface              IP-Address      OK? Method Status                Protocol'+COLOR_END)
print(COLOR_BLUE+'Vlan103                10.11.103.1     YES manual up                    up'+COLOR_END)
print('\n')
LAB_NODE = 'AS2'
command_set = [ 'do sh ip int brief | ex un' ]
connect(LAB_NODE, command_set)
temp=input(COLOR_BLUE+"Press Enter to Next Aspect: "+COLOR_END)

print('\n')
print('########## C1 - M7 - 3.1.1:IPv4 Addressing - AS3 ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Interface              IP-Address      OK? Method Status                Protocol'+COLOR_END)
print(COLOR_BLUE+'Vlan103                10.1.103.1      YES NVRAM  up                    up'+COLOR_END)
print('\n')
LAB_NODE = 'AS3'
command_set = [ 'do sh ip int brief | ex un' ]
connect(LAB_NODE, command_set)
temp=input(COLOR_BLUE+"Press Enter to Next Aspect: "+COLOR_END)

print('\n')
print('########## C1 - M8 - 3.1.1:IPv4 Addressing - AS4 ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Interface              IP-Address      OK? Method Status                Protocol'+COLOR_END)
print(COLOR_BLUE+'Vlan103                10.2.103.1      YES NVRAM  up                    up'+COLOR_END)
print('\n')
LAB_NODE = 'AS4'
command_set = [ 'do sh ip int brief | ex un' ]
connect(LAB_NODE, command_set)
temp=input(COLOR_BLUE+"Press Enter to Next Aspect: "+COLOR_END)

print('\n')
print('########## C1 - M9 - 3.1.1:IPv4 Addressing - BR1 ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Interface                  IP-Address      OK? Method Status                Protocol'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/0         192.0.2.2       YES manual up                    up'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/1.100     10.1.100.10     YES manual up                    up'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/1.101     10.1.101.10     YES manual up                    up'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/1.102     10.1.102.10     YES manual up                    up'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/1.103     10.1.103.10     YES manual up                    up'+COLOR_END)
print(COLOR_BLUE+'Loopback1                  10.10.0.21      YES manual up                    up'+COLOR_END)
print('\n')
LAB_NODE = 'BR1'
command_set = [ 'do sh ip int brief | ex un' ]
connect(LAB_NODE, command_set)
temp=input(COLOR_BLUE+"Press Enter to Next Aspect: "+COLOR_END)

print('\n')
print('########## C1 - M10 - 3.1.1:IPv4 Addressing - BR2 ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Interface                  IP-Address      OK? Method Status                Protocol'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/0         192.0.2.6       YES NVRAM  up                    up'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/1.100     10.2.100.10     YES NVRAM  up                    up'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/1.101     10.2.101.10     YES NVRAM  up                    up'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/1.102     10.2.102.10     YES NVRAM  up                    up'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/1.103     10.2.103.10     YES NVRAM  up                    up'+COLOR_END)
print(COLOR_BLUE+'Loopback1                  10.10.0.22      YES NVRAM  up                    up'+COLOR_END)
print('\n')
LAB_NODE = 'BR2'
command_set = [ 'do sh ip int brief | ex un' ]
connect(LAB_NODE, command_set)
temp=input(COLOR_BLUE+"Press Enter to Next Aspect: "+COLOR_END)

print('\n')
print('########## C1 - M11 - 3.1.1:IPv6 Addressing - IR2, CR3, CR4, DS3, DS4 ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'IR2 IPv6 Addressing'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/1     [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:0:204::1'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/2     [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:0:208::1'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/3     [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:0:200::2'+COLOR_END)
print(COLOR_BLUE+'Loopback1              [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:0:11::1'+COLOR_END)
print('\n')
LAB_NODE = 'IR2'
command_set = [ 'do sh ipv6 int brief | ex un' ]
connect(LAB_NODE, command_set)
temp=input(COLOR_BLUE+"Press Enter to check IPv6 Addressing of CR3: "+COLOR_END)

print(COLOR_BLUE+'CR3 IPv6 Addressing'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/0     [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:0:212::1'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/1     [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:0:220::1'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/2     [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:0:224::1'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/3     [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:0:204::2'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/4     [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:0:136::2'+COLOR_END)
print(COLOR_BLUE+'Loopback1              [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:0:12::1'+COLOR_END)
print('\n')
LAB_NODE = 'CR3'
command_set = [ 'do sh ipv6 int brief | ex un' ]
connect(LAB_NODE, command_set)
temp=input(COLOR_BLUE+"Press Enter to check IPv6 Addressing of CR4: "+COLOR_END)

print(COLOR_BLUE+'CR4 IPv6 Addressing'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/0     [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:0:212::2'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/1     [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:0:228::1'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/2     [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:0:232::1'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/3     [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:0:208::2'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/4     [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:0:116::2'+COLOR_END)
print(COLOR_BLUE+'Loopback1              [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:0:13::1'+COLOR_END)
print('\n')
LAB_NODE = 'CR4'
command_set = [ 'do sh ipv6 int brief | ex un' ]
connect(LAB_NODE, command_set)
temp=input(COLOR_BLUE+"Press Enter to check IPv6 Addressing of DS3: "+COLOR_END)

print(COLOR_BLUE+'DS3 IPv6 Addressing'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/0     [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:0:220::2'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/1     [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:0:228::2'+COLOR_END)
print(COLOR_BLUE+'Loopback1              [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:0:14::1'+COLOR_END)
print(COLOR_BLUE+'Vlan100                [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:11:100::11'+COLOR_END)
print(COLOR_BLUE+'Vlan101                [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:11:101::11'+COLOR_END)
print(COLOR_BLUE+'Vlan102                [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:11:102::11'+COLOR_END)
print(COLOR_BLUE+'Vlan999                [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:0:240::1'+COLOR_END)
print('\n')
LAB_NODE = 'DS3'
command_set = [ 'do sh ipv6 int brief | ex un' ]
connect(LAB_NODE, command_set)
temp=input(COLOR_BLUE+"Press Enter to check IPv6 Addressing of DS4: "+COLOR_END)

print(COLOR_BLUE+'DS4 IPv6 Addressing'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/0     [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:0:224::2'+COLOR_END)
print(COLOR_BLUE+'GigabitEthernet0/1     [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:0:232::2'+COLOR_END)
print(COLOR_BLUE+'Loopback1              [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:0:15::1'+COLOR_END)
print(COLOR_BLUE+'Vlan100                [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:11:100::12'+COLOR_END)
print(COLOR_BLUE+'Vlan101                [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:11:101::12'+COLOR_END)
print(COLOR_BLUE+'Vlan102                [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:11:102::12'+COLOR_END)
print(COLOR_BLUE+'Vlan999                [up/up]'+COLOR_END)
print(COLOR_BLUE+'    2001:DB8:0:240::2'+COLOR_END)
print('\n')
LAB_NODE = 'DS4'
command_set = [ 'do sh ipv6 int brief | ex un' ]
connect(LAB_NODE, command_set)
temp=input(COLOR_BLUE+"Press Enter to Next Aspect: "+COLOR_END)

print('\n')
print('########## C1 - M12 - 3.1.3:TimeZone ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'timezone is CET 1 0'+COLOR_END)
print(COLOR_BLUE+'clock summer-time CET recurring last Sun Mar 2:00 last Sun Oct 3:00'+COLOR_END)
print('\n')
NODES = [ 'IR1', 'CR1', 'CR2', 'DS1', 'DS2', 'AS1', 'IR2', 'CR3', 'CR4', 'DS3', 'DS4', 'AS2', 'BR1', 'AS3', 'BR2', 'AS4' ]
LAB_NODE = random.choice(NODES)
command_set = [ 'do show run | include clock' ]
connect(LAB_NODE, command_set)
temp=input(COLOR_BLUE+"Press Enter to Next Aspect: "+COLOR_END)

print('\n')
print('########## C1 - M13 - 3.1.4:DomainName ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'Domain Name is wsc2024.net'+COLOR_END)
print('\n')
NODES = [ 'IR1', 'CR1', 'CR2', 'DS1', 'DS2', 'AS1', 'IR2', 'CR3', 'CR4', 'DS3', 'DS4', 'AS2', 'BR1', 'AS3', 'BR2', 'AS4' ]
LAB_NODE = random.choice(NODES)
command_set = [ 'do show ip domain' ]
connect(LAB_NODE, command_set)
temp=input(COLOR_BLUE+"Press Enter to Next Aspect: "+COLOR_END)

print('\n')
print('########## C1 - M14 - 3.1.5:Privileged mode password ##########')
print(COLOR_BLUE+'Requirement:'+COLOR_END)
print(COLOR_BLUE+'You should see output like this: username admin privilege 15 secret 9 $9$NOUZJkpL/2WNiv$pL9bus2.Tf90j8ZBwV1AwBfv/jPJFmmzmWtH0WUF2/Q. Password type is 9. Hash value could be different.'+COLOR_END)
print(COLOR_BLUE+'You should see output like this: enable secret 9 $9$eXQkNfnt7wXC5f$wmtQW14ysBLUDV87oOrKy90eX8FXdYKP77JaEMr7ddo. Password type is 9. Hash value could be different.'+COLOR_END)
print(COLOR_RED+'Password type is 9. Hash value could be different.'+COLOR_END)
print('\n')
NODES = [ 'IR1', 'CR1', 'CR2', 'DS1', 'DS2', 'AS1', 'IR2', 'CR3', 'CR4', 'DS3', 'DS4', 'AS2', 'BR1', 'AS3', 'BR2', 'AS4' ]
LAN_NODE = random.choice(NODES)
command_set = [ 'do show run | include admin |enable secret' ]
connect(LAB_NODE, command_set)
temp=input(COLOR_RED+"Press Enter to End C1: "+COLOR_END)

