# support_bundle_backlog

Process all EventIDs with pending `SUPPORT_BUNDLE_GENERATOR` jobs.
```py
def support_bundle_backlog()
```

## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

rubrik.support_bundle_backlog()
```