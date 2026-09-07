"""Command-line login and library publishing against a hosted Sema registry.

The login follows the OAuth 2.0 device authorization grant (RFC 8628): the CLI
asks the registry for a device code, shows the person a short user code and a
verification URL, and polls for the token while the person approves the code
in a browser. The token is stored per registry origin under the Sema
configuration directory with owner-only permissions.

A registry is any deployment of the Sema website. The default is
https://semahash.org, but ``--registry`` or ``SEMA_REGISTRY_URL`` selects
another one, and ``sema install`` never needs a registry or a login.
"""

from __future__ import annotations

import json
import os
import socket
import sys
import time
import webbrowser
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import httpx

from .. import __version__
from ..core.registry import _get_config_dir

DEFAULT_REGISTRY = "https://semahash.org"
REGISTRY_ENV = "SEMA_REGISTRY_URL"
TOKEN_ENV = "SEMA_REGISTRY_TOKEN"
CREDENTIALS_FILENAME = "credentials.json"
LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}
IMPORT_TIMEOUT_SECONDS = 180.0
DEFAULT_TIMEOUT_SECONDS = 20.0


class RegistryError(RuntimeError):
    """A registry request failed or the client is not logged in."""


def say(line: str) -> None:
    """Print progress immediately, so an agent reading a pipe sees the code."""

    print(line, flush=True)


@dataclass(frozen=True)
class LoginResult:
    registry: str
    login: str | None
    token_id: str | None
    expires_at: int | None


def normalize_registry(url: str | None) -> str:
    """Return the registry origin, accepting only HTTPS or a loopback HTTP URL."""

    raw = (url or os.environ.get(REGISTRY_ENV) or DEFAULT_REGISTRY).strip()
    parts = urlsplit(raw)
    if (
        parts.scheme not in {"http", "https"}
        or not parts.netloc
        or parts.username
        or parts.password
        or parts.path.rstrip("/")
        or parts.query
        or parts.fragment
    ):
        raise RegistryError(f"Invalid registry URL: {raw}")
    if parts.scheme == "http" and parts.hostname not in LOCAL_HOSTS:
        raise RegistryError("Registry URLs must use HTTPS")
    return f"{parts.scheme}://{parts.netloc}"


def credentials_path() -> Path:
    return _get_config_dir() / CREDENTIALS_FILENAME


