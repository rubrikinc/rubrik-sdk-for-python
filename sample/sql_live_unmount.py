import rubrik_cdm

rubrik = rubrik_cdm.Connect()

mounted_db_name = "python-sdk-demo"
sql_instance = 'MSSQLSERVER'
sql_host = 'sql.rubrikdemo.com'

live_unmount = rubrik.sql_live_unmount(mounted_db_name, sql_instance, sql_host)