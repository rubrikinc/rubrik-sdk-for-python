import rubrik_cdm, urllib3
urllib3.disable_warnings()

rubrik = rubrik_cdm.Connect(rubrik_cdm_ip,rubrik_cdm_user_name,rubrik_cdm_password)


# Example with Domain creds
guest = rubrik.add_guest_creds("admin6","password123","dantest4")
print(guest)

# Example with local creds
guest = rubrik.add_guest_creds("admin6","password123")
print(guest)
