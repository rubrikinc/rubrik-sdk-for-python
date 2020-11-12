import rubrik_cdm

rubrik = rubrik_cdm.Connect()

username = "python-sdk-read-only"

read_only_permission = rubrik.read_only_authorization(username)
