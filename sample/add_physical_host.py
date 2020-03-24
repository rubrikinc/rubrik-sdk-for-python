### Single Host
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

hostname = "python-sdk-demo"

add_host = rubrik.add_physical_host(hostname)

### Bulk Hosts
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

hosts = ['host1.rubrik.com','host2.rubrik.com','host3.rubrik.com']
bulk_add = rubrik.add_physical_host(hosts)