import rubrik_cdm

rubrik = rubrik_cdm.Connect()

org = "PythonSDK"
mssql_db = "DemoData"
mssql_host = "demo.rubrikdemo.com"
mssql_instance = "DEMOINSTANCE"

update_org = rubrik.add_organization_protectable_object_sql_server_db(org, mssql_db, mssql_host, mssql_instance)
