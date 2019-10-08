import rubrik_cdm

node_ip = 'RVM15BS020871.local'
bootstrap = rubrik_cdm.Bootstrap(node_ip)

node_config = {}
ipmi_config = {}
data_config = {}

node_config['RVM15BS020871'] = '10.10.60.31'
node_config['RVM15BS020133'] = '10.10.60.32'
node_config['RVM15BS019940'] = '10.10.60.33'
node_config['RVM15BS019813'] = '10.10.60.34'

ipmi_config['RVM15BS020871'] = '10.10.60.35'
ipmi_config['RVM15BS020133'] = '10.10.60.36'
ipmi_config['RVM15BS019940'] = '10.10.60.37'
ipmi_config['RVM15BS019813'] = '10.10.60.38'

data_config['RVM15BS020871'] = '10.10.70.131'
data_config['RVM15BS020133'] = '10.10.70.132'
data_config['RVM15BS019940'] = '10.10.70.133'
data_config['RVM15BS019813'] = '10.10.70.134'

cluster_name = 'EMEACluster'
admin_email = 'jerome.letellier@rubrik.com'
admin_password = 'RubrikGoForward'
mgmt_gateway = '10.10.60.1'
mgmt_subnet_mask = '255.255.255.0'
ipmi_gateway = '10.10.60.1'
ipmi_subnet_mask = '255.255.255.0'
data_gateway = '10.10.70.1'
data_subnet_mask = '255.255.255.0'
dns = ['10.10.60.2']

##    def setup_cluster(self, cluster_name, admin_email, admin_password, mgmt_gateway, mgmt_subnet_mask, node_mgmt_ips,
##                      mgmt_vlan=None, ipmi_gateway=None, ipmi_subnet_mask=None, ipmi_vlan=None, node_ipmi_ips=None,
##                      data_gateway=None, data_subnet_mask=None, data_vlan=None, node_data_ips=None,
##                      enable_encryption=True, dns_search_domains=None, dns_nameservers=None,
##                      ntp_servers=None, wait_for_completion=True, timeout=30):


setup_cluster = bootstrap.setup_cluster(cluster_name, admin_email, admin_password, mgmt_gateway,mgmt_subnet_mask,None,node_config,
                                        ipmi_gateway, ipmi_subnet_mask,None,ipmi_config,
                                        data_gateway,data_subnet_mask,data_vlan=321,data_config,
                                        enable_encryption = True)

print(setup_cluster)
