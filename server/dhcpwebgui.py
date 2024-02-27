from flask import Flask, render_template,jsonify,request,redirect
from dhcp import *
import os
import sys

app = Flask(__name__)

# Assuming DHCPServer and DHCPServerConfiguration are defined in dhcp.py
configuration = DHCPServerConfiguration()
configuration.debug = print
HERE = os.path.dirname(sys.argv[0])
configuration.load(os.path.join(HERE, 'dhcpgui.conf'))
server = DHCPServer(configuration)
server.run_in_thread()

@app.route('/')
def home():
    hosts = server.get_all_hosts()
    current_hosts = server.get_current_hosts()
    time_sorted_hosts = list(reversed(sorted(hosts, key=lambda host: host.last_used)))
    # Convert hosts info into a list of dicts for easier handling in the template
    hosts_info = [{
        'mac': host.mac,
        'ip': host.ip,
        'hostname': host.hostname,
        'is_current': host in current_hosts
    } for host in time_sorted_hosts]
    return render_template('index.html', hosts_info=hosts_info)



@app.route('/update')
def update():
    hosts = server.get_all_hosts()
    current_hosts = server.get_current_hosts()
    time_sorted_hosts = list(reversed(sorted(hosts, key=lambda host: host.last_used)))

    hosts_info = [{
        'mac': host.mac,
        'ip': host.ip,
        'hostname': host.hostname,
        'is_current': host in current_hosts
    } for host in time_sorted_hosts]

    return jsonify(hosts_info)

@app.route('/update-config', methods=['POST'])
def update_config():
    # Extracting form data
    dhcp_offer_after_seconds = request.form.get('dhcp_offer_after_seconds')
    dhcp_acknowledge_after_seconds = request.form.get('dhcp_acknowledge_after_seconds')
    network = request.form.get('network')
    subnet_mask = request.form.get('subnet_mask')
    
    # Construct the new configuration string
    new_config = f"""
# This config file is Python code.
# It is executed when starting dhcpgui.pyw.

########### Timings ###########
dhcp_offer_after_seconds = {dhcp_offer_after_seconds}
dhcp_acknowledge_after_seconds = {dhcp_acknowledge_after_seconds}

########### Network ###########
# This is the network address
network = '{network}'
# This is the subnet mask
subnet_mask = '{subnet_mask}'

# Currently there is no range configuration.
# Assigned IP addresses will range from 5 to 250.

# This is the address of the router.
# router = None # Do not tell clients about routers.
# router = []   # Tell clients there is no router.
# router = ['192.168.137.1'] # 192.168.137.1 is a router.
router = None

# This are the addresses of the DNS-server.
# domain_name_server = None # Do not tell clients about DNS-Servers.
# domain_name_server = []   # Tell clients there is no DNS-server.
# domain_name_server = ['192.168.137.1'] # 192.168.137.1 is a DNS-Server.
domain_name_server = None # list of ips

# This is the time in seconds after which the client
#   should have asked for a new IP address.
# 1 day is 86400 seconds.
ip_address_lease_time = 300

# This is the broadcast address
# If the network is 192.168.137.0 
#   the broadcast address could also be 192.168.137.255
broadcast_address = '255.255.255.255'

# Listen to DHCP requests on this interface
# bind_address = '192.168.137.10'  # Listen for requests on this specific interface
bind_address = ''                 # Listen for requests on all interfaces

########### Memory ###########
# This is the path to a file to the DHCP-servers memory.
# MAC, IP and host name will be stored there 
#   in CSV format.
# You can delete the file and the DHCP-server will 
#   assign different IP-addresses.
# It also contains the entries not issued by the DHCP-server.
host_file = 'hosts.csv'

########### Options ###########
# You can set all options that a DHCP-server can serve.
# There are 253 of them.
# See the RFC 2132 for a list of options:
#   https://tools.ietf.org/html/rfc2132
# How do you set options:
#
# 1. You can set options by name.
#     You can find the name in listener.py.
#     Example: subnet_mask
#     
# 2. You can set options by number.
#     You can find the number in the RFC 2132.
#     Named options are preferred over unnamed options.
#     Example: option_1
#     Option 1 is the subnet mask.
#     Because subnet_mask = '255.255.255.0' is in this
#       file, the option_1 = '255.255.255.0' statement
#       is ignored.
#
# If you see "3.17. Domain Name" you can use 
#   "Domain Name".lower().replace(" ", "_") 
#   to convert it to the variable name.
#
# Some options do not have conversion functions
#   assigned to them so you need to use bytes.
# Example: domain_name = b'hello.kitty.tv'
# Again, see listener.py



    """

    # Write the new configuration to dhcpgui.conf
    with open('dhcpgui.conf', 'w') as config_file:
        config_file.write(new_config)

    # Redirect back to the main page or display a success message
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)