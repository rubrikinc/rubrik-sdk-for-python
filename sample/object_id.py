# VMware
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vm_name = "python-sdk-demo"
object_type = "vmware"

vmware_id = rubrik.object_id(vm_name, object_type)

# Oracle Database

rubrik = rubrik_cdm.Connect()

object_name = 'python-sdk-demo'
object_type = 'oracle_db'
hostname = 'python-sdk.demo.com'

oracle_id = rubrik.object_id(object_name, object_type, hostname=hostname)

# Organization

rubrik = rubrik_cdm.Connect()

object_name = 'PythonSDKOrganization'
object_type = 'organization'

organization_id = rubrik.object_id(object_name, object_type)

# Organization Role ID

```py

rubrik = rubrik_cdm.Connect()

object_name = 'PythonSDKOrganization'
object_type = 'organization_role_id'

organization_role_id = rubrik.object_id(object_name, object_type)
```


# Organization Admin Role

```py

rubrik = rubrik_cdm.Connect()

object_name = 'PythonSDKOrganization'
object_type = 'organization_admin_role'

organization_admin_role = rubrik.object_id(object_name, object_type)
