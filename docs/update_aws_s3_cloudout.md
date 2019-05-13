# update_aws_s3_cloudout

Update an AWS S3 archival location on the Rubrik cluster.
```py
def update_aws_s3_cloudout(current_archive_name, new_archive_name=None, aws_access_key=None, aws_secret_key=None, storage_class=None, timeout=180)
```

## Keyword Arguments
| Name                 | Type | Description                                                                                                                           | Choices                                               | Default |
|----------------------|------|---------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|---------|
| current_archive_name | str  | The name of the current archive to be updated.                                                                                        |                                                       |         |
| new_archive_name     | str  | Desired name for the updated archive location. If set to default `None` keyword argument, no change will be made.                     |                                                       | None    |
| aws_access_key       | str  | The access key of a AWS account with the required permissions. If set to the default `None` keyword argument, no change will be made. |                                                       | None    |
| aws_secret_key       | str  | The secret key of a AWS account with the required permissions. If set to the default `None` keyword argument, no change will be made. |                                                       | None    |
| storage_class        | str  | The AWS storage class you wish to use. If set to the default `None` keyword argument, no change will be made.                         | standard, standard_ia, reduced_redundancy, onezone_ia | None    |
| timeout              | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.                          |                                                       | 180     |

## Returns
| Type | Return Value                                                            |
|------|-------------------------------------------------------------------------|
| dict | The full API response for `PATCH /internal/archive/object_store/{id}'`. |

## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

# s3:current-archive-name references an existing S3 archive on rubrik, the below example changes the name, rotates the access key and secret key, and changes the storage class to one zone IA
update_status = rubrik.update_aws_s3_cloudout("s3:current-archive-name", new_archive_name="s3:new-archive-name", aws_access_key="01234567890ABCDEFGHI", aws_secret_key="Th1s1sAnewS3cretKey", storage_class="onezone_ia")
```