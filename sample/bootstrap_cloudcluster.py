import rubrik_cdm

## Examples of specifying IPs
## node_ip = '10.10.10.10'
## node_ip = 'fe80::250:56ff:fe90:36b7%ens192'
node_ip = 'VRVW4210B38ED.local'

bootstrap = rubrik_cdm.Bootstrap(node_ip)

node_config = {}

node_config['VRVW4210B38ED'] = '10.10.60.230'

cluster_name = 'RUBRIKAMSLABED'
admin_email = 'Eric.Doezie@rubrik.com'
admin_password = 'RubrikGoForward'
mgmt_gateway = '10.10.60.1'
mgmt_subnet_mask = '255.255.255.0'
enable_encryption = False

setup_cluster = bootstrap.setup_cluster(cluster_name, admin_email, admin_password, mgmt_gateway,mgmt_subnet_mask,None,node_config,enable_encryption=False)

print(setup_cluster)
