import rubrik_cdm

rubrik = rubrik_cdm.Connect()

remote_cluster_user = "testuser"
remote_cluster_password = "testpassword"
src_gateway = ["1.2.3.4",[1234]]
tgt_gateway = ["2.3.4.5",[1234]]

new_replication = rubrik.configure_replication_nat(remote_cluster_user, remote_cluster_password, src_gateway, tgt_gateway)
