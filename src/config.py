# Copyright (c) 2025 Kirill Vasilev
# Licensed under the MIT License. See LICENSE file for details.

"""Configuration management for the application."""

import json
from pathlib import Path
from typing import Any

from PySide6.QtCore import QStandardPaths


class Config:
    """Application configuration manager."""

    def __init__(self) -> None:
        """Initialize configuration manager."""
        self.app_name = "CodeToMarkdown"
        self.config_dir = Path(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation))
        self.config_file = self.config_dir / "config.json"
        self._config: dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from file."""
        try:
            if self.config_file.exists():
                with open(self.config_file, encoding="utf-8") as f:
                    self._config = json.load(f)
            else:
                self._config = self._get_default_config()
        except (json.JSONDecodeError, OSError) as e:
            print(f"Error loading config: {e}")
            self._config = self._get_default_config()

    def _get_default_config(self) -> dict[str, Any]:
        """Get default configuration."""
        return {
            "last_project_path": "",
            "include_gitignore": True,
            "include_large_files": True,  # Always include large files
            "include_config_files": True,
            "max_file_size_mb": 5,
            "split_large_output": False,
            "max_output_size_mb": 50,
            "window_geometry": None,
            "splitter_state": None,
        }

    def save_config(self) -> None:
        """Save configuration to file."""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
        except OSError as e:
            print(f"Error saving config: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self._config[key] = value

    @property
    def last_project_path(self) -> str:
        """Get last selected project path."""
        return self.get("last_project_path", "")

    @last_project_path.setter
    def last_project_path(self, value: str) -> None:
        """Set last selected project path."""
        self.set("last_project_path", value)

    @property
    def include_gitignore(self) -> bool:
        """Get gitignore inclusion setting."""
        return self.get("include_gitignore", True)

    @include_gitignore.setter
    def include_gitignore(self, value: bool) -> None:
        """Set gitignore inclusion setting."""
        self.set("include_gitignore", value)

    @property
    def include_large_files(self) -> bool:
        """Get large files inclusion setting."""
        return self.get("include_large_files", True)

    @include_large_files.setter
    def include_large_files(self, value: bool) -> None:
        """Set large files inclusion setting."""
        self.set("include_large_files", value)

    @property
    def include_config_files(self) -> bool:
        """Get config files inclusion setting."""
        return self.get("include_config_files", True)

    @include_config_files.setter
    def include_config_files(self, value: bool) -> None:
        """Set config files inclusion setting."""
        self.set("include_config_files", value)

    @property
    def max_file_size_mb(self) -> int:
        """Get maximum file size in MB."""
        return self.get("max_file_size_mb", 5)

    @property
    def window_geometry(self) -> bytes | None:
        """Get window geometry."""
        return self.get("window_geometry")

    @window_geometry.setter
    def window_geometry(self, value: bytes | None) -> None:
        """Set window geometry."""
        self.set("window_geometry", value)

    @property
    def splitter_state(self) -> bytes | None:
        """Get splitter state."""
        return self.get("splitter_state")

    @splitter_state.setter
    def splitter_state(self, value: bytes | None) -> None:
        """Set splitter state."""
        self.set("splitter_state", value)
