import rubrik

rubrik = rubrik.Connect()

with open("/home/python-sdk-demo/rubrik_encryption_key.pem") as rsa_pem:
    rsa_key = rsa_pem.read()

archive_name = "AWS:S3:rubrikpythonsdk"
vpc_id = 'vpc-8d80iii9'
subnet_id = 'subnet-125b5q79'
security_group_id = 'sg-f31bb489'

cloudon = rubrik.aws_s3_cloudon(archive_name, vpc_id, subnet_id, security_group_id)
