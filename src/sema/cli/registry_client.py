"""Command-line login and library publishing against a hosted Sema registry.

The login follows the OAuth 2.0 device authorization grant (RFC 8628): the CLI
asks the registry for a device code, shows the person a short user code and a
verification URL, and polls for the token while the person approves the code
in a browser. The token is stored per registry origin under the Sema
configuration directory with owner-only permissions.

A registry is any deployment of the Sema website. A successful login remembers
that registry for later commands. ``--registry`` and ``SEMA_REGISTRY_URL`` take
precedence over the remembered choice; https://semahash.org is the first-use
default. ``sema install`` never needs a registry or a login.
"""

from __future__ import annotations

import json
import os
import socket
import sys
import tempfile
import time
import webbrowser
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any
from urllib.parse import quote, urlsplit

import httpx

from .. import __version__
from ..core.registry import _get_config_dir

if TYPE_CHECKING:
    from ..core.libraries import ExpectedRelease

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

    raw = url or os.environ.get(REGISTRY_ENV)
    if not raw:
        remembered = _load_credentials().get("default_registry")
        if remembered is not None and (not isinstance(remembered, str) or not remembered.strip()):
            raise RegistryError("Stored default registry must be a non-empty URL")
        raw = remembered or DEFAULT_REGISTRY
    raw = raw.strip()
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
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(data, stream, indent=2, sort_keys=True)
            stream.write("\n")
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def stored_credential(registry: str) -> dict[str, Any] | None:
    record = _load_credentials()["registries"].get(registry)
    return record if isinstance(record, dict) else None


def store_credential(registry: str, record: dict[str, Any]) -> None:
    data = _load_credentials()
    data["registries"][registry] = record
    data["default_registry"] = registry
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


# ── Public libraries: search, look up, and a key for agents ────────────────


def _public_get(
    registry: str, path: str, *, http_client: httpx.Client | None = None
) -> tuple[int, Any]:
    """GET a public registry endpoint without credentials."""

    client = http_client or _client(DEFAULT_TIMEOUT_SECONDS)
    try:
        response = client.get(f"{registry}{path}")
        if response.status_code == 404:
            return 404, None
        _raise_for_status(response)
        return response.status_code, response.json()
    except httpx.HTTPError as exc:
        raise RegistryError(f"Could not reach {registry}: {exc}") from exc
    except ValueError as exc:
        raise RegistryError(f"{registry} returned an invalid response") from exc
    finally:
        if http_client is None:
            client.close()


def is_library_name(source: str) -> bool:
    """A bare name is looked up on a registry; paths and URLs are installed directly."""

    value = source.strip()
    return bool(value) and (
        "://" not in value
        and "/" not in value
        and "\\" not in value
        and not value.endswith(".json")
        and not Path(value).expanduser().exists()
    )


def _source_label(record: dict[str, Any]) -> str:
    owner, repo = record.get("owner"), record.get("repo")
    return f"{owner}/{repo}" if owner and repo else str(repo or record.get("manifest_url") or "")


def registry_search(
    query: str = "",
    registry_url: str | None = None,
    *,
    http_client: httpx.Client | None = None,
    out: Callable[[str], None] = say,
) -> list[dict[str, Any]]:
    """List the public libraries on a registry that match every word of a query.

    Needs no login. An empty query lists every published library.
    """

    registry = normalize_registry(registry_url)
    status, rows = _public_get(registry, "/api/vocabularies", http_client=http_client)
    if status == 404 or not isinstance(rows, list):
        raise RegistryError(f"{registry} does not offer a public library list")
    terms = query.lower().split()

    def matches(row: dict[str, Any]) -> bool:
        haystack = " ".join(
            str(row.get(key) or "")
            for key in ("slug", "library_id", "owner", "repo", "description")
        ).lower()
        return all(term in haystack for term in terms)

    found = [row for row in rows if isinstance(row, dict) and matches(row)]
    if not found:
        if query.strip():
            out(f"No libraries on {registry} match {query.strip()!r}.")
        else:
            out(f"No libraries published on {registry} yet.")
        return []
    for row in found:
        out(
            f"{row.get('slug')} v{row.get('version')}: {row.get('pattern_count')} patterns, "
            f"from {_source_label(row)}"
        )
    out("Install one with: sema install <name>")
    return found


def resolve_library(
    name: str,
    registry_url: str | None = None,
    *,
    http_client: httpx.Client | None = None,
) -> dict[str, Any]:
    """Return a published library's public record, including its stable manifest URL."""

    registry = normalize_registry(registry_url)
    slug = name.strip()
    if not slug:
        raise RegistryError("Give the name of a published library")
    status, payload = _public_get(
        registry, f"/api/vocabularies/{quote(slug, safe='')}", http_client=http_client
    )
    record = payload.get("record") if isinstance(payload, dict) else None
    if status == 404 or not isinstance(record, dict):
        raise RegistryError(f"No published library named {slug} on {registry}")
    if not isinstance(record.get("manifest_url"), str) or not record["manifest_url"]:
        raise RegistryError(f"{slug} on {registry} has no installable release")
    return record


