# end_user_authorization

Grant an End User authorization to the provided object.
```py
def end_user_authorization(object_name, end_user, object_type='vmware', timeout=15)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| object_name  | str  | The name of the object you wish to grant the `end_ser` authorization to. |         |
| end_user  | str  | The name of the end user you wish to grant authorization to. |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| object_type  | str  | The Rubrik object type you wish to backup.  |    vmware     |    vmware      |
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    15     |

## Returns
| Type | Description                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | 'No change required. The End User "`end_user`" is already authorized to interact with the "`object_name`" VM.'.format(end_user, object_name) |
| dict  | dict -- The API response from `POST /internal/authorization/role/end_user`. |
