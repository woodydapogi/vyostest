#Test network automation using vyos router.
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
    "password": "$75C.woodie"
}

vyos2= {
    "device_type": "vyos",
    "host": "192.168.1.16",
    "username": "vyos",
    "password": "$75C.woodie"
}

with open("vyos_details.json", "r") as login_details:
    login= json.load(login_details)

class Network:
    def __init__(self, mac_id):
        self.mac_id = mac_id
    
    def mac_addr(self):
        '''Output mac address from the vyos router'''
        
#Check output using ping.py module.
for ip_addr in range(15, 17):
    octet= "192.168.1."
    ip= str(ip_addr)
    ping.ping_conn(f'{octet}{ip}')


dev_list= [vyos1, vyos2]
for device in dev_list:
    try:
        main_conn= ConnectHandler(**device)
        print(f"{octet}{ip} ---> Connection Established")

    except(NetMikoAuthenticationException, NetMikoTimeoutException) as net_err:
        print(net_err)
