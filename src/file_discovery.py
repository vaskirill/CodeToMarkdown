# Copyright (c) 2025 Kirill Vasilev
# Licensed under the MIT License. See LICENSE file for details.

"""File discovery and filtering module."""

import logging
from collections.abc import Iterator
from pathlib import Path

try:
    import pathspec
    PATHSPEC_AVAILABLE = True
except ImportError:
    PATHSPEC_AVAILABLE = False
    pathspec = None  # Set to None to avoid NameError
    logging.warning("pathspec not available, .gitignore support disabled")

try:
    # Try relative imports first (for development)
    from .utils import is_binary_file
except ImportError:
    # Fallback to absolute imports (for PyInstaller)
    from src.utils import is_binary_file


class FileDiscovery:
    """File discovery and filtering utility."""

    # Supported text file extensions (optimized set)
    TEXT_EXTENSIONS = frozenset({
        # Code files
        ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".kt", ".cs",
        ".cpp", ".c", ".hpp", ".h", ".go", ".rs", ".php", ".rb", ".swift",
        # Scripts
        ".sh", ".ps1", ".bat", ".cmd",
        # Config/markup
        ".json", ".yaml", ".yml", ".toml", ".ini", ".env", ".md", ".txt", ".cfg",
        # Web
        ".html", ".css", ".scss", ".sass", ".less",
        # Other
        ".xml", ".sql", ".r", ".m", ".pl", ".lua", ".dart", ".scala", ".clj",
        ".hs", ".elm", ".ex", ".exs", ".fs", ".fsx", ".ml", ".mli", ".nim",
        ".pas", ".pp", ".d", ".ada", ".adb", ".ads", ".v", ".vhdl", ".sv",
        ".tcl", ".awk", ".sed", ".vim", ".emacs", ".el", ".lisp", ".cl",
        ".scm", ".rkt", ".jl",
    })

    # Directories to exclude (optimized set)
    EXCLUDED_DIRS = frozenset({
        ".git", ".hg", ".svn", ".idea", ".vscode", "__pycache__",
        "node_modules", "dist", "build", "out", ".venv", "venv",
        ".mypy_cache", ".pytest_cache", ".tox", ".coverage",
        "target", "bin", "obj", ".vs", ".settings",
        "logs", "log", "tmp", "temp", ".tmp", ".temp",
    })

    # Files to exclude (optimized set)
    EXCLUDED_FILES = frozenset({
        "PROJECT_CODEBUNDLE.md",  # Our output file
    })

    def __init__(self, include_gitignore: bool = True, include_config: bool = True):
        """Initialize file discovery.
        
        Args:
            include_gitignore: Whether to respect .gitignore files.
            include_config: Whether to include config files.
        """
        self.include_gitignore = include_gitignore and PATHSPEC_AVAILABLE
        self.include_config = include_config
        self.logger = logging.getLogger(__name__)

    def discover_files(self, project_path: Path, max_file_size_mb: int = 5) -> list[Path]:
        """Discover all text files in the project.
        
        Args:
            project_path: Path to the project directory.
            max_file_size_mb: Maximum file size in MB.
            
        Returns:
            List of discovered file paths.
        """
        max_size_bytes = max_file_size_mb * 1024 * 1024

        try:
            gitignore_spec = self._load_gitignore(project_path)

            # Use generator expression for memory efficiency
            files = [
                file_path for file_path in self._walk_directory(project_path, gitignore_spec)
                if self._should_include_file(file_path, max_size_bytes)
            ]

            # Sort in-place for better performance
            files.sort()
            return files

        except Exception as e:
            self.logger.error(f"Error discovering files: {e}")
            return []

    def _load_gitignore(self, project_path: Path) -> object | None:
        """Load .gitignore rules if available.
        
        Args:
            project_path: Path to the project directory.
            
        Returns:
            PathSpec object or None if not available.
        """
        if not self.include_gitignore:
            return None

        gitignore_path = project_path / ".gitignore"
        if not gitignore_path.exists():
            return None

        try:
            with open(gitignore_path, encoding="utf-8") as f:
                patterns = f.readlines()
            return pathspec.PathSpec.from_lines("gitwildmatch", patterns)
        except Exception as e:
            self.logger.warning(f"Error loading .gitignore: {e}")
            return None

    def _walk_directory(self, root: Path, gitignore_spec: object | None) -> Iterator[Path]:
        """Walk directory and yield files.
        
        Args:
            root: Root directory to walk.
            gitignore_spec: Gitignore specification.
            
        Yields:
            File paths.
        """
        try:
            for item in root.rglob("*"):
                if item.is_file():
                    # Check if file is in excluded directory
                    if self._is_in_excluded_directory(item, root):
                        continue

                    # Check gitignore
                    if gitignore_spec and gitignore_spec.match_file(str(item.relative_to(root))):
                        continue
                    yield item
        except PermissionError as e:
            self.logger.warning(f"Permission denied accessing {root}: {e}")
        except Exception as e:
            self.logger.error(f"Error walking directory {root}: {e}")

    def _is_in_excluded_directory(self, file_path: Path, root: Path) -> bool:
        """Check if file is in an excluded directory.
        
        Args:
            file_path: Path to the file.
            root: Root directory.
            
        Returns:
            True if file is in excluded directory.
        """
        try:
            rel_path = file_path.relative_to(root)
            for part in rel_path.parts:
                if part in self.EXCLUDED_DIRS:
                    return True
            return False
        except ValueError:
            return False

    def _should_include_file(self, file_path: Path, max_size_bytes: int) -> bool:
        """Check if file should be included.
        
        Args:
            file_path: Path to the file.
            max_size_bytes: Maximum file size in bytes.
            
        Returns:
            True if file should be included.
        """
        # Fast checks first (most likely to fail)
        if file_path.name in self.EXCLUDED_FILES:
            return False

        # Check extension (fast lookup with frozenset)
        if file_path.suffix.lower() not in self.TEXT_EXTENSIONS:
            return False

        # Check if config file and config files are disabled
        if not self.include_config and self._is_config_file(file_path):
            return False

        # Check file size (expensive operation last)
        try:
            file_size = file_path.stat().st_size
            if file_size > max_size_bytes:
                self.logger.info(f"File too large: {file_path} ({file_size / (1024 * 1024):.1f} MB)")
                return False
        except OSError:
            return False

        # Check if file contains binary data (most expensive check last)
        if is_binary_file(file_path):
            return False

        return True


    def _is_config_file(self, file_path: Path) -> bool:
        """Check if file is a config file.
        
        Args:
            file_path: Path to the file.
            
        Returns:
            True if file is a config file.
        """
        config_extensions = {".json", ".yaml", ".yml", ".toml", ".ini", ".env", ".cfg"}
        return file_path.suffix.lower() in config_extensions



    def get_file_stats(self, file_path: Path) -> tuple[int, int, str]:
        """Get file statistics.
        
        Args:
            file_path: Path to the file.
            
        Returns:
            Tuple of (size_bytes, line_count, sha256_hash).
        """
        try:
            stat_info = file_path.stat()
            size_bytes = stat_info.st_size

            # Count lines
            line_count = 0
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                for _ in f:
                    line_count += 1

            # Calculate hash
            import hashlib
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)

            return size_bytes, line_count, sha256_hash.hexdigest()[:12]

        except Exception as e:
            self.logger.error(f"Error getting stats for {file_path}: {e}")
            return 0, 0, "error"

    def get_file_type(self, file_path: Path) -> str:
        """Get file type description.
        
        Args:
            file_path: Path to the file.
            
        Returns:
            File type description.
        """
        return get_file_type_description(file_path.suffix)
