import boto3
from botocore.exceptions import ClientError
import uuid
from app.config import S3_ACCESS_KEY, S3_SECRET_KEY, S3_BUCKET, S3_REGION



class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=S3_ACCESS_KEY,
            aws_secret_access_key=S3_SECRET_KEY,
            region_name=S3_REGION,
        )
        self.bucket_name = S3_BUCKET

    def upload_image(self, file, user_id):
        file_name = file.filename
        file_extenstion = file_name.split(".")[-1]
        unique_finename = f"user_{user_id}/{uuid.uuid4()}.{file_extenstion}"

        try:
            self.s3_client.upload_fileobj(
                file.file,
                self.bucket_name,
                unique_finename,
                ExtraArgs={"ContentType": file.content_type},
            )

            location = self.s3_client.get_bucket_location(Bucket=self.bucket_name)[
                "LocationConstraint"
            ]
            location_prefix = f".{location}" if location else ""
            url = f"https://{self.bucket_name}.s3{location_prefix}.amazonaws.com/{unique_finename}"

            return url
        except ClientError as e:
            print(f"S3 Upload Error: {e}")
            return None

    def delete_image(self, image_url):
        try:
            key = image_url.split("amazonaws.com/")[-1]
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
            return True
        except ClientError as e:
            print(f"S3 Delete Error: {e}")
            return False


s3_service = S3Service()
