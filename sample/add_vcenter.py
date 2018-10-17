import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vcenter_ip = "demo-vcsa.python.demo"
vcenter_username = "pythonuser"
vcenter_password = "python123!"


add_vcenter, url = rubrik.add_vcenter(
    vcenter_ip, vcenter_username, vcenter_password)
