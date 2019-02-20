import rubrik_cdm
rubrik = rubrik_cdm.Connect()

vcenter_hostname = "python.demo.lab"

refresh = rubrik.refresh_vcenter(vcenter_hostname)

print(refresh)
