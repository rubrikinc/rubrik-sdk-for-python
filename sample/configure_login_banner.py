import rubrik_cdm

rubrik = rubrik_cdm.Connect()

bannerText = "Welcome To Rubrik"
configure_ntp = rubrik.configure_login_banner(bannerText)
