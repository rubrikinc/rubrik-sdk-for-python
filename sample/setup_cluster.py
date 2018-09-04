import rubrik_cdm

node_ip = '172.22.13.66'
bootstrap = rubrik_cdm.Bootstrap(node_ip)

node_config = {}
node_config['1'] = node_ip
node_config['2'] = '172.22.18.241'
node_config['3'] = '172.22.9.68'
node_config['4'] = '172.22.12.154'

cluster_name = 'Python-SDK'
admin_email = 'Drew.Russell@rubrik.com'
admin_password = 'RubrikGoForward'
management_gateway = '172.22.0.1'
management_subnet_mask = '255.255.240.0'

enable_encryption = False

setup_cluster = bootstrap.setup_cluster(cluster_name, admin_email, admin_password, management_gateway,
                                        management_subnet_mask, node_config, enable_encryption)

print(setup_cluster)
