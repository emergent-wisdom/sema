"""Keep the server tests independent of the developer's own Sema configuration."""

import os
import tempfile

# sema.server.api resolves its database when it is imported and, like the MCP
# server, follows the vocabulary selected with `sema use`. Point the configuration
# at an empty directory before any test module imports the API, so every run
# starts on the bundled vocabulary instead of whatever the developer has active.
os.environ["XDG_CONFIG_HOME"] = tempfile.mkdtemp(prefix="sema-server-tests-")
os.environ.pop("SEMA_DB_PATH", None)
