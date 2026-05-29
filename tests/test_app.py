"""Tests for application factory and health check."""


# -- App factory / route tests --


class TestHomePage:
    def test_home_page_loads(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert b"My projects" in response.data
        assert b"Your First Project" in response.data
        assert b"Hi, I'm" in response.data


class TestStudentDetail:
    def test_placeholder_detail_page_loads(self, client):
        response = client.get("/students/placeholder-project")
        assert response.status_code == 200
        assert b"Your First Project" in response.data

    def test_unknown_student_slug_returns_404(self, client):
        response = client.get("/students/missing-slug")
        assert response.status_code == 404


# -- Health check tests --


class TestHealthCheck:
    def test_health_endpoint_returns_json(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "healthy"
        assert data["projects"] == "available"
