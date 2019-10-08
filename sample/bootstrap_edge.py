import rubrik_cdm

## Examples of specifying IPs
## node_ip = '10.10.10.10'
## node_ip = 'fe80::250:250:250:250%ens123'
node_ip = 'SERIAL.local'

bootstrap = rubrik_cdm.Bootstrap(node_ip)

node_config = {}

node_config['SERIAL.local'] = '10.10.10.10'

cluster_name = 'CLUSTERNAME'
admin_email = 'admin@company.com'
admin_password = 'SafePassword!'
mgmt_gateway = '10.10.10.1'
mgmt_subnet_mask = '255.255.255.0'

setup_cluster = bootstrap.setup_cluster(cluster_name, admin_email, admin_password, mgmt_gateway, mgmt_subnet_mask, node_config, enable_encryption=False)

print(setup_cluster)
