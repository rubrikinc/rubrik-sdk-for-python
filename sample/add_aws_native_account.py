import rubrik_cdm
rubrik = rubrik_cdm.Connect()

name = 'pythonsdkdemo'
accessKey = 'AWS_ACCESS_KEY'
secretKey = 'AWS_SECRET_KEY'
regions = ['us-east-1']

regional_bolt_network_configs = [
    {
        "region": "us-east-1", 
        "vNetId": "vpc-a46e72c2",
        "subnetId": "subnet-f0cc9695", 
        "securityGroupId": "sg-66091b19"
    }
]

nativeaccount = rubrik.add_aws_native_account(name, accessKey, secretKey, regions, regional_bolt_network_configs)
