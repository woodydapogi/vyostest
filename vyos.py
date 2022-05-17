#Purpose: Test automation for our network.
#Version: 1.0
#Env: Vbox
#Platform: Windows

try:
    from netmiko import *
    import ping #from ping.py module.
    import json

except ImportError as i_err:
    print(i_err)

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

#Establishing connection to the vyos router/s.
try:
    main_conn= ConnectHandler(**login) #from netmiko library.
    print(f"Connection Established")

except(NetMikoAuthenticationException, NetMikoTimeoutException) as net_err:
    print(net_err)

#Basic object creation for specific purpose.
class Network:
    def __init__(self, vyos):
        self.vyos = vyos
    
    def mac_addr(self):
        '''Output mac address from the vyos router'''
        self.vyos = main_conn.send_command("show config | match hw-id")
        return f'\nMAC ADDR: {self.vyos.lstrip()}'
    
    def ssh(self):
        '''Output ssh listen address'''
        self.vyos= main_conn.send_command("show config | match listen-address")
        return f'\nSSH: {self.vyos.lstrip()}'
    
    def ospf_config(self):
        '''OSPF configuration'''
        show_ospf="show config | match ospf"
        ospf_conf="set protocol area 20 network 192.168.10.0/24"

        self.vyos= main_conn.send_command(show_ospf)

        if self.vyos == "":
            return "OSPF not set."

        #self.vyos= main_conn.send_config_set(ospf_conf, exit_config_mode=False)

        #self.vyos.main_conn.commit()

vyos1 = Network(main_conn)
print(vyos1.mac_addr())
print(vyos1.ssh())
print(vyos1.ospf_config())