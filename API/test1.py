import unittest
from fastapi.testclient import TestClient
from main import app

class TestAPIEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app=app) 

    def test_root_endpoint(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'This is home page.'})

    def test_search_repo_endpoint_success(self):
        # Providing a valid repository URL
        repo_url = 'https://github.com/1md3nd/AI-Github-Code-Review/'
        response = self.client.get(f'/searchRepo?repo_url={repo_url}')
        self.assertEqual(response.status_code, 200)
        # Ensure 'files_data' and 'cumulative_res' keys exist in the response JSON
        self.assertIn('files_data', response.json())
        self.assertIn('cumulative_res', response.json())

    def test_search_repo_endpoint_missing_url(self):
        # Not providing a repository URL
        response = self.client.get('/searchRepo')
        self.assertEqual(response.status_code, 400)
        # Ensure the response contains the expected error message
        self.assertIn('Repository URL not provided', response.text)

    def test_search_repo_endpoint_invalid_url(self):
        # Providing an invalid repository URL
        invalid_repo_url = 'invalid_url'
        response = self.client.get(f'/searchRepo?repo_url={invalid_repo_url}')
        self.assertEqual(response.status_code, 400)
        # Ensure the response contains the expected error message
        self.assertIn('Invalid repository URL provided', response.text)

if __name__ == '__main__':
    unittest.main()
