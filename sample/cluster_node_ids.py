import rubrik_cdm, urllib3
urllib3.disable_warnings()

rubrik = rubrik_cdm.Connect(rubrik_cdm_ip,rubrik_cdm_user_name,rubrik_cdm_password)

ids = rubrik.cluster_node_id()
print(ids)
