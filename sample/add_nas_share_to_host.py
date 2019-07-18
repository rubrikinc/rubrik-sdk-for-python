import rubrik_cdm

rubrik = rubrik_cdm.Connect()

hostname = "my_nas_host"
share_type = "NFS" # NFS or SMB
export_point = "/my_nas_share"

rubrik.add_nas_share_to_host(hostname, share_type, export_point)
