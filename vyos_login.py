### Basic script --- Direct script to a single vyos router. Adu a ti useless codes.

try:

    from netmiko import *
    from subprocess import *
    import json
    import re
    import sys
    import time

except ImportError as i_err:
    print(i_err)

with open('vyos_details.json', 'r') as login:
    vyos_login= json.load(login)

### CHECK IF CONNECTION IS OK. ###
def ping_conn(ip):
    '''Ping IP Address from file.'''

    ping_ip= Popen(['ping', '-n', '1', ip], stdout=PIPE, stderr=PIPE)
    
    output, error= ping_ip.communicate()
    
    ping_output= str(output)

    #parse ip address from the output.
    ip_addr= re.search(r'[1-9]+\.[1-9]+\.[1-9]+\.[1-9]+', ping_output)
    ip_add= ip_addr.group()

    #parse error.
    if "Destination host unreachable" in ping_output or \
        "Request timed out" in ping_output:
        print(f'{ip_add} ---> Unreachable.')
    
    else:
        print(f'{ip_add} ---> Ok.')
        main_conn()
    
### ESTABLISH CONNECTION TO THE VYOS ROUTER. ###
def main_conn():
    '''Building connection to the vyos router.'''
    try: 
        main_conn.vyos_conn= ConnectHandler(**vyos_login)

        print("\n")
        print("### Connection Established. ###")
        print("\n")

    except:
        print("Timed out / Auth Error")
    
    inventory()

#SAMPLE INVENTORY
def inventory():
    options= '''
    Router Inventory:
    1. Uptime
    2. Interface
    3. MAC Address
    4. SSH
    '''
    print(options)

    option= int(input("Option#> "))
    
    uptime= main_conn.vyos_conn.send_command("show system uptime")
    interfaces= main_conn.vyos_conn.send_command("show interfaces | match eth")
    mac_addr= main_conn.vyos_conn.send_command("show config | match hw-id")
    try:
        while True:
            if option == 1:
                print(f'Uptime --- {uptime}')

            elif option == 2:
                inventory()
                print(f'Interfaces --- {interfaces}')
                inventory()
            
            elif option == 3:
                print(f'MAC Address --- {mac_addr.lstrip()}')
                inventory()
            
            elif option == 4:
                print("Config mode.")
                housekeeping()
            else:
                print("Bye!")
                sys.exit()
    
    except:
        print("Adda error, bahala kan.")

### PUSHING BASIC CONFIGURATIONS TO THE NEW ROUTER. ###
def housekeeping():
    pass

### SAVE CONFIG AND SAVE TO FILE. ###
def save_config():
    conf_file= main_conn.vyos_conn.send_command("show config")

    with open("config.boot", "w") as wr_conf:
        wr_conf.write(conf_file)
    
        if wr_conf:
            print("Config file saved.")
        else:
            print("Unsaved.")

### ORAYT LADTA ####
if __name__ == "__main__":
    ip_addr= vyos_login['host']
    ping_conn(ip_addr) 