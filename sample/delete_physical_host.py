import rubrik

rubrik = rubrik.Connect()

hostname = "python-sdk-demo"

delete_host = rubrik.delete_physical_host(hostname)
