import unittest

from app import create_app


class AppFactoryTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Featured Work", response.data)

    def test_placeholder_detail_page_loads(self):
        response = self.client.get("/students/placeholder-project")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Student:", response.data)


if __name__ == "__main__":
    unittest.main()
