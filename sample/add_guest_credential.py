import rubrik_cdm

rubrik = rubrik_cdm.Connect()

username = "pythonuser"
password = "python123!"

add_guest_credential = rubrik.add_guest_credential(username, password)