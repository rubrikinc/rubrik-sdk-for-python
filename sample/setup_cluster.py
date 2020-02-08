# This file contains multiple bootstrap examples for different cluster types. 
# See https://rubrik.gitbook.io/rubrik-sdk-for-python/bootstrap-functions/setup_cluster for additional info

#
# Physical Cluster Bootstrap
#

import rubrik_cdm

## IPv6 only. mDNS broadcast - avahi daemon
node_ip = 'SERIAL1.local'
bootstrap = rubrik_cdm.Bootstrap(node_ip)

## Alternatively, specify local interface
## interface = 'ens160'
## bootstrap = rubrik_cdm.Bootstrap(node_ip, interface)

node_config = {}
ipmi_config = {}
data_config = {}

node_config['SERIAL1'] = '10.10.10.10'
node_config['SERIAL2'] = '10.10.10.12'
node_config['SERIAL3'] = '10.10.10.13'
node_config['SERIAL4'] = '10.10.10.14'

ipmi_config['SERIAL1'] = '10.10.10.15'
ipmi_config['SERIAL2'] = '10.10.10.16'
ipmi_config['SERIAL3'] = '10.10.10.17'
ipmi_config['SERIAL4'] = '10.10.10.18'

cluster_name = 'CLUSTERNAME'
admin_email = 'admin@company.com'
admin_password = 'SafePassword!'
mgmt_gateway = '10.10.10.1'
mgmt_subnet_mask = '255.255.255.0'
ipmi_gateway = '10.10.10.1'
ipmi_subnet_mask = '255.255.255.0'
data_gateway = None
data_subnet_mask = None
dns = ['10.10.10.2']
encryption = False

setup_cluster = bootstrap.setup_cluster(cluster_name, admin_email, admin_password, mgmt_gateway,mgmt_subnet_mask,node_config, None,
                                        ipmi_gateway, ipmi_subnet_mask,None,ipmi_config,
                                        data_gateway,data_subnet_mask,data_vlan,None,
                                        encryption, None, dns)

#                                        
# Virtual Appliance (Edge) Bootstrap
#

import rubrik_cdm

## Examples of specifying IPs (v4 or v6 possible)
## node_ip = '10.10.10.10'
## node_ip = 'fe80::250:250:250:250'
node_ip = 'SERIAL.local'

bootstrap = rubrik_cdm.Bootstrap(node_ip)

node_config = {}
node_config['SERIAL.local'] = '10.10.10.10'

cluster_name = 'CLUSTERNAME'
admin_email = 'admin@company.com'
admin_password = 'SafePassword!'
mgmt_gateway = '10.10.10.1'
mgmt_subnet_mask = '255.255.255.0'

setup_cluster = bootstrap.setup_cluster(cluster_name, admin_email, admin_password, mgmt_gateway, mgmt_subnet_mask, 
										node_config, enable_encryption=False)

#
# Cloud Cluster Bootstrap
#

import rubrik_cdm

## IPv4 only bootstrap.
node_ip = '10.10.10.10'

bootstrap = rubrik_cdm.Bootstrap(node_ip)

node_config = {}

node_config['SERIAL1'] = '10.10.10.10'
node_config['SERIAL2'] = '10.10.10.11'
node_config['SERIAL3'] = '10.10.10.12'
node_config['SERIAL4'] = '10.10.10.13'

cluster_name = 'CLUSTERNAME'
admin_email = 'admin@company.com'
admin_password = 'SafePassword!'
mgmt_gateway = '10.10.60.1'
mgmt_subnet_mask = '255.255.255.0'

setup_cluster = bootstrap.setup_cluster(cluster_name, admin_email, admin_password, mgmt_gateway, mgmt_subnet_mask, node_config, enable_encryption=False)

print(setup_cluster)