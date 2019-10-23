import rubrik_cdm

rubrik = rubrik_cdm.Connect()

db_name = "python-sdk-demo"
date = "10-14-2019"
time = "3:00 PM"
sql_instance = 'MSSQLSERVER'
sql_host = 'sql.rubrikdemo.com'

get_db_files = rubrik.get_sql_db_files(db_name, date, time, sql_instance, sql_host)