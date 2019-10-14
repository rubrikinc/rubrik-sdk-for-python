import rubrik_cdm

## IPv6 only. mDNS broadcast - avahi daemon
node_ip = 'SERIAL1.local'
bootstrap = rubrik_cdm.Bootstrap(node_ip)

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
data_gateway = '10.10.20.1'
data_subnet_mask = '255.255.255.0'
dns = ['10.10.10.2']

setup_cluster = bootstrap.setup_cluster(cluster_name, admin_email, admin_password, mgmt_gateway,mgmt_subnet_mask,node_config, None,
                                        ipmi_gateway, ipmi_subnet_mask,None,ipmi_config,
                                        None,None,None,None,
                                        False, None, dns)
print(setup_cluster)
