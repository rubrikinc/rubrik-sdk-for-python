# add\_vcenter

Add a new vCenter to the Rubrik cluster.

```python
def add_vcenter(self, vcenter_ip, vcenter_username, vcenter_password, vm_linking=True, ca_certificate=None, timeout=30):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| vcenter\_ip | str | The IP address or FQDN of the vCenter you wish to add. |  |
| vcenter\_username | str | The vCenter username used for authentication. |  |
| vcenter\_password | str | The vCenter password used for authentication. |  |

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| vm\_linking | bool | Automatically link discovered virtual machines \(i.e VM Linking\). |  | True |
| ca\_certificate | str | CA certificiate used to perform TLS certificate validation |  | None |
| timeout | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |  | 30 |

## Returns

| Type | Return Value |
| :--- | :--- |
| str | No change required. The vCenter '`vcenter_ip`' has already been added to the Rubrik cluster. |
| tuple | The full API response for `POST /v1/vmware/vcenter` and the job status URL which can be used to monitor progress of the adding the vCenter to the Rubrik cluster. \(api\_response, job\_status\_url\) |

## Example

```python
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vcenter_ip = "demo-vcsa.python.demo"
vcenter_username = "pythonuser"
vcenter_password = "python123!"


add_vcenter, url = rubrik.add_vcenter(vcenter_ip, vcenter_username, vcenter_password)
```

