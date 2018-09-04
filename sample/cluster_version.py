import rubrik_cdm

rubrik = rubrik_cdm.Connect()

cluster_version = rubrik.cluster_version()
