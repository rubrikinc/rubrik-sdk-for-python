import rubrik_cdm
rubrik = rubrik_cdm.Connect()

username = "python-sdk-user"
password = "RubrikPythonSDK"

create_user = rubrik.create_user(username, password)
