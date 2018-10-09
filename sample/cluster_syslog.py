import rubrik_cdm

rubrik = rubrik_cdm.Connect()

syslog_ip = "192.168.1.208"
protocol = "UDP"

syslog = rubrik.cluster_syslog(syslog_ip, protocol)
