#! /usr/bin/env python3
import sys
from timeit import default_timer as timer

import rubrik_polaris
import argparse
import pprint

pp = pprint.PrettyPrinter(indent=2)

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--password', dest='password', help="Polaris Password", default=None)
parser.add_argument('-u', '--username', dest='username', help="Polaris UserName", default=None)
parser.add_argument('-d', '--domain', dest='domain', help="Polaris Domain", default=None)
parser.add_argument('-r', '--root', dest='root_domain', help="Polaris Root Domain", default=None)
parser.add_argument('--insecure', help='Deactivate SSL Verification', action="store_true")

args = parser.parse_args()

try:
    rubrik = rubrik_polaris.PolarisClient(args.domain, args.username, args.password, root_domain=args.root_domain,
                                          insecure=args.insecure)
except Exception as err:
    print(err)
    sys.exit(1)

### Schema Introspection
# pp.pprint(rubrik.get_graphql_queries_from_schema())

### Add AWS Acct (local profile must be configured, specify list of profiles _or_ set all=True.
# rubrik.add_account_aws(regions = ["us-east-1"], profiles = ["peterm-profile"])
# rubrik.add_account_aws(regions = ["us-east-1"], aws_access_key_id='blah', aws_secret_access_key='blah')
# rubrik.add_account_aws(regions = ["us-west-2"], all = True )

### Remove AWS Acct (local profile must be configured, specify list of profiles _or_ set all=True.
# rubrik.delete_account_aws(profiles = ['peterm-profile'])
# rubrik.delete_account_aws(aws_access_key_id='blah', aws_secret_access_key='blah')
# rubrik.delete_account_aws(all = True )


### Run ODS for machines in a region using Gold retention, monitor to complete via threads
# pp.pprint(rubrik.submit_on_demand(rubrik.get_object_ids_azure(region="EastUS2"), rubrik.get_sla_domains("Bronze"), wait = True))

### Returns all objectIDs matching arbitrary available inputs. ec2 tags have special treatment
# pp.pprint(rubrik.get_object_ids_ec2(tags = {"Name": "gurlingwinjb"}))
# pp.pprint(rubrik.get_object_ids_azure(region = "EastUS2"))
# pp.pprint(rubrik.get_object_ids_gce(region = "us-west1"))

### Get snapshot ids for snappables
# snappables = rubrik.get_object_ids_ec2(tags = {"Name": "gurlingwinjb"})
# snappables = rubrik.get_object_ids_azure(name = "tpm1-lin1")
# snappables = rubrik.get_object_ids_gce(nativeName = "ubuntu-fdse-shared-1")
# snappables = ['af7e69b7-b836-4ab5-9a6c-66a23ff94de8']
# for snappable in snappables:
#     snapshot_id = (rubrik.get_snapshots(snappable, recovery_point='2020-09-19 04:20')) # can include anything up to this. 2020 is ok, 2020-09, 2020-09-19, ...
#     pp.pprint(snappable)
#     snapshot_id = rubrik.get_snapshots(snappable, recovery_point='latest')
#     pp.pprint(rubrik.get_snapshots(snappable)) # Get all snapshots
#     pp.pprint(snapshot_id)

### Submit Restore for above Snapshot (EC2)
#     result = rubrik.submit_restore_ec2(snapshot_id, wait=True, should_power_on=True, should_restore_tags=True)
#     result = rubrik.submit_restore_azure(snapshot_id, wait=True, should_power_on=True, should_restore_tags=True)
#     result = rubrik.submit_restore_gce(snapshot_id, wait=True, should_power_on=True, should_restore_tags=True)
#     pp.pprint(result)

### Search for a set of objects and get their details
# for i in rubrik.get_object_ids_ec2(region = 'US_WEST_2'):
#      pp.pprint(rubrik.get_instances_ec2(i))

### Returns all instances
# pp.pprint(rubrik.get_instances_ec2())
# pp.pprint(rubrik.get_instances_gce())
# pp.pprint(rubrik.get_instances_azure())

### Returns sla domain map, or specified name/id
# pp.pprint(rubrik.get_sla_domains())
# pp.pprint(rubrik.get_sla_domains("Bronze"))

### Returns specified cloud account details, or all
# pp.pprint(rubrik.get_accounts_aws("gurling"))
# pp.pprint(rubrik.get_accounts_aws_detail("d01bd273-ccce-496b-aac1-d7ba9a0b7074"))
# pp.pprint(rubrik.get_accounts_gcp("Trinity-FDSE"))
# pp.pprint(rubrik.get_accounts_azure("RubrikRangers"))
# pp.pprint(rubrik.get_accounts_aws())
# pp.pprint(rubrik.get_accounts_gcp())
# pp.pprint(rubrik.get_accounts_azure())
# pp.pprint(rubrik.update_account_aws())

### Query objects, set sla_domain
# pp.pprint(rubrik.submit_assign_sla( rubrik.get_object_ids_ec2(region = "US_WEST_2"), rubrik.get_sla_domains("Gold")))


