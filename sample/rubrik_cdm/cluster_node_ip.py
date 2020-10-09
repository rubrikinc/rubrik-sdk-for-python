import rubrik_cdm

rubrik = rubrik_cdm.Connect()

cluster_node_ips = rubrik.cluster_node_ip()
