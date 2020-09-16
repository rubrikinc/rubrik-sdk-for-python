import rubrik_cdm

rubrik = rubrik_cdm.Connect()

storage_account_name = "pythonsdkdemo"
container = "pythonsdkdemocontainer"
archive_name = "Azure:{}".format(container)

application_id = "385d0378-6ea2-872c-8fa2-c8376563e3a9"
application_key = "QeSO3Easf9fGasssLdaQrRNYa+jr5Eeae9daz9GvCduc="
tenant_id = "8391b522-1988-40ee-2912-8a85782093cb"
region = "centralus"
virtual_network_id = "/subscriptions/89b90dec-a6e1-4q9e-bc12-23138bb3cee4/resourceGroups/PythonSDK/providers" \
                     "/Microsoft.Network/virtualNetworks/pythonsdk"
subnet_name = "default"  # name of virtual network
security_group_id = "/subscriptions/89b90dec-a6e1-4q9e-bc12-23138bb3cee4/resourceGroups/PythonSDK/providers/Microsoft" \
                    ".Network/networkSecurityGroups/pythonsdk"

cloudon = rubrik.azure_cloudon(archive_name, container, storage_account_name, application_id,
                               application_key, tenant_id, region, virtual_network_id, subnet_name, security_group_id)
