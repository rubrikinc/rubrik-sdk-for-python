# support_bundle

Generate/Download a Support Bundle for the specified EventID(s).
```py
def support_bundle(event_id=None, events=None)
```

## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| event_id  | str  | EventID (`eventSeriesId`) to generate a Support Bundle for. |         |         |
| events  | dict  | Dictionary of events returned by the `Events.get_events` method. |         |         |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

events = rubrik.get_events(
    limit=10,
    event_type="Backup",
    status="Failure"
)

rubrik.support_bundle(events=events)
```