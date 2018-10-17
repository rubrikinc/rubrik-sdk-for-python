import rubrik_cdm

rubrik = rubrik_cdm.Connect()

ntp_servers = ["192.168.10.121", "192.168.10.122"]
configure_ntp = rubrik.cluster_ntp(ntp_servers)
