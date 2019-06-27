import rubrik_cdm, urllib3
urllib3.disable_warnings()

rubrik = rubrik_cdm.Connect(rubrik_cdm_ip,rubrik_cdm_user_name,rubrik_cdm_password)

# Example with Domain Creds
del_guest = rubrik.del_guest_creds("admin6","dantest4")
print (del_guest)

# Example with Local Creds
del_guest = rubrik.del_guest_creds("admin5")
print (del_guest)