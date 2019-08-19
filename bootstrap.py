import rubrik_cdm

node_ip = '10.10.60.31'
bootstrap = rubrik_cdm.Bootstrap(node_ip)

## dns:10.10.60.2
##
node_config = {}
ipmi_config = {}
data_config = {}

node_config['RVM15BS020871'] = node_ip
node_config['RVM15BS020133'] = '10.10.60.32'
node_config['RVM15BS019940'] = '10.10.60.33'
node_config['RVM15BS019813'] = '10.10.60.34'

ipmi_config['RVM15BS020871'] = '10.10.60.35'
ipmi_config['RVM15BS020133'] = '10.10.60.36'
ipmi_config['RVM15BS019940'] = '10.10.60.37'
ipmi_config['RVM15BS019813'] = '10.10.60.38'

data_config['RVM15BS020871'] = '10.10.60.42'
data_config['RVM15BS020133'] = '10.10.60.43'
data_config['RVM15BS019940'] = '10.10.60.44'
data_config['RVM15BS019813'] = '10.10.60.45'

cluster_name = 'RUBRIKAMSLAB'
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


///""" OUTPUT....
Constructed the following JSON: 
{
 'enableSoftwareEncryptionAtRest': True, 
 'name': 'RUBRIKAMSLAB', 
 'dnsNameservers': ['8.8.8.8'], 
 'dnsSearchDomains': [], 
 'ntpServers': ['pool.ntp.org'], 
 'adminUserInfo': {'password': 'RubrikGoForward', 'emailAddress': 'Eric.Doezie@rubrik.com', 'id': 'admin'}, 
 'nodeConfigs': 
{'RVM15BS020871': {'managementIpConfig': {'netmask': '255.255.255.0', 'gateway': '10.10.60.1', 'address': '10.10.60.31'}, 'ipmiIpConfig': {'netmask': '255.255.255.0', 'gateway': '10.10.60.1', 'address': '10.10.60.35'}, 'dataIpConfig': {'netmask': '255.255.255.0', 'gateway': '10.10.60.1', 'address': '10.10.60.42'}}, 
 'RVM15BS020133': {'managementIpConfig': {'netmask': '255.255.255.0', 'gateway': '10.10.60.1', 'address': '10.10.60.32'}, 'ipmiIpConfig': {'netmask': '255.255.255.0', 'gateway': '10.10.60.1', 'address': '10.10.60.36'}, 'dataIpConfig': {'netmask': '255.255.255.0', 'gateway': '10.10.60.1', 'address': '10.10.60.43'}}, 
 'RVM15BS019940': {'managementIpConfig': {'netmask': '255.255.255.0', 'gateway': '10.10.60.1', 'address': '10.10.60.33'}, 'ipmiIpConfig': {'netmask': '255.255.255.0', 'gateway': '10.10.60.1', 'address': '10.10.60.37'}, 'dataIpConfig': {'netmask': '255.255.255.0', 'gateway': '10.10.60.1', 'address': '10.10.60.44'}}, 
 'RVM15BS019813': {'managementIpConfig': {'netmask': '255.255.255.0', 'gateway': '10.10.60.1', 'address': '10.10.60.34'}, 'ipmiIpConfig': {'netmask': '255.255.255.0', 'gateway': '10.10.60.1', 'address': '10.10.60.38'}, 'dataIpConfig': {'netmask': '255.255.255.0', 'gateway': '10.10.60.1', 'address': '10.10.60.45'}}
 }
}
///"""
