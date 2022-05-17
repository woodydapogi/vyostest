# Sending icmp to our existing deployed vyos routers.
# Checking if vyos routers ip addresses are reachable.
# Env: Windows

from subprocess import *
import re

def ping_conn(ip):
    '''Ping IP Address from file.'''

    #sending ping command using windows' ping command.
    #linux: ping <ip> -c <n>
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

'''
for ip_addr in range(15,17):
    ip= str(ip_addr)
    octets= "192.168.1."
    ping_conn(f'{octets}{ip}')
'''