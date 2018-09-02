import rubrik

rubrik = rubrik.Connect()

with open("/home/vagrant/Development/Python/rubrik-sdk-for-python/sample/rubrik_encryption_key.pem") as rsa_pem:
    rsa_key = rsa_pem.read()

storage_account_name = "pythonsdkdemo"
container = "pythonsdkdemocontainer"
azure_access_key = "ze=AIHW/Y2a7bee1MXXJelpN2clVa8E=YEw/IsCQE/LAecnyeeUMF6I/9mIi27oRBjyuiespqUHT928jW+TiWYA=="

cloudout = rubrik.azure_cloudout(container, azure_access_key, storage_account_name, rsa_key)
