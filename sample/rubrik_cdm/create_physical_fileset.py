import rubrik_cdm

rubrik = rubrik_cdm.Connect()

name = "Python SDK"
operating_system = 'Linux'
include = ['/usr/local', '*.pdf']
exclude = ['/user/local/temp', '*.mov', '*.mp3']
exclude_exception = ['/company/*.mp4']

new_fileset = rubrik.create_physical_fileset(name, operating_system, include, exclude, exclude_exception)
