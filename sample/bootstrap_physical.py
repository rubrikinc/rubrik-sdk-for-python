import rubrik_cdm

node_ip = 'SERIAL.local'
bootstrap = rubrik_cdm.Bootstrap(node_ip)

node_config = {}
ipmi_config = {}
data_config = {}

node_config['SERIAL1'] = '10.10.10.1' 
node_config['SERIAL2'] = '10.10.10.2'
node_config['SERIAL3'] = '10.10.10.3'

ipmi_config[''SERIAL1] = '10.10.60.11'
ipmi_config[''SERIAL2] = '10.10.60.12'
ipmi_config[''SERIAL3] = '10.10.60.13'

data_config[''SERIAL1] = '10.10.60.21'
data_config[''SERIAL2] = '10.10.60.22'
data_config[''SERIAL3] = '10.10.60.23'

cluster_name = 'cluster'
admin_email = 'admin@company.com'
admin_password = 'SafePassword!'
mgmt_gateway = '10.10.10.1'
mgmt_subnet_mask = '255.255.255.0'
ipmi_gateway = '10.10.10.1'
ipmi_subnet_mask = '255.255.255.0'
data_gateway = '10.10.10.1'
data_subnet_mask = '255.255.255.0'
enable_encryption = True

setup_cluster = bootstrap.setup_cluster(cluster_name, admin_email, admin_password, mgmt_gateway,mgmt_subnet_mask,None,node_config,
                                        ipmi_gateway, ipmi_subnet_mask,None,ipmi_config,data_gateway,data_subnet_mask,None,data_config,enable_encryption,None,None)

print(setup_cluster)