def _load_credentials() -> dict[str, Any]:
    path = credentials_path()
    if not path.exists():
        return {"registries": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RegistryError(f"Stored credentials are unreadable: {path}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("registries"), dict):
        raise RegistryError(f"Stored credentials have an unexpected shape: {path}")
    return data


def _save_credentials(data: dict[str, Any]) -> None:
    path = credentials_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.chmod(tmp, 0o600)
    os.replace(tmp, path)
    os.chmod(path, 0o600)


def stored_credential(registry: str) -> dict[str, Any] | None:
    record = _load_credentials()["registries"].get(registry)
    return record if isinstance(record, dict) else None


def store_credential(registry: str, record: dict[str, Any]) -> None:
    data = _load_credentials()
    data["registries"][registry] = record
    _save_credentials(data)


def forget_credential(registry: str) -> bool:
    data = _load_credentials()
    if registry not in data["registries"]:
        return False
    del data["registries"][registry]
    _save_credentials(data)
    return True


def resolve_token(registry: str) -> str:
    """Prefer an explicit environment token, then the stored login."""

    env_token = os.environ.get(TOKEN_ENV, "").strip()
    if env_token:
        return env_token
    record = stored_credential(registry)
    token = record.get("token") if record else None
    if not isinstance(token, str) or not token:
        raise RegistryError(f"Not logged in to {registry}. Run `sema login` first.")
    return token


def client_label() -> str:
    host = socket.gethostname() or "unknown host"
    return f"sema {__version__} on {host}"[:120]


def _error_payload(response: httpx.Response) -> tuple[str | None, str]:
    """Return the OAuth-style error code, if any, and a readable message."""

    try:
        payload = response.json()
    except ValueError:
        return None, f"HTTP {response.status_code}"
    detail = payload.get("detail") if isinstance(payload, dict) else None
    if isinstance(detail, dict):
        code = detail.get("error") if isinstance(detail.get("error"), str) else None
        message = detail.get("message") or detail.get("error") or f"HTTP {response.status_code}"
        return code, str(message)
    if isinstance(detail, str) and detail.strip():
        return None, detail.strip()
    return None, f"HTTP {response.status_code}"


def _raise_for_status(response: httpx.Response) -> None:
    if response.is_success:
        return
    _code, message = _error_payload(response)
    if response.status_code == 401:
        raise RegistryError(f"{message}. Run `sema login` to log in again.")
    raise RegistryError(message)


def _client(timeout: float) -> httpx.Client:
    return httpx.Client(timeout=timeout, follow_redirects=False)


def login(
    registry_url: str | None = None,
    *,
    http_client: httpx.Client | None = None,
    open_browser: bool = True,
    out: Callable[[str], None] = say,
    sleep: Callable[[float], None] = time.sleep,
    clock: Callable[[], float] = time.time,
) -> LoginResult:
    """Run the device authorization flow and store the resulting token."""

    registry = normalize_registry(registry_url)
    client = http_client or _client(DEFAULT_TIMEOUT_SECONDS)
    try:
        started = client.post(f"{registry}/api/cli/device", json={"client": client_label()})
        _raise_for_status(started)
        data = started.json()
        device_code = str(data["device_code"])
        user_code = str(data["user_code"])
        verification = str(data.get("verification_uri_complete") or data["verification_uri"])
        interval = max(1, int(data.get("interval", 5)))
        deadline = clock() + int(data.get("expires_in", 900))

        out(f"Open {verification}")
        out(f"and confirm the code {user_code} with your GitHub account.")
        if open_browser:
            try:
                webbrowser.open(verification)
            except Exception:  # noqa: BLE001 - the link above is the fallback
                pass
        out("Waiting for approval...")

        while True:
            if clock() >= deadline:
                raise RegistryError("The login code expired before it was approved")
            sleep(interval)
            response = client.post(f"{registry}/api/cli/token", json={"device_code": device_code})
            if response.is_success:
                token = response.json()
                break
            code, message = _error_payload(response)
            if code == "authorization_pending":
                continue
            if code == "slow_down":
                interval += 5
                continue
            if code == "access_denied":
                raise RegistryError("The login was denied in the browser")
            if code == "expired_token":
                raise RegistryError("The login code expired before it was approved")
            raise RegistryError(f"Login failed: {message}")
    except httpx.HTTPError as exc:
        raise RegistryError(f"Could not reach {registry}: {exc}") from exc
    finally:
        if http_client is None:
            client.close()

    access_token = token.get("access_token")
    if not isinstance(access_token, str) or not access_token:
        raise RegistryError("The registry returned no access token")
    account = token.get("account") if isinstance(token.get("account"), dict) else {}
    now = int(clock())
    expires_in = token.get("expires_in")
    expires_at = now + int(expires_in) if isinstance(expires_in, int) and expires_in > 0 else None
    record = {
        "token": access_token,
        "token_id": token.get("token_id"),
        "login": account.get("login"),
        "created_at": now,
        "expires_at": expires_at,
    }
    store_credential(registry, record)
    return LoginResult(
        registry=registry,
        login=record["login"],
        token_id=record["token_id"],
        expires_at=expires_at,
    )


def _auth_headers(registry: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {resolve_token(registry)}"}


def logout(
    registry_url: str | None = None,
    *,
    http_client: httpx.Client | None = None,
    out: Callable[[str], None] = say,
) -> bool:
    """Revoke the stored token on the registry, then forget it locally."""

    registry = normalize_registry(registry_url)
    record = stored_credential(registry)
    if record is None:
        out(f"Not logged in to {registry}.")
        return True
    token_id = record.get("token_id")
    if isinstance(token_id, str) and token_id and isinstance(record.get("token"), str):
        client = http_client or _client(DEFAULT_TIMEOUT_SECONDS)
        try:
            response = client.delete(
                f"{registry}/api/me/tokens/{token_id}",
                headers={"Authorization": f"Bearer {record['token']}"},
            )
            if not response.is_success and response.status_code not in {401, 404}:
                out(f"⚠️  The registry did not revoke the token ({response.status_code}).")
        except httpx.HTTPError as exc:
            out(f"⚠️  Could not reach {registry} to revoke the token: {exc}")
        finally:
            if http_client is None:
                client.close()
    forget_credential(registry)
    out(f"✅ Logged out of {registry}")
    return True


def whoami(
    registry_url: str | None = None,
    *,
    http_client: httpx.Client | None = None,
    out: Callable[[str], None] = say,
) -> dict[str, Any]:
    registry = normalize_registry(registry_url)
    client = http_client or _client(DEFAULT_TIMEOUT_SECONDS)
    try:
        response = client.get(f"{registry}/api/me", headers=_auth_headers(registry))
        _raise_for_status(response)
        payload = response.json()
    except httpx.HTTPError as exc:
        raise RegistryError(f"Could not reach {registry}: {exc}") from exc
    finally:
        if http_client is None:
            client.close()
    user = payload.get("user") if isinstance(payload, dict) else None
    if not payload.get("authenticated") or not isinstance(user, dict):
        raise RegistryError(f"Not logged in to {registry}. Run `sema login` first.")
    out(f"@{user.get('login')} on {registry}")
    return user


def registry_import(
    manifest_url: str,
    registry_url: str | None = None,
    *,
    http_client: httpx.Client | None = None,
    out: Callable[[str], None] = say,
) -> dict[str, Any]:
    """Ask the registry to verify and publish a GitHub Release manifest you own."""

    registry = normalize_registry(registry_url)
    client = http_client or _client(IMPORT_TIMEOUT_SECONDS)
    try:
        response = client.post(
            f"{registry}/api/registry/import",
            json={"manifest_url": manifest_url.strip()},
            headers=_auth_headers(registry),
        )
        _raise_for_status(response)
        payload = response.json()
    except httpx.HTTPError as exc:
        raise RegistryError(f"Could not reach {registry}: {exc}") from exc
    finally:
        if http_client is None:
            client.close()
    record = payload.get("record") if isinstance(payload, dict) else None
    if not isinstance(record, dict):
        raise RegistryError("The registry returned an incomplete import result")
    operation = payload.get("operation", "imported")
    verb = {"created": "Published", "updated": "Updated", "unchanged": "Already current:"}.get(
        str(operation), "Imported"
    )
    out(
        f"✅ {verb} {record.get('library_id')} v{record.get('version')} "
        f"({record.get('pattern_count')} patterns)"
    )
    out(f"   semantic root: {record.get('root')}")
    out(f"   catalog root:  {record.get('catalog_root')}")
    out(f"   page:          {registry}/vocabularies/{record.get('library_id')}")
    return payload


def registry_list(
    registry_url: str | None = None,
    *,
    http_client: httpx.Client | None = None,
    out: Callable[[str], None] = say,
) -> list[dict[str, Any]]:
    registry = normalize_registry(registry_url)
    client = http_client or _client(DEFAULT_TIMEOUT_SECONDS)
    try:
        response = client.get(f"{registry}/api/me/libraries", headers=_auth_headers(registry))
        _raise_for_status(response)
        rows = response.json()
    except httpx.HTTPError as exc:
        raise RegistryError(f"Could not reach {registry}: {exc}") from exc
    finally:
        if http_client is None:
            client.close()
    if not isinstance(rows, list):
        raise RegistryError("The registry returned an invalid library list")
    if not rows:
        out(f"No libraries published to {registry} yet.")
        return []
    for row in rows:
        if isinstance(row, dict):
            out(
                f"{row.get('library_id')} v{row.get('version')}: "
                f"{row.get('pattern_count')} patterns, root {str(row.get('root', ''))[:16]}"
            )
    return [row for row in rows if isinstance(row, dict)]


def registry_remove(
    library_id: str,
    registry_url: str | None = None,
    *,
    http_client: httpx.Client | None = None,
    out: Callable[[str], None] = say,
) -> bool:
    registry = normalize_registry(registry_url)
    client = http_client or _client(DEFAULT_TIMEOUT_SECONDS)
    try:
        response = client.delete(
            f"{registry}/api/me/libraries/{library_id.strip()}",
            headers=_auth_headers(registry),
        )
        _raise_for_status(response)
    except httpx.HTTPError as exc:
        raise RegistryError(f"Could not reach {registry}: {exc}") from exc
    finally:
        if http_client is None:
            client.close()
    out(f"✅ Removed {library_id} from {registry}. Your GitHub release is untouched.")
    return True


# ── CLI entry points (print, return success) ────────────────────────────────


def run_login(registry_url: str | None, *, open_browser: bool) -> bool:
    try:
        result = login(registry_url, open_browser=open_browser)
    except RegistryError as exc:
        print(f"❌ {exc}", file=sys.stderr, flush=True)
        return False
    who = f"@{result.login}" if result.login else "your account"
    say(f"✅ Logged in as {who} on {result.registry}")
    say(f"   Token stored in {credentials_path()}")
    say("   Revoke it with `sema logout` or from your profile page.")
    return True


def run_logout(registry_url: str | None) -> bool:
    try:
        return logout(registry_url)
    except RegistryError as exc:
        print(f"❌ {exc}", file=sys.stderr, flush=True)
        return False


def run_whoami(registry_url: str | None) -> bool:
    try:
        whoami(registry_url)
    except RegistryError as exc:
        print(f"❌ {exc}", file=sys.stderr, flush=True)
        return False
    return True


def run_registry(command: str, args: Any) -> bool:
    try:
        if command == "import":
            registry_import(args.manifest_url, args.registry)
        elif command == "list":
            registry_list(args.registry)
        elif command == "remove":
            registry_remove(args.library_id, args.registry)
        else:
            print(f"❌ Unknown registry command: {command}", file=sys.stderr, flush=True)
            return False
    except RegistryError as exc:
        print(f"❌ {exc}", file=sys.stderr, flush=True)
        return False
    return True
