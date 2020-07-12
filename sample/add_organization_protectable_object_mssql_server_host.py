import rubrik_cdm

rubrik = rubrik_cdm.Connect()

org = "PythonSDK"
mssql_host = "demo.rubrikdemo.com"

update_org = rubrik.add_organization_protectable_object_mssql_server_host(org, mssql_host)