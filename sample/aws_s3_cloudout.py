import rubrik

rubrik = rubrik.Connect()

with open("/home/python-sdk-demo/rubrik_encryption_key.pem") as rsa_pem:
    rsa_key = rsa_pem.read()

aws_bucket_name = 'rubrikpythonsdk'

# AWS_DEFAULT_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY are being read from environment variables
cloudout = rubrik.aws_s3_cloudout(aws_bucket_name, rsa_key=rsa_key)
