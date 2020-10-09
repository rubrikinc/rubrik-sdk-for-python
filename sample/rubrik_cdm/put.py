import rubrik_cdm

rubrik = rubrik_cdm.Connect()


config = {}
config['loginBanner'] = "Login Banner for the Python SDK Cluster"


set_login_banner = rubrik.put('internal', '/cluster/me/login_banner', config)