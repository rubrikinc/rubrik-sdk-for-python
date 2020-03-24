import rubrik_cdm

rubrik = rubrik_cdm.Connect()

db_name = "AdventureWorks2016"
sql_instance = 'MSSQLSERVER'
sql_host = 'sql.rubrikdemo.com'
mount_name = 'AdventureWorksClone'
date = "08-26-2018"
time = "12:11 AM"

live_mount = rubrik.sql_live_mount(db_name, sql_instance, sql_host, mount_name, date, time)