def expected_release(record: dict[str, Any]) -> ExpectedRelease:
    """The release a registry verified, which an install by name must match exactly.

    A registry name resolves to the publisher's stable URL, which can later serve a
    different release: a new version, or a replacement after an account takeover.
    Pinning to the verified identity stops such a release before it is installed.
    """
    from ..core.libraries import ExpectedRelease

    slug = record.get("slug")
    root = record.get("root")
    if not isinstance(slug, str) or not slug or not isinstance(root, str) or not root:
        raise RegistryError(
            f"{slug or 'This library'} lists no verified release, so it cannot be installed by name"
        )

    def optional(key: str) -> str | None:
        value = record.get(key)
        return value if isinstance(value, str) and value else None

    return ExpectedRelease(
        name=slug,
        semantic_root=root,
        version=optional("version"),
        catalog_root=optional("catalog_root"),
        artifact_sha256=optional("artifact_sha256"),
    )


def pinned_install_refusal(record: dict[str, Any], registry: str, exc: Exception) -> str:
    """Explain a refused install by name, and the explicit way to take the release anyway."""
    return (
        f"{exc}. Nothing was installed. {record.get('slug')} is verified on {registry} "
        f"at v{record.get('version')}; its publisher may have released a version that the "
        "registry has not verified yet, or the release was replaced. To install the "
        f"publisher's current release anyway, run: sema install '{record.get('manifest_url')}'"
    )


def registry_show(
    name: str,
    registry_url: str | None = None,
    *,
    http_client: httpx.Client | None = None,
    out: Callable[[str], None] = say,
) -> dict[str, Any]:
    registry = normalize_registry(registry_url)
    record = resolve_library(name, registry, http_client=http_client)
    out(f"{record.get('slug')} v{record.get('version')} from {_source_label(record)}")
    out(f"   patterns:      {record.get('pattern_count')}")
    out(f"   semantic root: {record.get('root')}")
    out(f"   license:       {record.get('license') or 'not stated; check the repository'}")
    out(f"   release:       {record.get('manifest_url')}")
    out(f"   page:          {registry}/vocabularies/{record.get('slug')}")
    out(f"   install with:  sema install {record.get('slug')}")
    return record


def login_with_key(
    key: str,
    registry_url: str | None = None,
    *,
    http_client: httpx.Client | None = None,
    clock: Callable[[], float] = time.time,
) -> LoginResult:
    """Check and store a key that the person created on the registry's profile page."""

    registry = normalize_registry(registry_url)
    secret = key.strip()
    if not secret.startswith("sema_"):
        raise RegistryError("A Sema key starts with sema_. Create one on your profile page.")
    client = http_client or _client(DEFAULT_TIMEOUT_SECONDS)
    try:
        response = client.get(f"{registry}/api/me", headers={"Authorization": f"Bearer {secret}"})
        if response.status_code == 401:
            raise RegistryError(
                f"{registry} did not accept the key. It may be revoked or expired; "
                "create a new one on your profile page."
            )
        _raise_for_status(response)
        payload = response.json()
    except httpx.HTTPError as exc:
        raise RegistryError(f"Could not reach {registry}: {exc}") from exc
    finally:
        if http_client is None:
            client.close()
    user = payload.get("user") if isinstance(payload, dict) else None
    if (
        not isinstance(payload, dict)
        or not payload.get("authenticated")
        or not isinstance(user, dict)
    ):
        raise RegistryError(f"{registry} did not accept the key")
    token_id = payload.get("token_id") if isinstance(payload.get("token_id"), str) else None
    record = {
        "token": secret,
        "token_id": token_id,
        "login": user.get("login"),
        "created_at": int(clock()),
        "expires_at": None,
    }
    store_credential(registry, record)
    return LoginResult(registry=registry, login=record["login"], token_id=token_id, expires_at=None)


# ── CLI entry points (print, return success) ────────────────────────────────


def run_login(registry_url: str | None, *, open_browser: bool, key: str | None = None) -> bool:
    try:
        if key is not None:
            secret = sys.stdin.readline() if key == "-" else key
            result = login_with_key(secret, registry_url)
        else:
            result = login(registry_url, open_browser=open_browser)
    except RegistryError as exc:
        print(f"❌ {exc}", file=sys.stderr, flush=True)
        return False
    who = f"@{result.login}" if result.login else "your account"
    say(f"✅ Logged in as {who} on {result.registry}")
    say(f"   Remembered registry: {result.registry} (--registry or {REGISTRY_ENV} overrides it)")
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
        elif command == "search":
            registry_search(" ".join(args.query), args.registry)
        elif command == "show":
            registry_show(args.name, args.registry)
        else:
            print(f"❌ Unknown registry command: {command}", file=sys.stderr, flush=True)
            return False
    except RegistryError as exc:
        print(f"❌ {exc}", file=sys.stderr, flush=True)
        return False
    return True
