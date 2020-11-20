import rubrik_cdm

rubrik = rubrik_cdm.Connect()

db_name = "python-sdk-demo"
sql_instance = 'MSSQLSERVER'
sql_host = 'sql.rubrikdemo.com'

get_live_mount = rubrik.get_sql_live_mount(db_name, sql_instance, sql_host)
