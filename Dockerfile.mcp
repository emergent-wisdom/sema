# Minimal container that runs the sema MCP server over stdio.
#
# The server is distributed as a PyPI package (`semahash[mcp]`) and invoked
# as `sema mcp`. It reads the MCP protocol from stdin and writes responses
# to stdout — no network ports are exposed. Consumers talk to the container
# through `docker run -i`, which wires their stdio to the container's.
#
# Build:   docker build -t sema-mcp .
# Run:     docker run --rm -i sema-mcp            # wires to your stdio
# Glama:   upload this file at https://glama.ai/mcp/servers

FROM python:3.12-slim

# Install the MCP server from PyPI. Pinning to a named version is optional —
# omitting the pin tracks the latest release, matching `uvx --from` behaviour.
RUN pip install --no-cache-dir "semahash[mcp]"

# Default command: run the MCP server on stdio. Container orchestrators
# (Glama's inspector, Claude Desktop, etc.) run the image with `-i`
# interactive stdin so the MCP handshake can proceed.
CMD ["sema", "mcp"]
