import json
import os
import sys
from pathlib import Path

DEFAULT_CONFIG_FILE = "sema.json"
DEFAULT_PROFILE = "default"
# Default relative to where command is run, or absolute system path?
# Usually CWD/data/vocabulary is the convention in this repo.
DEFAULT_REGISTRY_PATH = "data/vocabulary"


class SemaConfig:
    def __init__(self, config_path=None):
        # Resolve config path relative to project root if not provided
        if not config_path:
            # src/sema/core/config.py -> project_root/sema.json
            root = Path(__file__).parent.parent.parent.parent
            self.config_path = str(root / DEFAULT_CONFIG_FILE)
        else:
            self.config_path = config_path

        self.config = self._load_config()

    def _load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path) as f:
                    return json.load(f)
            except Exception as e:
                # stderr: this can run during MCP server import, where
                # stdout is the JSON-RPC transport.
                print(f"Warning: Failed to load config {self.config_path}: {e}", file=sys.stderr)

        # Default Config
        return {
            "active_profile": DEFAULT_PROFILE,
            "profiles": {
                DEFAULT_PROFILE: {
                    "registry_path": DEFAULT_REGISTRY_PATH,
                    "identity": "anonymous",
                    "policies": {"fail_on_drift": True, "allow_autonomous_ingest": False},
                }
            },
        }

    def save(self):
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=2)

    def get_active_profile_name(self):
        return self.config.get("active_profile", DEFAULT_PROFILE)

    def get_active_profile(self):
        active_name = self.get_active_profile_name()
        profiles = self.config.get("profiles", {})
        profile = profiles.get(active_name) or profiles.get(DEFAULT_PROFILE)
        if profile is None:
            # User config names a missing profile and has no "default"
            # either — behave like an unconfigured install instead of
            # crashing with a KeyError.
            profile = {
                "registry_path": DEFAULT_REGISTRY_PATH,
                "identity": "anonymous",
                "policies": {"fail_on_drift": True, "allow_autonomous_ingest": False},
            }

        # Return a copy with resolved paths: resolving in place would make
        # any later save() rewrite the user's relative paths as
        # machine-specific absolute ones.
        profile = dict(profile)

        # Resolve paths relative to Project Root (where sema.json likely lives)
        project_root = Path(self.config_path).parent

        if "registry_path" in profile:
            path = Path(profile["registry_path"])
            if not path.is_absolute():
                profile["registry_path"] = str((project_root / path).resolve())

        if "db_path" in profile:
            path = Path(profile["db_path"])
            if not path.is_absolute():
                profile["db_path"] = str((project_root / path).resolve())

        return profile

    def switch_profile(self, name):
        if name in self.config["profiles"]:
            self.config["active_profile"] = name
            self.save()
            return True
        return False

    def add_profile(self, name, registry_path, identity="agent", allow_ingest=False):
        self.config["profiles"][name] = {
            "registry_path": registry_path,
            "identity": identity,
            "policies": {"fail_on_drift": True, "allow_autonomous_ingest": allow_ingest},
        }
        self.save()

    def list_profiles(self):
        return self.config["profiles"]


# Global Singleton
_CONFIG_INSTANCE = None


def get_config(path=None):
    global _CONFIG_INSTANCE
    if not _CONFIG_INSTANCE:
        _CONFIG_INSTANCE = SemaConfig(path)
    return _CONFIG_INSTANCE
