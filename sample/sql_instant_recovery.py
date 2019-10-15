import rubrik_cdm

rubrik = rubrik_cdm.Connect()

db_name = "AdventureWorks2016"
date = "08-26-2018"
time = "12:11 AM"
sql_instance = 'MSSQLSERVER'
sql_host = 'sql.rubrikdemo.com'

live_mount = rubrik.sql_instant_recovery(db_name, date, time, sql_instance, sql_host)