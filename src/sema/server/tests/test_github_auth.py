import pytest

pytest.importorskip("fastapi")

from fastapi.testclient import TestClient

from sema.server import api


def test_me_reports_missing_github_config(monkeypatch):
    monkeypatch.delenv("GITHUB_CLIENT_ID", raising=False)
    monkeypatch.delenv("GITHUB_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("SEMA_SESSION_SECRET", raising=False)
    monkeypatch.delenv("SESSION_SECRET", raising=False)

    response = TestClient(api.app).get(
        "/api/me",
        headers={"host": "sema.example", "x-forwarded-proto": "https"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "authenticated": False,
        "user": None,
        "github_oauth_configured": False,
        "session_configured": False,
        "github_callback_url": "https://sema.example/auth/github/callback",
    }


def test_github_auth_start_redirects_when_config_is_missing(monkeypatch):
    monkeypatch.delenv("GITHUB_CLIENT_ID", raising=False)
    monkeypatch.delenv("GITHUB_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("SEMA_SESSION_SECRET", raising=False)
    monkeypatch.delenv("SESSION_SECRET", raising=False)

    response = TestClient(api.app).get("/auth/github/start", follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/workspace?auth=missing"


def test_me_treats_non_ascii_cookie_as_logged_out(monkeypatch):
    """A corrupted cookie must read as logged-out, not crash with a 500."""
    monkeypatch.setenv("SEMA_SESSION_SECRET", "test-session-secret")

    raw_cookie = f"{api._SESSION_COOKIE}=payload\xe9garbage.signature".encode("latin-1")
    response = TestClient(api.app).get("/api/me", headers={b"cookie": raw_cookie})

    assert response.status_code == 200
    assert response.json()["authenticated"] is False


def test_me_treats_tampered_signature_as_logged_out(monkeypatch):
    monkeypatch.setenv("SEMA_SESSION_SECRET", "test-session-secret")
    session = api._encode_session({"id": 1, "login": "octocat"})
    tampered = session[:-2] + "xx"

    response = TestClient(api.app).get("/api/me", cookies={api._SESSION_COOKIE: tampered})

    assert response.status_code == 200
    assert response.json()["authenticated"] is False


def test_me_reads_signed_session_cookie(monkeypatch):
    monkeypatch.setenv("SEMA_SESSION_SECRET", "test-session-secret")
    user = {
        "id": 1,
        "login": "octocat",
        "name": "The Octocat",
        "avatar_url": "https://github.com/images/error/octocat_happy.gif",
        "html_url": "https://github.com/octocat",
        "email": "octocat@example.com",
    }
    session = api._encode_session(user)

    response = TestClient(api.app).get("/api/me", cookies={api._SESSION_COOKIE: session})

    assert response.status_code == 200
    assert response.json()["authenticated"] is True
    assert response.json()["user"] == user
