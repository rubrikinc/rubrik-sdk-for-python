import rubrik_cdm

rubrik = rubrik_cdm.Connect()

host = "proxy.python.demo"
protocol = "HTTPS"
port = 443

update_proxy = rubrik.update_proxy(host, protocol, port)