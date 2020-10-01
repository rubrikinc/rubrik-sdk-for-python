import rubrik_cdm

rubrik = rubrik_cdm.Connect()

# Monitor the progress of a On-Demand Snapshot
job_status_url = "https://172.21.8.52/api/v1/vmware/vm/request/CREATE_VMWARE_SNAPSHOT_fase1f32-3872-2982-a68c" \
                 "-6fe145982f48-vm-5008_f7c393f3-383-4b44-920-8cde7a9ae2bd:::0"

snapshot_status = rubrik.job_status(job_status_url)
