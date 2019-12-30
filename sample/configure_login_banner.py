import rubrik_cdm

rubrik = rubrik_cdm.Connect()

bannerText = "Testing Banner Configuration"
configure_ntp = rubrik.configure_login_banner(bannerText)
