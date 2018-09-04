import rubrik

rubrik = rubrik.Connect()

hostname = "python-sdk-demo"

add_host = rubrik.add_physical_host(hostname)
