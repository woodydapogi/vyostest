#Purpose: Test automation for our network.
#Version: 1.0
#Env: Vbox
#Platform: Windows

from netmiko import *
import ping
import json

vyos1= {
    "device_type": "vyos",
    "host": "192.168.1.15",
    "username": "vyos",
    "password": "vyos"
}

vyos2= {
    "device_type": "vyos",
    "host": "192.168.1.16",
    "username": "vyos",
    "password": "vyos"
}

#Check output using ping.py module.
for ip_addr in range(16,17):
    octet= "192.168.1."
    ip= str(ip_addr)
    ping.ping_conn(f'{octet}{ip}')

with open("vyos_details.json", "r") as login_details:
    login= json.load(login_details)

try:
    main_conn= ConnectHandler(**login)
    print(f"Connection Established")

except(NetMikoAuthenticationException, NetMikoTimeoutException) as net_err:
    print(net_err)

class Network:
    def __init__(self, vyos):
        self.vyos = vyos
    
    def mac_addr(self):
        '''Output mac address from the vyos router'''
        self.vyos = main_conn.send_command("show config | match hw-id")
        return self.vyos.lstrip()
    
    def ssh(self):
        '''Output listen address'''
        self.vyos= main_conn.send_command("show config | match listen-address")
        return self.vyos.lstrip()

vyos1 = Network(main_conn)
print(vyos1.mac_addr())
print(vyos1.ssh())

'''
dev_list= [vyos1, vyos2]
for device in dev_list:
    try:
        main_conn= ConnectHandler(**device)
        print(f"{octet}{ip} ---> Connection Established")

    except(NetMikoAuthenticationException, NetMikoTimeoutException) as net_err:
        print(net_err)
'''