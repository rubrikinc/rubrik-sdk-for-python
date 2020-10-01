# update\_aws\_native\_account

Update an exsiting AWS account used for EC2 native protection on the Rubrik cluster.

```python
def update_aws_native_account(self, aws_account_name, config, timeout=15):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| aws\_account\_name | str | The name of the AWS account you wish to update. This is the name that is displayed in the Rubrik UI. |  |

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| config | dict | The configuration to use to update the AWS account. Full example values can be found in the Rubrik API Playground for the PATCH /aws/account/{id} endpoint |  |  |
| timeout | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |  | 15 |

## Returns

| Type | Return Value |
| :--- | :--- |
| dict | The full API response for `PATCH /aws/account/{id}`. |

## Example

```python
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

current_aws_account_name = "Python"

config = {}
config["name"] = "Python-AWS-Demo"

update_native = rubrik.update_aws_native_account(current_aws_account_name, config)
```

