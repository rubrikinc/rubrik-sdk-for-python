import rubrik_cdm

rubrik = rubrik_cdm.Connect()

archive_name = "AWS:S3:rubrikpythonsdk"
vpc_id = 'vpc-8d80iii9'
subnet_id = 'subnet-125b5q79'
security_group_id = 'sg-f31bb489'
enable_archive_consolidation = True

cloudon = rubrik.aws_s3_cloudon(archive_name, vpc_id, subnet_id, security_group_id, enable_archive_consolidation)
