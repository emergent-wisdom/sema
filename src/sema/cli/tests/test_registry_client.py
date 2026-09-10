"""Device login and registry commands against a mocked hosted registry."""

from __future__ import annotations

import json
import os
import stat

import httpx
import pytest

from sema.cli import registry_client as rc

REGISTRY = "https://registry.test"
MANIFEST = "https://github.com/alice/reasoning/releases/latest/download/library.json"


class FakeRegistry:
    """The server side of the device flow, with a scripted approval."""

    def __init__(self, *, pending_polls: int = 1, decision: str = "approved"):
        self.pending_polls = pending_polls
        self.decision = decision
        self.requests: list[httpx.Request] = []
        self.token = "sema_" + "t" * 43
        self.revoked: list[str] = []

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        path = request.url.path
        auth = request.headers.get("authorization")
        if path == "/api/cli/device" and request.method == "POST":
            body = json.loads(request.content)
            assert body["client"].startswith("sema ")
            return httpx.Response(
                200,
                json={
                    "device_code": "device-secret-0123456789",
                    "user_code": "ABCD-EFGH",
                    "verification_uri": f"{REGISTRY}/cli/authorize",
                    "verification_uri_complete": f"{REGISTRY}/cli/authorize?user_code=ABCD-EFGH",
                    "expires_in": 900,
                    "interval": 5,
                },
            )
        if path == "/api/cli/token" and request.method == "POST":
            assert json.loads(request.content) == {"device_code": "device-secret-0123456789"}
            if self.pending_polls > 0:
                self.pending_polls -= 1
                return httpx.Response(
                    400, json={"detail": {"error": "authorization_pending", "message": "wait"}}
                )
            if self.decision == "denied":
                return httpx.Response(
                    400, json={"detail": {"error": "access_denied", "message": "denied"}}
                )
            return httpx.Response(
                200,
                json={
                    "access_token": self.token,
                    "token_type": "bearer",
                    "expires_in": 7_776_000,
                    "token_id": "tok_0123456789abcdef",
                    "account": {"login": "alice"},
                },
            )
        if auth != f"Bearer {self.token}":
            return httpx.Response(401, json={"detail": "Invalid or revoked API token"})
        if path == "/api/me":
            return httpx.Response(200, json={"authenticated": True, "user": {"login": "alice"}})
        if path == "/api/registry/import" and request.method == "POST":
            assert json.loads(request.content) == {"manifest_url": MANIFEST}
            return httpx.Response(
                200,
                json={
                    "operation": "created",
                    "record": {
                        "library_id": "reasoning",
                        "version": "0.1.0",
                        "pattern_count": 3,
                        "root": "8cc3aa60" + "0" * 56,
                        "catalog_root": "9a9cb8d7" + "0" * 56,
                    },
                },
            )
        if path == "/api/me/libraries" and request.method == "GET":
            return httpx.Response(
                200,
                json=[
                    {
                        "library_id": "reasoning",
                        "version": "0.1.0",
                        "pattern_count": 3,
                        "root": "8cc3" * 16,
                    }
                ],
            )
        if path == "/api/me/libraries/reasoning" and request.method == "DELETE":
            return httpx.Response(200, json={"library_id": "reasoning", "deleted": True})
        if path.startswith("/api/me/tokens/") and request.method == "DELETE":
            self.revoked.append(path.rsplit("/", 1)[1])
            return httpx.Response(200, json={"revoked": True})
        return httpx.Response(404, json={"detail": "Not Found"})

    def client(self) -> httpx.Client:
        return httpx.Client(transport=httpx.MockTransport(self.handler), base_url=REGISTRY)


