import unittest
from app import app

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_get_books(self):
        result = self.app.get('/books?query=harry')
        self.assertEqual(result.status_code, 200)

    def test_missing_query_parameters(self):
        result = self.app.get('/books')
        self.assertEqual(result.status_code, 422)

    def test_get_book_by_isbn(self):
        result = self.app.get('/book/0451526538')
        self.assertEqual(result.status_code, 200)

    def test_book_not_found(self):
        result = self.app.get('/book/invalid_isbn')
        self.assertEqual(result.status_code, 404)

if __name__ == '__main__':
    unittest.main()

