# end_user_authorization

Grant an End User authorization to the provided object.
```py
def end_user_authorization(object_name, end_user, object_type='vmware', timeout=15)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| object_name  | str  | The name of the object you wish to grant authorization to. |         |
| end_user  | str  | The name of the end user you wish to grant authorization to. |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| object_type  | str  | The Rubrik object type you wish to backup. `vmware` is currently the only supported option. (choices: {vmware})  |    vmware (default: {vmware     |    vmware     |
| timeout  | int  | The timeout value for the API call that grants the End User authoriauthorizationation.  |         |    15     |

## Returns
| Type | Description                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | If the End User is already authorized to interact with the provided object name the following is returned: The End User "{`end_user`}" is already authorized to interact with the "{`object_name`}" VM. |
| dict  | The full response for the `/internal//authorization/role/end_user` API endpoint. |
