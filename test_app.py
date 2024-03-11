import unittest
from app import index, plural_forms, autopct_format
from unittest.mock import patch, MagicMock

class TestApp(unittest.TestCase):

    @patch('app.NewsApiClient')
    def test_index(self, mock_api):
        # Mock the NewsApiClient
        mock_api.return_value.get_everything.return_value = {
            'articles': [
                {'title': 'Test Title', 'content': 'Test Content'}
            ]
        }

        # Call the index function
        result = index()

        # Assert that the function returns the expected result
        self.assertIn('Test Title', result)

    def test_plural_forms(self):
        # Test the plural_forms function
        result = plural_forms('test')
        expected_result = ['test', 'tests', 'testes', 'testies', 'testves']
        self.assertEqual(result, expected_result)

    def test_autopct_format(self):
        # Test the autopct_format function
        result = autopct_format([10, 90])
        self.assertEqual(result(10), '10.0%')
        self.assertEqual(result(1), '')

if __name__ == '__main__':
    unittest.main()