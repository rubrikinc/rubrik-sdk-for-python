import rubrik_cdm

rubrik = rubrik_cdm.Connect()

# Retrieve summary information for the "Python SDK" SLA Domain
sla_name = "Python SDK"

sla_summary_information = rubrik.get('v1', '/sla_domain?name={}'.format(sla_name))

# The same information but now using the optional params argument
params = {
    "name": "Python SDK"
}

sla_summary_information = rubrik.get('v1', '/sla_domain', params=params)