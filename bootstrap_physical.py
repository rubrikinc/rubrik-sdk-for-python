import rubrik_cdm

management IP address: 10.10.60.34
management IP address: 10.10.60.33
management IP address: 10.10.60.32
management IP address: 10.10.60.31
node id: RVM15BS019813
node id: RVM15BS019940
node id: RVM15BS020133
node id: RVM15BS020871

IPMI address: 10.10.60.38
IPMI address: 10.10.60.37
IPMI address: 10.10.60.36
IPMI address: 10.10.60.35

cluster uuid: 4320a9d1-fb73-440e-8ec9-3343029300f1
cluster id: cluster
NTP servers: pool.ntp.org
DNS servers: 10.10.60.2

node_ip = ''
bootstrap = rubrik_cdm.Bootstrap(node_ip)

## dns:10.10.60.2
##
node_config = {}
ipmi_config = {}
data_config = {}

node_config[''RVM15BS020871] = '10.10.60.31' 
node_config[''RVM15BS020133] = '10.10.60.32'
node_config[''RVM15BS019940] = '10.10.60.33'
node_config[''RVM15BS019813] = '10.10.60.34'

ipmi_config[''RVM15BS020871] = '10.10.60.35'
ipmi_config[''RVM15BS020133] = '10.10.60.36'
ipmi_config[''RVM15BS019940] = '10.10.60.37'
ipmi_config[''RVM15BS019813] = '10.10.60.38'

data_config[''RVM15BS020871] = '10.10.60.131'
data_config[''RVM15BS020133] = '10.10.60.132'
data_config[''RVM15BS019940] = '10.10.60.133'
data_config[''RVM15BS019813] = '10.10.60.134'

cluster_name = 'cluster'
admin_email = 'Eric.Doezie@rubrik.com'
admin_password = 'RubrikGoForward'
mgmt_gateway = '10.10.60.1'
mgmt_subnet_mask = '255.255.255.0'
ipmi_gateway = '10.10.60.1'
ipmi_subnet_mask = '255.255.255.0'
data_gateway = '10.10.60.1'
data_subnet_mask = '255.255.255.0'
enable_encryption = True

setup_cluster = bootstrap.setup_cluster(cluster_name, admin_email, admin_password, mgmt_gateway,mgmt_subnet_mask,None,node_config,
                                        ipmi_gateway, ipmi_subnet_mask,None,ipmi_config,data_gateway,data_subnet_mask,None,data_config,enable_encryption,None,None)

print(setup_cluster)
