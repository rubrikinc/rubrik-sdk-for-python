import rubrik_cdm
rubrik = rubrik_cdm.Connect()

nutanix_ahv_cluster_name = "ahvcluster"

refresh = rubrik.refresh_ahv(nutanix_ahv_cluster_name)

print(refresh)
