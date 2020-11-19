import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vms_in_sla = rubrik.get_sla_objects("Gold", "vmware")
