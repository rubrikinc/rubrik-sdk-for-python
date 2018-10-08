import rubrik_cdm

rubrik = rubrik_cdm.Connect()

managed_volume_name = 'MV1'

end_snapshot = rubrik.end_managed_volume_snapshot(managed_volume_name)

print(end_snapshot)
