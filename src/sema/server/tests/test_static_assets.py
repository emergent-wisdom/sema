import pytest

pytest.importorskip("fastapi")

from fastapi.testclient import TestClient

from sema.server.api import app


def test_missing_asset_does_not_return_spa_html():
    response = TestClient(app).get("/assets/does-not-exist.js")

    assert response.status_code == 404
    assert "text/html" not in response.headers.get("content-type", "")
