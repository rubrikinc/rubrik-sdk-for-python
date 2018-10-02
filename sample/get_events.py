import rubrik_cdm

rubrik = rubrik_cdm.Connect()

events = rubrik.get_events()
