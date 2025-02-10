import typing
import uuid

import boto3
import threading

import django.core.files


class StorageClient:
    _instance = None
    _lock = threading.Lock()

    _config = {}

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(StorageClient, cls).__new__(cls)
                cls._instance._initialise()
        return cls._instance

    @classmethod
    def initialise(cls, endpoint_url: str, access_key: str, secret_key: str, bucket_name: str, public_url: str):
        """
        Set the configuration for StorageClient.

        :param endpoint_url: URL of the MinIO server, points to the minio instance
        :param access_key: Access key for MinIO/root user
        :param secret_key: Secret key for MinIO/root user password
        :param bucket_name: Name of the bucket to use, such as "uni-hub"
        :param public_url: Public URL for the MinIO server or CDN
        """
        cls._config = {
            "endpoint_url": endpoint_url,
            "access_key": access_key,
            "secret_key": secret_key,
            "bucket_name": bucket_name,
            "public_url": public_url,
        }

    def _initialise(self):
        """
        Initialise the S3 client and create the bucket if it doesn't exist.
        """
        if not self._config:
            raise ValueError("StorageClient not initialised")

        self._endpoint_url = self._config["endpoint_url"]
        self._bucket_name = self._config["bucket_name"]
        self._public_url = self._config["public_url"]

        self._s3_client = boto3.client(
            "s3",
            endpoint_url=self._config["endpoint_url"],
            aws_access_key_id=self._config["access_key"],
            aws_secret_access_key=self._config["secret_key"]
        )

        if self._bucket_name not in [bucket["Name"] for bucket in self._s3_client.list_buckets()["Buckets"]]:
            self._s3_client.create_bucket(Bucket=self._bucket_name)

        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": ["s3:GetObject"],
                    "Resource": [f"arn:aws:s3:::{self._bucket_name}/*"]
                }
            ]
        }

        self._s3_client.put_bucket_policy(
            Bucket=self._bucket_name,
            Policy=str(bucket_policy).replace("'", '"')  # JSON requires double quotes
        )

    def upload_file(self, file: django.core.files.File) -> typing.Optional[str]:
        """
        Upload a file. This will auto generate a unique filename.

        Ensure a file extension is present in the file name.

        :param file: A django.core.files.File object to upload.
        :return: The public URL of the uploaded file, or None if the upload failed.
        """
        file_extension = file.name.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        s3_key = f"{unique_filename}"

        try:
            self._s3_client.upload_fileobj(file, self._bucket_name, s3_key, ExtraArgs={
                'ACL': 's3:GetObject'
            })
        except Exception as e:
            print(f"Error uploading file: {e}")
            return None

        return self._get_url(s3_key)

    def _get_url(self, object_name: str):
        """Generate a public URL for an object."""
        return f"{self._public_url}/{self._bucket_name}/{object_name}"

    def delete_file(self, object_name: str) -> None:
        """
        Delete a file.

        :param object_name: The name of the object to delete. For example: example.png
        :return:
        """
        self._s3_client.delete_object(Bucket=self._bucket_name, Key=object_name)

    def replace_file(self, old_object_name, file: django.core.files.File) -> typing.Optional[str]:
        """
        Replace an existing file name with a new file.

        :param old_object_name: The name of the object to delete. For example: example.png
        :param file: A django.core.files.File object to upload.
        :return: The public URL of the new file, or None if the upload failed.
        """
        self.delete_file(old_object_name)
        return self.upload_file(file)
