import rubrik_cdm

rubrik = rubrik_cdm.Connect()
host_details = rubrik.get_all_hosts()
