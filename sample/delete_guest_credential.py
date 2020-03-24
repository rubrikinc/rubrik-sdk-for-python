import rubrik_cdm

rubrik = rubrik_cdm.Connect()

username = "pythonuser"

delete_guest_credential = rubrik.delete_guest_credential(username)