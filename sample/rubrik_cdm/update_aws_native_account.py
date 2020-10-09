import rubrik_cdm

rubrik = rubrik_cdm.Connect()

current_aws_account_name = "Python"

config = {}
config["name"] = "Python-AWS-Demo"

update_native = rubrik.update_aws_native_account(current_aws_account_name, config)
