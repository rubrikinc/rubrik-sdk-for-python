import rubrik_cdm

rubrik = rubrik_cdm.Connect()

timezone = "America/Chicago"

configure_timezone = rubrik.configure_timezone(timezone)
