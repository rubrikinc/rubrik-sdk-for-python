from rubrik_polaris import PolarisClient


domain = 'my-company'
username = 'john.doe@example.com'
password = 's3cr3tP_a55w0R)'

aws_account_id = '789702809484'


client = PolarisClient(domain, username, password, insecure=True)

# Search for a set of objects and get their details
for i in client.get_object_ids_gce():
    print(client.get_instances_gce(i))
