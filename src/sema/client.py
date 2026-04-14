import logging
import shutil
from pathlib import Path

# We'll need these dependencies
try:
    import httpx
    from platformdirs import user_data_dir
except ImportError:
    # Fallbacks or graceful failure if deps aren't installed yet
    httpx = None
    user_data_dir = None

logger = logging.getLogger(__name__)

# Constants
APP_NAME = "sema"
APP_AUTHOR = "emergentwisdom"
# TODO: Replace with your actual production URL (e.g. GitHub Pages or S3)
# For now, we can default to a raw GitHub URL if the repo is public, or a placeholder.
DEFAULT_REMOTE_URL = "https://raw.githubusercontent.com/emergent-wisdom/sema/main/data/taxonomy.db"
DEFAULT_DB_NAME = "taxonomy.db"


class SemaClient:
    def __init__(self, data_dir: str | None = None):
        if data_dir:
            self.data_dir = Path(data_dir)
        elif user_data_dir:
            self.data_dir = Path(user_data_dir(APP_NAME, APP_AUTHOR))
        else:
            self.data_dir = Path.home() / ".sema"

        self.db_path = self.data_dir / DEFAULT_DB_NAME
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def is_initialized(self) -> bool:
        """Check if the local database exists."""
        return self.db_path.exists() and self.db_path.stat().st_size > 0

    def download_db(self, url: str = DEFAULT_REMOTE_URL, force: bool = False):
        """Download the latest taxonomy database."""
        if self.is_initialized() and not force:
            logger.info("Database already exists. Use force=True to overwrite.")
            return

        if not httpx:
            raise ImportError(
                "The 'httpx' library is required to download the database. "
                "Please install 'sema[full]' or 'httpx'."
            )

        logger.info(f"Downloading database from {url} to {self.db_path}...")
        try:
            with httpx.stream("GET", url, follow_redirects=True) as response:
                response.raise_for_status()
                # Download to a temporary file first
                tmp_path = self.db_path.with_suffix(".tmp")
                with open(tmp_path, "wb") as f:
                    for chunk in response.iter_bytes():
                        f.write(chunk)

                # Atomic move
                shutil.move(str(tmp_path), str(self.db_path))
                logger.info("Download complete.")
        except Exception as e:
            logger.error(f"Failed to download database: {e}")
            raise

    def get_db_path(self) -> str:
        """Return the path to the local database, downloading it if necessary."""
        if not self.is_initialized():
            print(f"Sema database not found at {self.db_path}.")
            print("Downloading default database... (this happens once)")
            try:
                self.download_db()
            except Exception as e:
                print(f"Warning: Could not download database ({e}). Functionality will be limited.")
        return str(self.db_path)


def get_default_client():
    return SemaClient()
