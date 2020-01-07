import rubrik_cdm

rubrik = rubrik_cdm.Connect()

rubrik.set_esxi_subnets(["192.168.2.10/24","10.255.0.2/16"])
