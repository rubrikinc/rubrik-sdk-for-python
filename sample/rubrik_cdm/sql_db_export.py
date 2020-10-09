import rubrik_cdm

rubrik = rubrik_cdm.Connect()

db_name = "python-sdk-demo"
date = '10-21-2019'
time = '3:00 PM'
sql_instance = 'MSSQLSERVER'
sql_host = 'sql.rubrikdemo.com'
target_instance_name = sql_instance
target_hostname = sql_host
target_database_name = 'Demo_Export'
target_data_file_path = 'C:\\Program Files\\Microsoft SQL ' \
                        'Server\\MSSQL13.MSSQLSERVER\\MSSQL\\DATA\\AdventureWorks2016_export'
target_log_file_path = 'C:\\Program Files\\Microsoft SQL ' \
                       'Server\\MSSQL13.MSSQLSERVER\\MSSQL\\DATA\\AdventureWorks2016_export'
target_file_paths = [{'logicalName': 'AdventureWorks2016_Data',
                      'exportPath': 'C:\\Program Files\\Microsoft SQL '
                                    'Server\\MSSQL13.MSSQLSERVER\\MSSQL\\DATA\\AdventureWorks2016_export',
                      'newLogicalName': 'AdventureWorks2016_Data_export',
                      'newFilename': 'AdventureWorks2016_Data_export.mdf'},
                     {'logicalName': 'AdventureWorks2016_Log',
                      'exportPath': 'C:\\Program Files\\Microsoft SQL '
                                    'Server\\MSSQL13.MSSQLSERVER\\MSSQL\\DATA\\AdventureWorks2016_export',
                      'newLogicalName': 'AdventureWorks2016_Log_export',
                      'newFilename': 'AdventureWorks2016_Log_export.mdf'}]

sql_db_export = rubrik.sql_db_export(db_name,
                                     date,
                                     time,
                                     sql_instance,
                                     sql_host,
                                     target_instance_name,
                                     target_hostname,
                                     target_database_name,
                                     target_data_file_path,
                                     target_log_file_path,
                                     target_file_paths)
