# log

Create properly formatted debug log messages.

```python
def log(self, log_message):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| log\_message | str | The message to pass to the debug log. |  |

## Example

```python
import rubrik_cdm

rubrik = rubrik_cdm.Connect(enable_logging=True)

rubrik.log('Python SDK')
```

