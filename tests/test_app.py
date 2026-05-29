"""Tests for application factory, health check, and config validation."""

import pytest

from app.extensions import validate_supabase_config


# -- App factory / route tests --


class TestHomePage:
    def test_home_page_loads(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert b"Student projects" in response.data
        assert b"Project Title" in response.data
        assert b"Student Name" in response.data


class TestStudentDetail:
    def test_placeholder_detail_page_loads(self, client):
        response = client.get("/students/placeholder-project")
        assert response.status_code == 200
        assert b"Student Name" in response.data

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
        assert data["supabase"] == "disconnected"


# -- Config validation tests --


class TestConfigValidation:
    def test_valid_config_returns_no_issues(self):
        issues = validate_supabase_config(
            "https://myproject.supabase.co",
            "a-valid-key-that-is-longer-than-twenty-characters",
        )
        assert issues == []

    def test_non_https_url_flagged(self):
        issues = validate_supabase_config(
            "http://myproject.supabase.co", "a-valid-key-longer-than-20"
        )
        assert "SUPABASE_URL should use HTTPS." in issues

    def test_short_key_flagged(self):
        issues = validate_supabase_config(
            "https://myproject.supabase.co", "short"
        )
        assert "SUPABASE_KEY appears too short to be a valid key." in issues

    def test_empty_values_no_issues(self):
        """Empty values are fine — means offline mode."""
        issues = validate_supabase_config("", "")
        assert issues == []
