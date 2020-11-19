import rubrik_cdm

rubrik = rubrik_cdm.Connect()

cluster_version = 5.0

node_names = rubrik.minimum_installed_cdm_version(cluster_version)
