import rubrik_cdm

rubrik = rubrik_cdm.Connect()

managed_volume_name = 'MV1'

begin_snapshot = rubrik.begin_managed_volume_snapshot(managed_volume_name)

print(begin_snapshot)
