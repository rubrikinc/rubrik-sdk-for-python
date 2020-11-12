import rubrik_cdm

rubrik = rubrik_cdm.Connect()

name = "Python SDK"
share_type = 'NFS'
include = ['/usr/local', '*.pdf']
exclude = ['/user/local/temp', '*.mov', '*.mp3', '*.mp4']
exclude_exception = ['/company/*.mp4']

new_fileset = rubrik.create_nas_fileset(name, share_type, include, exclude, exclude_exception)
