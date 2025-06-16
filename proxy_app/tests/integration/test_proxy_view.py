from django.test import TestCase, Client
from unittest.mock import patch, MagicMock
import httpx

class ProxyViewIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('proxy_app.views.get_target_backend')
    @patch('proxy_app.views.httpx')
    def test_proxy_success(self, mock_httpx_module, mock_get_target):
        # 1. Stub out routing to a fake backend
        mock_get_target.return_value = "http://backend.test"

        # 2. Create a fake httpx.Client() context manager
        fake_client = MagicMock()
        fake_response = httpx.Response(
            status_code=200,
            content=b"Hello from backend",
            headers={"content-type": "text/plain"}
        )
        fake_client.request.return_value = fake_response

        # httpx.Client() returns a context manager whose __enter__() is our fake_client
        mock_httpx_module.Client.return_value.__enter__.return_value = fake_client

        # 3. Perform a GET against any path
        response = self.client.get('/some/path/')

        # 4. Assert proxy forwarded correctly
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Hello from backend")
        self.assertEqual(response['Content-Type'], 'text/plain')

    @patch('proxy_app.views.get_target_backend')
    def test_proxy_no_rule(self, mock_get_target):
        mock_get_target.return_value = None

        response = self.client.post('/no/match/', data={'foo': 'bar'})

        self.assertEqual(response.status_code, 404)
        # JSON response with proper error message
        self.assertJSONEqual(
            response.content,
            {"error": "No matching routing rule"}
        )
