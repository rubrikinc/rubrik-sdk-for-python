### VMware
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vm_name = "python-sdk-demo"
object_type = "vmware"

vmware_id = rubrik.object_id(vm_name, object_type)

### Oracle Database
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

object_name = 'python-sdk-demo'
object_type = 'oracle_db'
hostname = 'python-sdk.demo.com'

oracle_id = rubrik.object_id(object_name, object_type)