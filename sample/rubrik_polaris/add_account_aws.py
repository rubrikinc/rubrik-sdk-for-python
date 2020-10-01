from rubrik_polaris import PolarisClient


domain = 'my-company'
username = 'john.doe@example.com'
password = 's3cr3tP_a55w0R)'

aws_account_id = '789702809484'


client = PolarisClient(domain, username, password, insecure=True)
client.add_account_aws(aws_account_id, 'my-aws-account', ['us-east-1'])
