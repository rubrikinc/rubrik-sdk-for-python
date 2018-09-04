import rubrik_cdm

rubrik = rubrik_cdm.Connect()

# Delete an SLA Domain from the Rubrik cluster
sla_id = "0589c4e5-eeec-4ece-9922-2c9ceef7bec8"

delete_sla = rubrik.delete('v1', '/sla_domain/{}'.format(sla_id))
