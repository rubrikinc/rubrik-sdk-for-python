# get_all_hosts

Gets information regarding every Rubrik host in the cluster.
```py
def get_all_hosts(timeout=60)
```


## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| dict  | The result of the API call `GET /host` |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

result = rubrik.get_all_hosts()
```