import rubrik_cdm

node_ip = '172.22.13.66'
bootstrap = rubrik_cdm.Bootstrap(node_ip)

bootstrap_status = bootstrap.status()

print(bootstrap_status)
