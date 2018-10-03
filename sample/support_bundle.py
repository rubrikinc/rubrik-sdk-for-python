import rubrik_cdm

rubrik = rubrik_cdm.Connect()

events = rubrik.get_events(
    limit=10,
    event_type="Backup",
    status="Failure"
)

rubrik.support_bundle(events=events)
