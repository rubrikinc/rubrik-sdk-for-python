import rubrik_cdm

rubrik = rubrik_cdm.Connect()

minimum_cluster_version = 5.0

node_names = rubrik.cluster_version_check(minimum_cluster_version)
