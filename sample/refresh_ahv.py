import rubrik_cdm
rubrik = rubrik_cdm.Connect()

nutanix_ahv_hostname = "ahv.example.com"

refresh = rubrik.refresh_ahv(nutanix_ahv_hostname)

print(refresh)
