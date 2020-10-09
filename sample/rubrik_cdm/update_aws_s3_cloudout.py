import rubrik_cdm

rubrik = rubrik_cdm.Connect()

# s3:current-archive-name references an existing S3 archive on rubrik, the below example changes the name,
# rotates the access key and secret key, and changes the storage class to one zone IA
update_status = rubrik.update_aws_s3_cloudout("s3:current-archive-name", new_archive_name="s3:new-archive-name",
                                              aws_access_key="01234567890ABCDEFGHI",
                                              aws_secret_key="Th1s1sAnewS3cretKey", storage_class="onezone_ia")
