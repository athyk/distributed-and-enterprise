import unittest
from unittest.mock import patch, MagicMock
import os
from backend.chat.server import Service, serve


class ChatTestCase(unittest.TestCase):
    def test_SendMessage_returns_success_response(self):
        """
        Fake a message request and test if SendMessage returns the expected response.
        :return:
        """
        service = Service()
        request = MagicMock()
        request.message = "Test message"
        context = MagicMock()

        response = service.SendMessage(request, context)

        self.assertTrue(response.success)
        self.assertEqual(response.message, "Hello, Test message!")
        self.assertEqual(response.error, '')
        print("TestService.SendMessage_returns_success_response PASSED")

    @patch('backend.chat.server.grpc.server')
    @patch('backend.chat.server.futures.ThreadPoolExecutor')
    def test_serve_starts_server_on_default_port(self, mock_executor, mock_grpc_server):
        """
        Test if serve starts the server on default port 50051.
        :return:
        """
        os.environ.pop('CHAT_PORT', None)
        os.environ.pop('CHAT_MAX_WORKERS', None)

        serve()

        mock_grpc_server.assert_called_once()
        mock_grpc_server.return_value.add_insecure_port.assert_called_once_with('[::]:50051')
        mock_grpc_server.return_value.start.assert_called_once()
        mock_grpc_server.return_value.wait_for_termination.assert_called_once()

    @patch('backend.chat.server.grpc.server')
    @patch('backend.chat.server.futures.ThreadPoolExecutor')
    def test_serve_starts_server_on_custom_port(self, mock_executor, mock_grpc_server):
        """"
        Test if serve starts the server on custom port 12345.
        """
        os.environ['CHAT_PORT'] = '12345'
        os.environ['CHAT_MAX_WORKERS'] = '5'

        serve()

        mock_grpc_server.assert_called_once()
        mock_grpc_server.return_value.add_insecure_port.assert_called_once_with('[::]:12345')
        mock_grpc_server.return_value.start.assert_called_once()
        mock_grpc_server.return_value.wait_for_termination.assert_called_once()


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
