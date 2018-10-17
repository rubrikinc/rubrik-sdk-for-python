import rubrik_cdm

rubrik = rubrik_cdm.Connect()

dns_server_ip = ["192.168.100.21", "192.168.100.22"]
cluster_dns_servers = rubrik.cluster_dns_servers(dns_server_ip)
