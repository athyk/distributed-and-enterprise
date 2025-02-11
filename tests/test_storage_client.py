import unittest
from unittest.mock import patch, MagicMock
from django.core.files.uploadedfile import SimpleUploadedFile
from common.files import StorageClient


class StorageClientTestCase(unittest.TestCase):

    @patch("boto3.client")
    def setUp(self, mock_boto_client):
        """
        Setup mock StorageClient instance before each test.
        """
        self.mock_s3 = MagicMock()
        mock_boto_client.return_value = self.mock_s3

        StorageClient.initialise(
            endpoint_url="http://test-minio:9000",
            access_key="test-access",
            secret_key="test-secret",
            bucket_name="test-bucket",
            public_url="http://test-minio:9000"
        )

        self.client = StorageClient()
        StorageClient._initialise(self.client)

    def test_singleton_instance(self):
        """Ensure that StorageClient follows singleton pattern, i.e. only one instance is created"""
        client1 = StorageClient()
        client2 = StorageClient()
        self.assertIs(client1, client2)

    def test_upload_file(self):
        test_file = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")

        self.mock_s3.upload_fileobj.return_value = None

        uploaded_url = self.client.upload_file(test_file)
        self.assertIsNotNone(uploaded_url)
        self.assertTrue(uploaded_url.startswith("http://test-minio:9000/test-bucket/"))
        self.mock_s3.upload_fileobj.assert_called_once() # Ensure upload was called

    def test_upload_file_with_error(self):
        test_file = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        self.mock_s3.upload_fileobj.side_effect = Exception("Upload failed")

        uploaded_url = self.client.upload_file(test_file)
        self.assertIsNone(uploaded_url)

    def test_get_url(self):
        expected_url = "http://test-minio:9000/test-bucket/test-file.jpg"
        self.assertEqual(self.client._get_url("test-file.jpg"), expected_url)

    def test_delete_file(self):
        self.client.delete_file("test-file.jpg")
        self.mock_s3.delete_object.assert_called_once_with(Bucket="test-bucket", Key="test-file.jpg")

    def test_replace_file(self):
        test_file = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")

        # Mock S3 upload response
        self.mock_s3.upload_fileobj.return_value = None

        uploaded_url = self.client.replace_file("test.jpg", test_file)
        self.assertIsNotNone(uploaded_url)
        self.assertTrue(uploaded_url.startswith("http://test-minio:9000/test-bucket/"))
        self.mock_s3.upload_fileobj.assert_called_once()

    def test_uninitialised_client(self):
        """Ensure StorageClient raises an error if not initialised"""
        StorageClient._instance = None  # Reset singleton, so we can try to re-initialise
        StorageClient._config = {}  # Clear config within StorageClient
        with self.assertRaises(ValueError):
            StorageClient()


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
