from rubrik_polaris import PolarisClient


domain = 'my-company'
username = 'john.doe@example.com'
password = 's3cr3tP_a55w0R)'

client = PolarisClient(domain, username, password, insecure=True)


# Run On-Demand Snapshot for machines in us_west1 using Gold retention, wait until completion

object_ids = client.get_object_ids_gce(region='us-west-1')
sla_domain = client.get_sla_domains('Gold')

client.submit_on_demand(object_ids, sla_domain, wait = True)
