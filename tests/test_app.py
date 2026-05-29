import unittest

from app import create_app
from app.extensions import validate_supabase_config


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


class HealthCheckTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

    def test_health_endpoint_returns_json(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["supabase"], "disconnected")


class ConfigValidationTests(unittest.TestCase):
    def test_valid_config_returns_no_issues(self):
        issues = validate_supabase_config(
            "https://myproject.supabase.co",
            "a-valid-key-that-is-longer-than-twenty-characters",
        )
        self.assertEqual(issues, [])

    def test_non_https_url_flagged(self):
        issues = validate_supabase_config(
            "http://myproject.supabase.co", "a-valid-key-longer-than-20"
        )
        self.assertIn("SUPABASE_URL should use HTTPS.", issues)

    def test_short_key_flagged(self):
        issues = validate_supabase_config(
            "https://myproject.supabase.co", "short"
        )
        self.assertIn("SUPABASE_KEY appears too short to be a valid key.", issues)

    def test_empty_values_no_issues(self):
        """Empty values are fine — means offline mode."""
        issues = validate_supabase_config("", "")
        self.assertEqual(issues, [])


if __name__ == "__main__":
    unittest.main()
