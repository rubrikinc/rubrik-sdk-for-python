import rubrik_cdm

rubrik = rubrik_cdm.Connect()

name = "python-sdk-demo"
instance = 'MSSQLSERVER'
hostname = 'sql.rubrikdemo.com'

get_db = rubrik.get_sql_db(name=name, instance=instance, hostname=hostname)