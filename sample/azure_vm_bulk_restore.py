from rubrik_security_cloud import RscClient
import requests
import urllib3, json, csv, datetime, os, sys
import json


"""
This script is used to perform bulk restores of Azure virtual machines using Rubrik Security Cloud (RSC).

Usage:
1. Create a service account in Rubrik Security Cloud (RSC), download the JSON file, and rename it to clientid.json.
2. Fill the resource_list.csv file with the name and intended recovery date of the VMs, separated by commas. If the date is not specified, the current date will be selected. 
          Example: 
          azure-testvm-01,2024-08-08
          azure-prodvm-02,2024-02-01
          
3. Change domain with your domain name
4. Run the script.

Note: Make sure to install the required dependencies before running the script.
"""


def make_api_request(url, method, headers=None, data=None, variables=None):
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        if method == "GET":
            response = requests.get(url, verify=False, headers=headers, timeout=30)
        elif method == "POST":
            response = requests.post(
                url,
                verify=False,
                headers=headers,
                json={"query": data, "variables": variables},
                timeout=30,
            )
        elif method == "DELETE":
            response = requests.delete(
                url,
                verify=False,
                headers=headers,
                json={"query": data, "variables": variables},
                timeout=30,
            )
        else:
            raise ValueError("Invalid HTTP method")

        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as http_error:
        print(f"An error occurred: {http_error}")
        return None


def get_info(query, variables):
    return make_api_request(
        uri,
        "POST",
        headers,
        data= query,
        variables= variables,
    )


os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
path = os.getcwd()

vm_info_query = """
query  ($vm_name: String!,$snapshot_filter: PolarisSnapshotFilterInput!) {
	azureNativeVirtualMachines (virtualMachineFilters: {nameSubstringFilter:{nameSubstring: $vm_name}}) {
    nodes {
      snapshotConnection (filter:$snapshot_filter){
        nodes {
          id
          indexTime
        }
      }
      vmName
      attachedManagedDisks {
        id
      }
      newestSnapshot {
        id
      }
      id
      name
      effectiveSlaDomain {
        name
      }
    }
  }
}
"""

# Load client ID data from clientid.json
with open("clientid.json", "r") as file:
    client_id_data = json.load(file)

# Extract client ID and client secret
client_id = client_id_data["client_id"]
client_secret = client_id_data["client_secret"]

uri = "https://YOURDOMAIN.my.rubrik.com/api/graphql"
# Get Headers
rsc_client = RscClient(
    domain="YOURDOMAIN.my.rubrik.com",
    client_id=client_id,
    client_secret=client_secret,
)
headers = rsc_client._headers
variables_list = []
# get vm names
with open("restore_list.csv", "r") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        vm_name = row[0]
        start_date = (
            row[1] if len(row) > 1 and row[1] else datetime.datetime.now().strftime("%Y-%m-%d")
        )
        end_date = start_date + "T23:59:59.999Z"
        variables_for_vm_info_query = {
            "vm_name": vm_name,
            "snapshot_filter": {
                "timeRange": {
                    "start": start_date,
                    "end": end_date,
                }
            },
        }
        variables_list.append(variables_for_vm_info_query)


for variables_for_vm_info_query in variables_list:
    response = get_info(vm_info_query, json.dumps(variables_for_vm_info_query))
    if response.status_code == 200:
        vm_info = response.json()
        vm_info = vm_info["data"]["azureNativeVirtualMachines"]["nodes"][0]
        snapshot_id = vm_info["snapshotConnection"]["nodes"][0]["id"]
        variables_for_mutation = {
            "input": {
                "snapshotId": snapshot_id,
                "shouldRestoreTags": True,
                "shouldPowerOn": True,
                "snapshotTypeToUseIfSourceExpired": "ARCHIVED",
            }
        }
        variables_for_mutation_json = json.dumps(variables_for_mutation)
        restore_mutation = """
        mutation AzureVMRestoreMutation($input: StartRestoreAzureNativeVirtualMachineJobInput!) {
          startRestoreAzureNativeVirtualMachineJob(input: $input) {
            jobId
            __typename
          }
        }
        """
        restore_response = make_api_request(
            uri, "POST", headers, data=restore_mutation, variables=variables_for_mutation_json
        )
        if "errors" not in restore_response.text:
            print(f"Restoring {vm_info['vmName']} in progress")
            print(restore_response.json())
        else:
            print(f"Error in restore state: {restore_response.text}")
            continue
    else:
        print(f"Error in information retrieval: {response.text}")
        continue
