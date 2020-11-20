import rubrik_cdm

rubrik = rubrik_cdm.Connect()

remote_cluster_user = "testuser"
remote_cluster_password = "testpassword"
remote_cluster_ip = "1.2.3.4"

new_replication = rubrik.configure_replication_private(remote_cluster_user, remote_cluster_password, remote_cluster_ip)
