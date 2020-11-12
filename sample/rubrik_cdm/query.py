### Query only

import rubrik_cdm

rubrik = rubrik_cdm.Connect()

query = """
{
  cluster(id: "me") {
    version
  }
}
"""

cluster_details = rubrik.query(query)

### All parameters used

import rubrik_cdm

rubrik = rubrik_cdm.Connect()

operation_name = "ClusterDetails"

query = """
ClusterDetails($clusterID: String!) {
  cluster(id: $clusterID) {
    version
  }
}
"""

variables = {
    "clusterID": "me"
}

cluster_details = rubrik.query(query, operation_name, variables)
