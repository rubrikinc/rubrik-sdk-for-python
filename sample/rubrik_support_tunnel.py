import rubrik_cdm, urllib3
urllib3.disable_warnings()


rubrik = rubrik_cdm.Connect(rubrik_cdm_ip,rubrik_cdm_user_name,rubrik_cdm_password)


tunnel = rubrik.cluster_support_tunnel(True)
print(tunnel)
tunnel = rubrik.cluster_support_tunnel(False)
print(tunnel)

