import rubrik_cdm

rubrik = rubrik_cdm.Connect()

config = {}
config['id'] = "pythonsdk"
config['password'] = "RubrikGoForward"
config['firstName'] = "Rubrik"
config['lastName'] = "Ranger"
config['emailAddress'] = "Rubrik.Ranger@pysdk.com"
config['contactNumber'] = "555-555-5555"

create_user = rubrik.post('internal', '/user', config)
