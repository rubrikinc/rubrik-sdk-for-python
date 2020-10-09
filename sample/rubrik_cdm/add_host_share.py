import rubrik_cdm

hostname = 'nas-server.rubrikdemo.com'
share_type = 'NFS'
export_point = '/nas_share'

rubrik = rubrik_cdm.Connect()

add_host_share = rubrik.add_host_share(hostname, share_type, export_point)
