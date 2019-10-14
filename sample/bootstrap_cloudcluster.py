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
