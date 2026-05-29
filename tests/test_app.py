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
        self.assertIn(b"Project Title", response.data)
        self.assertIn(b"Student Name", response.data)

    def test_placeholder_detail_page_loads(self):
        response = self.client.get("/students/placeholder-project")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Student:", response.data)

    def test_unknown_student_slug_returns_404(self):
        response = self.client.get("/students/missing-slug")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