@pytest.fixture()
def config_home(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.delenv(rc.TOKEN_ENV, raising=False)
    monkeypatch.delenv(rc.REGISTRY_ENV, raising=False)
    return tmp_path / "config"


def test_login_polls_until_approved_and_stores_the_token_privately(config_home):
    server = FakeRegistry(pending_polls=2)
    lines: list[str] = []
    slept: list[float] = []
    with server.client() as client:
        result = rc.login(
            REGISTRY,
            http_client=client,
            open_browser=False,
            out=lines.append,
            sleep=slept.append,
            clock=lambda: 1_000_000.0,
        )

    assert result.login == "alice"
    assert result.registry == REGISTRY
    assert any("ABCD-EFGH" in line for line in lines)
    assert any("/cli/authorize?user_code=ABCD-EFGH" in line for line in lines)
    assert slept == [5, 5, 5]

    path = rc.credentials_path()
    assert path == config_home / "sema" / "credentials.json"
    assert stat.S_IMODE(path.stat().st_mode) == 0o600
    stored = json.loads(path.read_text())["registries"][REGISTRY]
    assert stored["token"] == server.token
    assert stored["login"] == "alice"
    assert stored["expires_at"] == 1_000_000 + 7_776_000
    assert rc.normalize_registry(None) == REGISTRY


def test_login_reports_denial_without_storing_anything(config_home):
    server = FakeRegistry(pending_polls=0, decision="denied")
    with server.client() as client, pytest.raises(rc.RegistryError, match="denied"):
        rc.login(
            REGISTRY,
            http_client=client,
            open_browser=False,
            out=lambda _line: None,
            sleep=lambda _s: None,
        )
    assert not rc.credentials_path().exists()


def test_login_gives_up_when_the_code_expires(config_home):
    server = FakeRegistry(pending_polls=99)
    ticks = iter([0.0, 0.0, 1000.0])
    with server.client() as client, pytest.raises(rc.RegistryError, match="expired"):
        rc.login(
            REGISTRY,
            http_client=client,
            open_browser=False,
            out=lambda _line: None,
            sleep=lambda _s: None,
            clock=lambda: next(ticks),
        )


def test_registry_commands_send_the_stored_bearer_token(config_home):
    server = FakeRegistry(pending_polls=0)
    lines: list[str] = []
    with server.client() as client:
        rc.login(
            REGISTRY,
            http_client=client,
            open_browser=False,
            out=lambda _line: None,
            sleep=lambda _s: None,
        )
        user = rc.whoami(http_client=client, out=lines.append)
        payload = rc.registry_import(MANIFEST, http_client=client, out=lines.append)
        rows = rc.registry_list(http_client=client, out=lines.append)
        assert rc.registry_remove("reasoning", http_client=client, out=lines.append)

    assert user["login"] == "alice"
    assert payload["operation"] == "created"
    assert rows[0]["library_id"] == "reasoning"
    assert any("Published reasoning v0.1.0 (3 patterns)" in line for line in lines)
    assert any("/vocabularies/reasoning" in line for line in lines)
    assert all(
        str(request.url).startswith(REGISTRY + "/")
        and request.headers.get("authorization") == f"Bearer {server.token}"
        for request in server.requests
        if request.url.path.startswith("/api/me") or request.url.path == "/api/registry/import"
    )


def test_environment_token_overrides_the_stored_login(config_home, monkeypatch):
    server = FakeRegistry()
    monkeypatch.setenv(rc.TOKEN_ENV, server.token)
    with server.client() as client:
        assert rc.whoami(REGISTRY, http_client=client, out=lambda _line: None)["login"] == "alice"


def test_commands_without_a_login_explain_how_to_log_in(config_home):
    server = FakeRegistry()
    with server.client() as client, pytest.raises(rc.RegistryError, match="sema login"):
        rc.registry_list(REGISTRY, http_client=client, out=lambda _line: None)


def test_logout_revokes_remotely_and_forgets_locally(config_home):
    server = FakeRegistry(pending_polls=0)
    with server.client() as client:
        rc.login(
            REGISTRY,
            http_client=client,
            open_browser=False,
            out=lambda _line: None,
            sleep=lambda _s: None,
        )
        assert rc.stored_credential(REGISTRY) is not None
        assert rc.logout(http_client=client, out=lambda _line: None)
    assert server.revoked == ["tok_0123456789abcdef"]
    assert rc.stored_credential(REGISTRY) is None
    assert rc.normalize_registry(None) == REGISTRY


def test_registry_urls_are_validated(config_home):
    assert rc.normalize_registry("https://semahash.org/") == "https://semahash.org"
    assert rc.normalize_registry("http://127.0.0.1:3000") == "http://127.0.0.1:3000"
    assert rc.normalize_registry(None) == rc.DEFAULT_REGISTRY
    with pytest.raises(rc.RegistryError, match="HTTPS"):
        rc.normalize_registry("http://registry.example")
    with pytest.raises(rc.RegistryError, match="Invalid registry URL"):
        rc.normalize_registry("https://registry.example/api")


def test_registry_env_selects_the_default(config_home, monkeypatch):
    monkeypatch.setenv(rc.REGISTRY_ENV, "https://mirror.example/")
    assert rc.normalize_registry(None) == "https://mirror.example"


def test_registry_precedence_preserves_existing_credentials(config_home, monkeypatch):
    # Credentials written by earlier clients remain valid without a saved default.
    rc._save_credentials({"registries": {REGISTRY: {"token": "original"}}})
    assert rc.normalize_registry(None) == rc.DEFAULT_REGISTRY
    assert rc.resolve_token(REGISTRY) == "original"

    rc.store_credential(REGISTRY, {"token": "original"})
    assert rc.normalize_registry(None) == REGISTRY
    monkeypatch.setenv(rc.REGISTRY_ENV, "https://environment.example")
    before = rc.credentials_path().read_bytes()
    assert rc.normalize_registry(None) == "https://environment.example"
    assert rc.normalize_registry("https://explicit.example") == "https://explicit.example"
    assert rc.credentials_path().read_bytes() == before
    monkeypatch.delenv(rc.REGISTRY_ENV)
    assert rc.normalize_registry(None) == REGISTRY


def test_failed_login_keeps_the_previous_registry(config_home):
    rc.store_credential("https://previous.example", {"token": "previous"})
    before = rc.credentials_path().read_bytes()
    server = FakeRegistry(pending_polls=0, decision="denied")
    with server.client() as client, pytest.raises(rc.RegistryError, match="denied"):
        rc.login(
            REGISTRY,
            http_client=client,
            open_browser=False,
            out=lambda _line: None,
            sleep=lambda _s: None,
        )
    assert rc.credentials_path().read_bytes() == before
    assert rc.normalize_registry(None) == "https://previous.example"


def test_switching_registry_keeps_tokens_separate(config_home, monkeypatch):
    previous = "https://previous.example"
    rc.store_credential(previous, {"token": "previous-token"})
    server = FakeRegistry(pending_polls=0)
    monkeypatch.setenv(rc.REGISTRY_ENV, REGISTRY)
    with server.client() as client:
        rc.login(
            http_client=client, open_browser=False, out=lambda _line: None, sleep=lambda _s: None
        )
    monkeypatch.delenv(rc.REGISTRY_ENV)
    assert rc.normalize_registry(None) == REGISTRY
    assert rc.resolve_token(previous) == "previous-token"

    def handler(request):
        expected = server.token if request.url.host == "registry.test" else "previous-token"
        assert request.headers["authorization"] == f"Bearer {expected}"
        return httpx.Response(200, json=[])

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        assert rc.registry_list(http_client=client, out=lambda _line: None) == []
        assert rc.registry_list(previous, http_client=client, out=lambda _line: None) == []
    assert rc.normalize_registry(None) == REGISTRY


@pytest.mark.parametrize("remembered", [False, 123, "", "http://remote.example"])
def test_invalid_saved_registry_never_silently_falls_back(config_home, remembered):
    rc._save_credentials({"registries": {}, "default_registry": remembered})
    with pytest.raises(rc.RegistryError):
        rc.normalize_registry(None)
    assert rc.normalize_registry(REGISTRY) == REGISTRY


def test_credentials_are_private_before_any_permission_change(config_home, monkeypatch):
    original_chmod = os.chmod

    def require_already_private(path, mode):
        # A chmod after token contents have been written must not close a prior exposure.
        assert stat.S_IMODE(path.stat().st_mode) & 0o077 == 0
        return original_chmod(path, mode)

    monkeypatch.setattr(rc.os, "chmod", require_already_private)
    previous_umask = os.umask(0o022)
    try:
        rc.store_credential(REGISTRY, {"token": "test-token"})
    finally:
        os.umask(previous_umask)
    assert stat.S_IMODE(rc.credentials_path().stat().st_mode) == 0o600


def test_failed_credential_save_keeps_old_login_and_removes_temp_file(config_home, monkeypatch):
    rc.store_credential(REGISTRY, {"token": "old-token"})
    before = rc.credentials_path().read_bytes()
    directory = rc.credentials_path().parent
    files_before = set(directory.iterdir())

    def fail_replace(source, destination):
        assert stat.S_IMODE(source.stat().st_mode) == 0o600
        raise OSError("simulated save failure")

    monkeypatch.setattr(rc.os, "replace", fail_replace)
    with pytest.raises(OSError, match="simulated save failure"):
        rc.store_credential("https://other.example", {"token": "new-token"})
    assert rc.credentials_path().read_bytes() == before
    assert set(directory.iterdir()) == files_before


def test_cli_parses_the_new_commands(monkeypatch, capsys):
    from sema.cli import main as cli_main

    calls: list[tuple] = []
    monkeypatch.setattr(
        "sema.cli.registry_client.run_registry",
        lambda command, args: calls.append((command, args.manifest_url, args.registry)) or True,
    )
    monkeypatch.setattr(
        "sys.argv",
        ["sema", "registry", "import", MANIFEST, "--registry", REGISTRY],
    )
    cli_main.main()
    assert calls == [("import", MANIFEST, REGISTRY)]
