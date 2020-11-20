import rubrik_cdm

rubrik = rubrik_cdm.Connect()
vcenter_details = rubrik.get_all_vcenters()
