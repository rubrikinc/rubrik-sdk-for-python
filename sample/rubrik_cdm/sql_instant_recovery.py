import rubrik_cdm

rubrik = rubrik_cdm.Connect()

db_name = "python-sdk-demo"
date = "08-26-2018"
time = "12:11 AM"
sql_instance = 'MSSQLSERVER'
sql_host = 'sql.rubrikdemo.com'
mount_name = 'AdventureWorksClone'
finish_recovery = True
max_data_streams = 0

live_mount = rubrik.sql_instant_recovery(db_name, date, time, sql_instance, sql_host, finish_recovery, max_data_streams)
