# log

Create properly formatted debug log messages.
```py
def log(log_message)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| log_message  | str  | The message to pass to the debug log. |         |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect(enable_logging=True)

rubrik.log('Python SDK')
```