import rubrik_cdm

rubrik = rubrik_cdm.Connect()

node_names = rubrik.cluster_node_name()
