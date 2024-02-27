from flask import Flask, render_template,jsonify
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

if __name__ == '__main__':
    app.run(debug=True)