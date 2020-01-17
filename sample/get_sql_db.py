import rubrik_cdm

rubrik = rubrik_cdm.Connect()

db_name = "python-sdk-demo"
instance = 'MSSQLSERVER'
hostname = 'sql.rubrikdemo.com'
availability_group = 'sql.rubrikdemo.com'
effective_sla_domain = 'Gold'
primary_cluster_id = 'local'
sla_assignment = 'Direct'

get_db = rubrik.get_sql_db(db_name=db_name, instance=instance, hostname=hostname, availability_group=availability_group, effective_sla_domain=effective_sla_domain, primary_cluster_id=primary_cluster_id, sla_assignment=sla_assignment)
