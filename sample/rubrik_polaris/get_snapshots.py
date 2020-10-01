from rubrik_polaris import PolarisClient


domain = 'my-company'
username = 'john.doe@example.com'
password = 's3cr3tP_a55w0R)'

aws_account_id = '789702809484'


client = PolarisClient(domain, username, password, insecure=True)
client.add_account_aws(aws_account_id, 'my-aws-account', ['us-east-1'])


snappables = client.get_object_ids_ec2(tags = {"Environment": "staging"})
for snappable in snappables:
    snapshot_id = client.get_snapshots(snappable, recovery_point='latest')
    print(snapshot_id)
