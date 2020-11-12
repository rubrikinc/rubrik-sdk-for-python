import rubrik_cdm

rubrik = rubrik_cdm.Connect()

org = "PythonSDK"
ag = "demo-ag"

update_org = rubrik.add_organization_protectable_object_sql_server_availability_group(org, ag)
