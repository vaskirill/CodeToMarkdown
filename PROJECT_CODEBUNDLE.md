# code-to-md

## Сводка

- **Дата создания:** 2025-09-19 22:49:57
- **Путь к проекту:** `D:\_GIT\code-to-md`
- **Количество файлов:** 44
- **Общий размер:** 0.23 МБ
- **Время генерации:** 2025-09-19 22:49:57

## Оглавление

  - [build.py](#build-py)
  - [build_release.py](#buildrelease-py)
  - [CLEAN_OPTIMIZATION_REPORT.md](#cleanoptimizationreport-md)
  - [pyproject.toml](#pyproject-toml)
  - [README.md](#readme-md)
  - [run.py](#run-py)
  - [version_info.txt](#versioninfo-txt)

- **.vite\deps_temp_67e18f42/**
  - [package.json](#-vite-depstemp67e18f42-package-json)

- **.vite\deps_temp_d1541c33/**
  - [package.json](#-vite-depstempd1541c33-package-json)

- **app/**
  - [__init__.py](#app-init-py)
  - [annotations.py](#app-annotations-py)
  - [config.py](#app-config-py)
  - [file_discovery.py](#app-filediscovery-py)
  - [i18n.py](#app-i18n-py)
  - [logging_setup.py](#app-loggingsetup-py)
  - [main.py](#app-main-py)
  - [md_builder.py](#app-mdbuilder-py)
  - [ui.py](#app-ui-py)
  - [utils.py](#app-utils-py)
  - [worker.py](#app-worker-py)

- **code_to_markdown.egg-info/**
  - [dependency_links.txt](#codetomarkdown-egg-info-dependencylinks-txt)
  - [requires.txt](#codetomarkdown-egg-info-requires-txt)
  - [SOURCES.txt](#codetomarkdown-egg-info-sources-txt)
  - [top_level.txt](#codetomarkdown-egg-info-toplevel-txt)

- **demo_project/**
  - [config.json](#demoproject-config-json)
  - [main.py](#demoproject-main-py)
  - [README.md](#demoproject-readme-md)

- **demo_project\config/**
  - [config.json](#demoproject-config-config-json)
  - [settings.py](#demoproject-config-settings-py)

- **demo_project\static/**
  - [app.js](#demoproject-static-app-js)
  - [style.css](#demoproject-static-style-css)

- **demo_project\tests/**
  - [test_main.py](#demoproject-tests-testmain-py)

- **demo_project\utils/**
  - [__init__.py](#demoproject-utils-init-py)
  - [helpers.py](#demoproject-utils-helpers-py)
  - [validators.py](#demoproject-utils-validators-py)

- **release/**
  - [CHANGELOG.md](#release-changelog-md)
  - [README.md](#release-readme-md)

- **release_v1.1.0/**
  - [CHANGELOG.md](#releasev1-1-0-changelog-md)
  - [INSTALL.txt](#releasev1-1-0-install-txt)
  - [README.md](#releasev1-1-0-readme-md)

- **tests/**
  - [__init__.py](#tests-init-py)
  - [test_annotations.py](#tests-testannotations-py)
  - [test_file_discovery.py](#tests-testfilediscovery-py)
  - [test_md_builder.py](#tests-testmdbuilder-py)

## .vite\deps_temp_67e18f42\package.json

**Описание:** package_json

**Размер:** 0.00 МБ | **Строки:** 3 | **Хэш:** `3ca9d4afd214`

```json
{
  "type": "module"
}

```

## .vite\deps_temp_d1541c33\package.json

**Описание:** package_json

**Размер:** 0.00 МБ | **Строки:** 3 | **Хэш:** `3ca9d4afd214`

```json
{
  "type": "module"
}

```

## app\__init__.py

**Описание:** Code to Markdown - Desktop GUI tool for converting project source code to Markdown.

**Размер:** 0.00 МБ | **Строки:** 4 | **Хэш:** `682bd445af0e`

```python
"""Code to Markdown - Desktop GUI tool for converting project source code to Markdown."""

__version__ = "1.0.0"
__author__ = "Code to Markdown Team"

```

## app\annotations.py

**Описание:** File annotation and AST analysis module.

**Размер:** 0.01 МБ | **Строки:** 321 | **Хэш:** `1c1215b23d78`

```python
"""File annotation and AST analysis module."""

import ast
import logging
import re
from pathlib import Path

from app.i18n import get_file_type_description, get_text
from app.utils import read_file_safe


class FileAnnotator:
    """File annotation generator."""

    def __init__(self) -> None:
        """Initialize file annotator."""
        self.logger = logging.getLogger(__name__)

        # File name patterns for heuristics (optimized)
        self.name_patterns = {
            "setup.py": "setup_script", "requirements.txt": "requirements_file",
            "pyproject.toml": "pyproject_file", "package.json": "package_json",
            "webpack.config.js": "webpack_config", "tsconfig.json": "typescript_config",
            "Dockerfile": "dockerfile", "docker-compose.yml": "docker_compose",
            "Makefile": "makefile", "CMakeLists.txt": "cmake_file",
            "README.md": "readme_file", "LICENSE": "license_file",
            "CHANGELOG.md": "changelog_file", "CONTRIBUTING.md": "contributing_file",
            "routes.py": "routes_file", "models.py": "models_file",
            "views.py": "views_file", "urls.py": "urls_file",
            "settings.py": "settings_file", "config.py": "config_file",
            "main.py": "main_file", "app.py": "app_file",
            "server.py": "server_file", "client.py": "client_file",
            "test_": "test_file", "_test.py": "test_file",
            "conftest.py": "conftest_file", "pytest.ini": "pytest_config",
            "tox.ini": "tox_config", "setup.cfg": "setup_cfg",
            "MANIFEST.in": "manifest_file", "index.html": "index_html",
            "index.js": "index_js", "index.ts": "index_ts",
            "app.js": "app_js", "app.ts": "app_ts",
            "main.js": "main_js", "main.ts": "main_ts",
            "style.css": "style_css", "styles.css": "styles_css",
            "main.css": "main_css", "app.css": "app_css",
        }

        # Directory patterns
        self.dir_patterns = {
            "tests/": "test_directory",
            "test/": "test_directory",
            "src/": "source_directory",
            "lib/": "library_directory",
            "utils/": "utils_directory",
            "helpers/": "helpers_directory",
            "config/": "config_directory",
            "static/": "static_directory",
            "templates/": "templates_directory",
            "migrations/": "migrations_directory",
            "docs/": "docs_directory",
            "scripts/": "scripts_directory",
            "tools/": "tools_directory",
        }

    def generate_annotation(self, file_path: Path, content: str = None) -> str:
        """Generate annotation for a file.
        
        Args:
            file_path: Path to the file.
            content: File content (optional, will be read if not provided).
            
        Returns:
            Generated annotation.
        """
        try:
            # Try to read content if not provided
            if content is None:
                content = read_file_safe(file_path)
                if content is None:
                    return get_text("no_description")

            # Try docstring/comment extraction first
            annotation = self._extract_docstring_annotation(file_path, content)
            if annotation:
                return annotation

            # Try AST analysis for Python files
            if file_path.suffix.lower() == ".py":
                annotation = self._analyze_python_ast(file_path, content)
                if annotation:
                    return annotation

            # Try heuristic analysis
            annotation = self._heuristic_analysis(file_path, content)
            if annotation:
                return annotation

            # Fallback to file type description
            return get_file_type_description(file_path.suffix)

        except Exception as e:
            self.logger.error(f"Error generating annotation for {file_path}: {e}")
            return get_text("no_description")


    def _extract_docstring_annotation(self, file_path: Path, content: str) -> str | None:
        """Extract annotation from docstring or comments.
        
        Args:
            file_path: Path to the file.
            content: File content.
            
        Returns:
            Extracted annotation or None.
        """
        lines = content.split("\n")

        # Look for module-level docstring (first 50 lines)
        for i, line in enumerate(lines[:50]):
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue

            # Look for docstring start
            if '"""' in line or "'''" in line:
                # Extract docstring content
                docstring_lines = []
                quote_char = '"""' if '"""' in line else "'''"

                # Handle single-line docstring
                if line.count(quote_char) >= 2:
                    start = line.find(quote_char) + 3
                    end = line.rfind(quote_char)
                    if end > start:
                        docstring = line[start:end].strip()
                        if docstring:
                            return self._clean_docstring(docstring)

                # Handle multi-line docstring
                start_line = i
                for j in range(i, min(i + 20, len(lines))):
                    if quote_char in lines[j]:
                        # Found end of docstring
                        docstring_lines = lines[start_line:j+1]
                        break

                if docstring_lines:
                    # Extract content between quotes
                    docstring = "\n".join(docstring_lines)
                    start = docstring.find(quote_char) + 3
                    end = docstring.rfind(quote_char)
                    if end > start:
                        docstring = docstring[start:end].strip()
                        if docstring:
                            return self._clean_docstring(docstring)
                break

        # Look for file header comments
        for i, line in enumerate(lines[:20]):
            line = line.strip()
            if line.startswith("#") and len(line) > 10:
                # Check if it looks like a description
                comment = line[1:].strip()
                if any(word in comment.lower() for word in ["description", "purpose", "about", "summary", "overview"]):
                    return self._clean_docstring(comment)

        return None

    def _clean_docstring(self, docstring: str) -> str:
        """Clean and truncate docstring.
        
        Args:
            docstring: Raw docstring content.
            
        Returns:
            Cleaned docstring.
        """
        # Remove extra whitespace
        docstring = re.sub(r"\s+", " ", docstring.strip())

        # Remove common prefixes
        prefixes = ["This file", "This module", "This script", "This is"]
        for prefix in prefixes:
            if docstring.lower().startswith(prefix.lower()):
                docstring = docstring[len(prefix):].strip()
                if docstring.startswith(","):
                    docstring = docstring[1:].strip()

        # Truncate to reasonable length
        if len(docstring) > 200:
            docstring = docstring[:197] + "..."

        return docstring or get_text("no_description")

    def _analyze_python_ast(self, file_path: Path, content: str) -> str | None:
        """Analyze Python file using AST.
        
        Args:
            file_path: Path to the file.
            content: File content.
            
        Returns:
            Generated annotation or None.
        """
        try:
            tree = ast.parse(content, filename=str(file_path))

            functions = 0
            classes = 0
            imports = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions += 1
                elif isinstance(node, ast.ClassDef):
                    classes += 1
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.ImportFrom) and node.module:
                        imports.append(node.module)
                    elif isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)

            # Generate annotation based on analysis
            parts = []

            if functions > 0 or classes > 0:
                parts.append(get_text("python_module", functions=functions, classes=classes))

            # Add context based on imports
            if imports:
                context = self._analyze_imports(imports)
                if context:
                    parts.append(context)

            return ". ".join(parts) if parts else None

        except SyntaxError:
            # File has syntax errors, skip AST analysis
            return None
        except Exception as e:
            self.logger.warning(f"Error analyzing Python AST for {file_path}: {e}")
            return None

    def _analyze_imports(self, imports: list) -> str | None:
        """Analyze imports to provide context.
        
        Args:
            imports: List of imported modules.
            
        Returns:
            Context description or None.
        """
        # Common patterns
        if any("flask" in imp for imp in imports):
            return "Flask web application"
        if any("django" in imp for imp in imports):
            return "Django web application"
        if any("fastapi" in imp for imp in imports):
            return "FastAPI web application"
        if any("pytest" in imp for imp in imports):
            return "Test file"
        if any("unittest" in imp for imp in imports):
            return "Unit test file"
        if any("numpy" in imp for imp in imports):
            return "Scientific computing module"
        if any("pandas" in imp for imp in imports):
            return "Data analysis module"
        if any("matplotlib" in imp for imp in imports):
            return "Data visualization module"
        if any("requests" in imp for imp in imports):
            return "HTTP client module"
        if any("sqlalchemy" in imp for imp in imports):
            return "Database module"

        return None

    def _heuristic_analysis(self, file_path: Path, content: str) -> str | None:
        """Analyze file using heuristics.
        
        Args:
            file_path: Path to the file.
            content: File content.
            
        Returns:
            Generated annotation or None.
        """
        file_name = file_path.name.lower()
        file_stem = file_path.stem.lower()
        parent_dir = file_path.parent.name.lower()

        # Check file name patterns - use early return for better performance
        for pattern, description in self.name_patterns.items():
            if pattern in file_name or file_name == pattern:
                return get_text(description)

        # Check directory patterns
        file_path_str = str(file_path).lower()
        for pattern, description in self.dir_patterns.items():
            if pattern in file_path_str:
                return get_text(description)

        # Check content patterns
        content_lower = content.lower()

        if "def test_" in content_lower or "class Test" in content_lower:
            return "Test file"
        if 'if __name__ == "__main__"' in content_lower:
            return "Executable script"
        if "import" in content_lower and "def " in content_lower:
            return "Python module with functions"
        if "class " in content_lower:
            return "Python module with classes"
        if "function " in content_lower or "const " in content_lower:
            return "JavaScript/TypeScript module"
        if "SELECT" in content.upper() or "INSERT" in content.upper():
            return "SQL script"
        if "<html" in content_lower or "<!DOCTYPE" in content_lower:
            return "HTML document"
        if "body {" in content_lower or "@media" in content_lower:
            return "CSS stylesheet"

        return None

```

## app\config.py

**Описание:** Configuration management for the application.

**Размер:** 0.00 МБ | **Строки:** 127 | **Хэш:** `6ca2dd8ea38b`

```python
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

```

## app\file_discovery.py

**Описание:** File discovery and filtering module.

**Размер:** 0.01 МБ | **Строки:** 256 | **Хэш:** `d13856a19008`

```python
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

from app.utils import is_binary_file


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

```

## app\i18n.py

**Описание:** Internationalization support for the application.

**Размер:** 0.01 МБ | **Строки:** 160 | **Хэш:** `de6f0ff41ee6`

```python
"""Internationalization support for the application."""

from typing import Any

# Default language (Russian)
TRANSLATIONS: dict[str, dict[str, str]] = {
    "ru": {
        # Main window
        "main_window_title": "Code to Markdown",
        "select_folder": "Выбрать папку",
        "preview": "Предпросмотр",
        "create_markdown": "Создать Markdown",
        "selected_path": "Выбрано: {path}",
        "no_folder_selected": "Папка не выбрана",

        # Options
        "include_gitignore": "Учитывать .gitignore",
        "include_large_files": "Включать большие файлы (>5 МБ)",
        "include_config_files": "Включать конфиги/разметку",

        # File tree
        "file_tree_title": "Файлы проекта",
        "preview_title": "Предпросмотр Markdown",

        # Status
        "ready": "Готов",
        "scanning_files": "Сканирование файлов...",
        "generating_markdown": "Генерация Markdown...",
        "completed": "Завершено",
        "cancelled": "Отменено",
        "error": "Ошибка",

        # Progress
        "files_processed": "Обработано файлов: {current}/{total}",
        "current_file": "Текущий файл: {file}",

        # Messages
        "file_saved": "Файл сохранён",
        "file_saved_message": "Markdown файл успешно создан: {path}",
        "open_folder": "Открыть папку",
        "error_occurred": "Произошла ошибка",
        "error_reading_file": "Ошибка чтения файла: {file}",
        "file_too_large": "Файл слишком большой: {file} ({size} МБ)",
        "unsupported_encoding": "Неподдерживаемая кодировка: {file}",

        # File types
        "python_file": "Python файл",
        "javascript_file": "JavaScript файл",
        "typescript_file": "TypeScript файл",
        "config_file": "Файл конфигурации",
        "markdown_file": "Markdown файл",
        "unknown_file": "Неизвестный тип файла",

        # Annotations
        "no_description": "Назначение файла не определено автоматически",
        "python_module": "Python модуль с {functions} функциями и {classes} классами",
        "config_file_desc": "Файл конфигурации",
        "script_file_desc": "Скрипт",
        "template_file_desc": "Шаблон",
        "style_file_desc": "Файл стилей",
        "markup_file_desc": "Файл разметки",
    },
    "en": {
        # Main window
        "main_window_title": "Code to Markdown",
        "select_folder": "Select Folder",
        "preview": "Preview",
        "create_markdown": "Create Markdown",
        "selected_path": "Selected: {path}",
        "no_folder_selected": "No folder selected",

        # Options
        "include_gitignore": "Respect .gitignore",
        "include_large_files": "Include large files (>5 MB)",
        "include_config_files": "Include config/markup files",

        # File tree
        "file_tree_title": "Project Files",
        "preview_title": "Markdown Preview",

        # Status
        "ready": "Ready",
        "scanning_files": "Scanning files...",
        "generating_markdown": "Generating Markdown...",
        "completed": "Completed",
        "cancelled": "Cancelled",
        "error": "Error",

        # Progress
        "files_processed": "Files processed: {current}/{total}",
        "current_file": "Current file: {file}",

        # Messages
        "file_saved": "File saved",
        "file_saved_message": "Markdown file created successfully: {path}",
        "open_folder": "Open folder",
        "error_occurred": "An error occurred",
        "error_reading_file": "Error reading file: {file}",
        "file_too_large": "File too large: {file} ({size} MB)",
        "unsupported_encoding": "Unsupported encoding: {file}",

        # File types
        "python_file": "Python file",
        "javascript_file": "JavaScript file",
        "typescript_file": "TypeScript file",
        "config_file": "Configuration file",
        "markdown_file": "Markdown file",
        "unknown_file": "Unknown file type",

        # Annotations
        "no_description": "File purpose not automatically determined",
        "python_module": "Python module with {functions} functions and {classes} classes",
        "config_file_desc": "Configuration file",
        "script_file_desc": "Script",
        "template_file_desc": "Template",
        "style_file_desc": "Style file",
        "markup_file_desc": "Markup file",
    },
}


def get_text(key: str, lang: str = "ru", **kwargs: Any) -> str:
    """Get translated text.
    
    Args:
        key: Translation key.
        lang: Language code.
        **kwargs: Format parameters.
        
    Returns:
        Translated and formatted text.
    """
    text = TRANSLATIONS.get(lang, TRANSLATIONS["ru"]).get(key, key)
    return text.format(**kwargs) if kwargs else text


def get_file_type_description(extension: str, lang: str = "ru") -> str:
    """Get file type description based on extension.
    
    Args:
        extension: File extension (with or without dot).
        lang: Language code.
        
    Returns:
        File type description.
    """
    ext = extension.lower().lstrip(".")

    # Optimized type mapping
    type_map = {
        "py": "python_file", "js": "javascript_file", "ts": "typescript_file",
        "tsx": "typescript_file", "jsx": "javascript_file", "json": "config_file",
        "yaml": "config_file", "yml": "config_file", "toml": "config_file",
        "ini": "config_file", "env": "config_file", "cfg": "config_file",
        "md": "markdown_file", "html": "markup_file", "css": "style_file",
        "scss": "style_file", "sh": "script_file_desc", "ps1": "script_file_desc",
        "bat": "script_file_desc", "cmd": "script_file_desc",
    }

    return get_text(type_map.get(ext, "unknown_file"), lang)

```

## app\logging_setup.py

**Описание:** Logging configuration for the application.

**Размер:** 0.00 МБ | **Строки:** 52 | **Хэш:** `c159d22eff83`

```python
"""Logging configuration for the application."""

import logging
import logging.handlers
from pathlib import Path


def setup_logging(log_file: Path | None = None) -> logging.Logger:
    """Set up application logging.
    
    Args:
        log_file: Path to log file. If None, uses default location.
        
    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger("CodeToMarkdown")
    logger.setLevel(logging.INFO)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler with rotation
    if log_file is None:
        log_file = Path.home() / "CodeToMarkdown" / "logs" / "app.log"

    log_file.parent.mkdir(parents=True, exist_ok=True)

    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=1024 * 1024,  # 1 MB
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

```

## app\main.py

**Описание:** Main application entry point.

**Размер:** 0.00 МБ | **Строки:** 77 | **Хэш:** `b0ad076862e5`

```python
"""Main application entry point."""

import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMessageBox

from app.logging_setup import setup_logging
from app.ui import MainWindow


def main() -> int:
    """Main application entry point.
    
    Returns:
        Exit code.
    """
    # Set up logging
    logger = setup_logging()
    logger.info("Starting Code to Markdown application v1.1.0")
    logger.debug("Python version: %s", sys.version)
    logger.debug("Platform: %s", sys.platform)

    try:
        # Create QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("Code to Markdown")
        app.setApplicationVersion("1.1.0")
        app.setOrganizationName("CodeToMarkdown")

        # Set application style
        app.setStyle("Fusion")

        # Set application icon (if available)
        try:
            icon_path = Path(__file__).parent / "icon.ico"
            if icon_path.exists():
                app.setWindowIcon(QIcon(str(icon_path)))
        except Exception:
            pass  # Icon not critical

        # Create and show main window
        logger.debug("Creating main window...")
        window = MainWindow()
        logger.debug("Main window created successfully")
        window.show()
        logger.info("Main window displayed")

        # Run application
        return app.exec()

    except Exception as e:
        logger.error(f"Fatal error: {e}")

        # Show error message if possible
        try:
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)

            msg = QMessageBox()
            msg.setWindowTitle("Fatal Error")
            msg.setText(f"Произошла критическая ошибка:\n{e!s}")
            msg.setIcon(QMessageBox.Critical)
            msg.exec()
        except Exception:
            print(f"Fatal error: {e}")

        return 1

    finally:
        logger.info("Application shutdown")


if __name__ == "__main__":
    sys.exit(main())

```

## app\md_builder.py

**Описание:** Markdown builder with streaming support.

**Размер:** 0.02 МБ | **Строки:** 434 | **Хэш:** `542a6c482a46`

```python
"""Markdown builder with streaming support."""

import logging
import platform
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable

from app.annotations import FileAnnotator
from app.file_discovery import FileDiscovery
from app.utils import clean_filename_for_anchor, read_file_safe


class MarkdownBuilder:
    """Markdown builder with streaming support."""

    # Language mapping for code blocks (optimized dict)
    LANGUAGE_MAP = {
        ".py": "python", ".js": "javascript", ".ts": "typescript", ".tsx": "tsx", ".jsx": "jsx",
        ".java": "java", ".kt": "kotlin", ".cs": "csharp", ".cpp": "cpp", ".c": "c",
        ".hpp": "cpp", ".h": "c", ".go": "go", ".rs": "rust", ".php": "php", ".rb": "ruby",
        ".swift": "swift", ".sh": "bash", ".ps1": "powershell", ".bat": "batch", ".cmd": "batch",
        ".json": "json", ".yaml": "yaml", ".yml": "yaml", ".toml": "toml", ".ini": "ini",
        ".env": "env", ".md": "markdown", ".txt": "text", ".cfg": "ini", ".html": "html",
        ".css": "css", ".scss": "scss", ".sass": "sass", ".less": "less", ".xml": "xml",
        ".sql": "sql", ".r": "r", ".m": "matlab", ".pl": "perl", ".lua": "lua", ".dart": "dart",
        ".scala": "scala", ".clj": "clojure", ".hs": "haskell", ".elm": "elm", ".ex": "elixir",
        ".exs": "elixir", ".fs": "fsharp", ".fsx": "fsharp", ".ml": "ocaml", ".mli": "ocaml",
        ".nim": "nim", ".pas": "pascal", ".pp": "pascal", ".d": "d", ".ada": "ada",
        ".adb": "ada", ".ads": "ada", ".v": "verilog", ".vhdl": "vhdl", ".sv": "systemverilog",
        ".tcl": "tcl", ".awk": "awk", ".sed": "sed", ".vim": "vim", ".emacs": "lisp",
        ".el": "lisp", ".lisp": "lisp", ".cl": "lisp", ".scm": "scheme", ".rkt": "racket",
        ".jl": "julia",
    }

    def __init__(self) -> None:
        """Initialize markdown builder."""
        self.logger = logging.getLogger(__name__)
        self.file_discovery = FileDiscovery()
        self.file_annotator = FileAnnotator()

    def build_markdown(
        self,
        project_path: Path,
        output_path: Path,
        include_gitignore: bool = True,
        include_large_files: bool = False,
        include_config_files: bool = True,
        max_file_size_mb: int = 5,
        progress_callback: Optional[Callable[[int, str], None]] = None,
    ) -> bool:
        """Build markdown file from project.
        
        Args:
            project_path: Path to the project directory.
            output_path: Path to output markdown file.
            include_gitignore: Whether to respect .gitignore.
            include_large_files: Whether to include large files.
            include_config_files: Whether to include config files.
            max_file_size_mb: Maximum file size in MB.
            progress_callback: Callback for progress updates.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            # Discover files
            if progress_callback:
                progress_callback(0, "Discovering files...")

            self.file_discovery.include_gitignore = include_gitignore
            self.file_discovery.include_config = include_config_files

            files = self.file_discovery.discover_files(project_path, max_file_size_mb)

            if not files:
                self.logger.warning("No files found to process")
                # Still create a basic markdown file for empty projects
                return self._write_empty_project_markdown(project_path, output_path)

            # Build markdown
            return self._write_markdown_stream(
                project_path,
                files,
                output_path,
                progress_callback,
            )

        except Exception as e:
            self.logger.error(f"Error building markdown: {e}")
            return False

    def _write_markdown_stream(
        self,
        project_path: Path,
        files: list[Path],
        output_path: Path,
        progress_callback: Optional[Callable[[int, str], None]] = None,
    ) -> bool:
        """Write markdown file with streaming.
        
        Args:
            project_path: Path to the project directory.
            files: List of files to include.
            output_path: Path to output file.
            progress_callback: Progress callback.
            
        Returns:
            True if successful.
        """
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                # Write header
                self._write_header(f, project_path, files)

                # Write table of contents
                self._write_toc(f, files, project_path)

                # Write file sections
                for i, file_path in enumerate(files):
                    if progress_callback:
                        progress_callback(
                            int((i / len(files)) * 100),
                            f"Processing {file_path.name}",
                        )

                    self._write_file_section(f, file_path, project_path)

                # Write appendices
                self._write_appendices(f, files, project_path)

            return True

        except Exception as e:
            self.logger.error(f"Error writing markdown: {e}")
            return False

    def _write_header(self, f, project_path: Path, files: list[Path]) -> None:
        """Write markdown header.
        
        Args:
            f: File handle.
            project_path: Project path.
            files: List of files.
        """
        project_name = project_path.name
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Calculate total size more efficiently with error handling
        total_size = 0
        for file_path in files:
            try:
                total_size += file_path.stat().st_size
            except OSError:
                continue  # Skip files that can't be accessed
        total_size_mb = total_size / (1024 * 1024)

        f.write(f"# {project_name}\n\n")
        f.write("## Сводка\n\n")
        f.write(f"- **Дата создания:** {timestamp}\n")
        f.write(f"- **Путь к проекту:** `{project_path.absolute()}`\n")
        f.write(f"- **Количество файлов:** {len(files)}\n")
        f.write(f"- **Общий размер:** {total_size_mb:.2f} МБ\n")
        f.write(f"- **Время генерации:** {timestamp}\n\n")

    def _write_toc(self, f, files: list[Path], project_path: Path) -> None:
        """Write table of contents.
        
        Args:
            f: File handle.
            files: List of files.
            project_path: Project path.
        """
        f.write("## Оглавление\n\n")

        # Group files by directory
        dirs = {}
        for file_path in files:
            rel_path = file_path.relative_to(project_path)
            parent = str(rel_path.parent) if rel_path.parent != Path() else "."

            if parent not in dirs:
                dirs[parent] = []
            dirs[parent].append(rel_path)

        # Write TOC
        for dir_path in sorted(dirs.keys()):
            if dir_path != ".":
                f.write(f"- **{dir_path}/**\n")

            for file_path in sorted(dirs[dir_path]):
                anchor = self._file_to_anchor(file_path)
                f.write(f"  - [{file_path.name}](#{anchor})\n")

            f.write("\n")

    def _write_file_section(self, f, file_path: Path, project_path: Path) -> None:
        """Write file section.
        
        Args:
            f: File handle.
            file_path: Path to file.
            project_path: Project path.
        """
        rel_path = file_path.relative_to(project_path)
        anchor = self._file_to_anchor(rel_path)

        # Get file stats
        size_bytes, line_count, file_hash = self.file_discovery.get_file_stats(file_path)
        size_mb = size_bytes / (1024 * 1024)

        # Generate annotation
        annotation = self.file_annotator.generate_annotation(file_path)

        # Write section header
        f.write(f"## {rel_path}\n\n")

        # Write file info
        f.write(f"**Описание:** {annotation}\n\n")
        f.write(f"**Размер:** {size_mb:.2f} МБ | ")
        f.write(f"**Строки:** {line_count} | ")
        f.write(f"**Хэш:** `{file_hash}`\n\n")

        # Write code block
        language = self._get_language(file_path)
        f.write(f"```{language}\n")

        # Write file content
        content = read_file_safe(file_path)
        if content is not None:
            f.write(content)
        else:
            f.write("# Error reading file: Unable to decode with any supported encoding\n")

        f.write("\n```\n\n")

    def _write_appendices(self, f, files: list[Path], project_path: Path) -> None:
        """Write appendices section.
        
        Args:
            f: File handle.
            files: List of files.
            project_path: Project path.
        """
        f.write("## Приложения\n\n")

        # File type statistics
        f.write("### Статистика по типам файлов\n\n")
        f.write("| Расширение | Количество файлов |\n")
        f.write("|------------|-------------------|\n")

        # Use Counter for better performance
        from collections import Counter
        ext_counts = Counter(file_path.suffix.lower() for file_path in files)

        for ext, count in sorted(ext_counts.items()):
            f.write(f"| {ext or '(без расширения)'} | {count} |\n")

        f.write("\n")

        # Largest files
        f.write("### Топ-10 самых больших файлов\n\n")
        f.write("| Файл | Размер (МБ) | Строки |\n")
        f.write("|------|-------------|--------|\n")

        # Get file stats and sort in one pass (optimized)
        file_stats = []
        for file_path in files:
            try:
                stats = self.file_discovery.get_file_stats(file_path)
                file_stats.append((file_path, *stats))
            except Exception:
                continue  # Skip files with errors

        file_stats.sort(key=lambda x: x[1], reverse=True)  # Sort by size

        for file_path, size_bytes, line_count, _ in file_stats[:10]:
            rel_path = file_path.relative_to(project_path)
            size_mb = size_bytes / (1024 * 1024)
            f.write(f"| `{rel_path}` | {size_mb:.2f} | {line_count} |\n")

        f.write("\n")

        # Environment metadata
        f.write("### Метаданные окружения\n\n")
        f.write(f"- **Python версия:** {sys.version}\n")
        f.write(f"- **Операционная система:** {platform.system()} {platform.release()}\n")
        f.write(f"- **Архитектура:** {platform.machine()}\n")
        f.write(f"- **Время генерации:** {datetime.now().isoformat()}\n")

    def _file_to_anchor(self, file_path: Path) -> str:
        """Convert file path to markdown anchor.
        
        Args:
            file_path: File path.
            
        Returns:
            Anchor string.
        """
        return clean_filename_for_anchor(str(file_path))

    def _get_language(self, file_path: Path) -> str:
        """Get language for code block.
        
        Args:
            file_path: File path.
            
        Returns:
            Language identifier.
        """
        return self.LANGUAGE_MAP.get(file_path.suffix.lower(), "text")

    def generate_preview(
        self,
        project_path: Path,
        files: list[Path],
        max_lines: int = 200,
    ) -> str:
        """Generate preview of markdown.
        
        Args:
            project_path: Project path.
            files: List of files.
            max_lines: Maximum lines in preview.
            
        Returns:
            Preview content.
        """
        lines = []

        # Header
        project_name = project_path.name
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lines.append(f"# {project_name}")
        lines.append("")
        lines.append("## Сводка")
        lines.append("")
        lines.append(f"- **Дата создания:** {timestamp}")
        lines.append(f"- **Путь к проекту:** `{project_path.absolute()}`")
        lines.append(f"- **Количество файлов:** {len(files)}")
        lines.append("")

        # TOC preview
        lines.append("## Оглавление")
        lines.append("")

        # Show first few files
        for i, file_path in enumerate(files[:10]):
            rel_path = file_path.relative_to(project_path)
            anchor = self._file_to_anchor(rel_path)
            lines.append(f"- [{rel_path.name}](#{anchor})")

        if len(files) > 10:
            lines.append(f"- ... и еще {len(files) - 10} файлов")

        lines.append("")

        # Show first file content
        if files:
            first_file = files[0]
            rel_path = first_file.relative_to(project_path)
            lines.append(f"## {rel_path}")
            lines.append("")

            # Get annotation
            annotation = self.file_annotator.generate_annotation(first_file)
            lines.append(f"**Описание:** {annotation}")
            lines.append("")

            # Show first few lines of content
            try:
                with open(first_file, encoding="utf-8") as f:
                    content_lines = f.readlines()[:20]  # First 20 lines
                    language = self._get_language(first_file)
                    lines.append(f"```{language}")
                    lines.extend(line.rstrip() for line in content_lines)
                    lines.append("```")
            except Exception:
                lines.append("```text")
                lines.append("# Error reading file")
                lines.append("```")

        # Truncate to max_lines
        result = "\n".join(lines)
        if len(result.split("\n")) > max_lines:
            result = "\n".join(result.split("\n")[:max_lines]) + "\n\n... (preview truncated)"

        return result

    def _write_empty_project_markdown(self, project_path: Path, output_path: Path) -> bool:
        """Write markdown for empty project.
        
        Args:
            project_path: Path to the project directory.
            output_path: Path to output file.
            
        Returns:
            True if successful.
        """
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                project_name = project_path.name
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                f.write(f"# {project_name}\n\n")
                f.write("## Сводка\n\n")
                f.write(f"- **Дата создания:** {timestamp}\n")
                f.write(f"- **Путь к проекту:** `{project_path.absolute()}`\n")
                f.write("- **Количество файлов:** 0\n")
                f.write("- **Общий размер:** 0.00 МБ\n")
                f.write(f"- **Время генерации:** {timestamp}\n\n")

                f.write("## Оглавление\n\n")
                f.write("Проект не содержит файлов для обработки.\n\n")

                f.write("## Приложения\n\n")
                f.write("### Статистика по типам файлов\n\n")
                f.write("| Расширение | Количество файлов |\n")
                f.write("|------------|-------------------|\n")
                f.write("| (нет файлов) | 0 |\n\n")

                f.write("### Метаданные окружения\n\n")
                f.write(f"- **Python версия:** {sys.version}\n")
                f.write(f"- **Операционная система:** {platform.system()} {platform.release()}\n")
                f.write(f"- **Архитектура:** {platform.machine()}\n")
                f.write(f"- **Время генерации:** {datetime.now().isoformat()}\n")

            return True

        except Exception as e:
            self.logger.error(f"Error writing empty project markdown: {e}")
            return False

```

## app\ui.py

**Описание:** Main UI implementation.

**Размер:** 0.03 МБ | **Строки:** 767 | **Хэш:** `b2c7c86c56a4`

```python
"""Main UI implementation."""

from pathlib import Path

from PySide6.QtCore import QSettings, Qt
from PySide6.QtGui import QBrush, QColor, QFont
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QStatusBar,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.config import Config
from app.i18n import get_text
from app.utils import open_file_explorer
from app.worker import WorkerManager


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self) -> None:
        """Initialize main window."""
        super().__init__()
        self.config = Config()
        self.worker_manager = WorkerManager()
        self.current_files = []
        self.selected_files = set()
        self.current_project_path = None
        self._initializing = False

        # Настройки оптимизации
        self.max_tree_items = 1000
        self.show_all_files = False
        self.total_files_in_project = 0
        self.shown_files_count = 0

        self._setup_ui()
        self._setup_connections()
        self._load_settings()

        # Don't load last project path automatically
        # User should explicitly select a folder

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        self.setWindowTitle("Project File Selector")
        self.setMinimumSize(800, 600)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Project path section
        self._create_project_path_section(main_layout)

        # Files section
        self._create_files_section(main_layout)

        # Action button and status
        self._create_action_section(main_layout)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готов")

    def _create_project_path_section(self, parent_layout: QVBoxLayout) -> None:
        """Create project path section."""
        # Section title
        path_label = QLabel("Путь к проекту")
        path_label.setFont(QFont("Arial", 12, QFont.Bold))
        path_label.setStyleSheet("color: #333333; margin-bottom: 8px;")

        # Path input and button layout
        path_layout = QHBoxLayout()
        path_layout.setSpacing(10)

        # Path input field
        self.project_path_input = QLineEdit()
        self.project_path_input.setPlaceholderText("Выберите папку проекта...")
        self.project_path_input.setMinimumHeight(40)
        self.project_path_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #0078d4;
            }
        """)

        # Select folder button
        self.select_folder_btn = QPushButton("Выбрать папку")
        self.select_folder_btn.setMinimumHeight(40)
        self.select_folder_btn.setMinimumWidth(120)
        self.select_folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #f8f9fa;
                color: #333333;
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                font-weight: 500;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                border-color: #0078d4;
            }
            QPushButton:pressed {
                background-color: #dee2e6;
            }
        """)

        path_layout.addWidget(self.project_path_input)
        path_layout.addWidget(self.select_folder_btn)

        # Add to parent layout
        parent_layout.addWidget(path_label)
        parent_layout.addLayout(path_layout)

    def _create_files_section(self, parent_layout: QVBoxLayout) -> None:
        """Create files section with checkboxes."""
        # Section title
        files_label = QLabel("Файлы проекта")
        files_label.setFont(QFont("Arial", 12, QFont.Bold))
        files_label.setStyleSheet("color: #333333; margin-bottom: 8px;")

        # Files list widget
        self.files_list = QTreeWidget()
        self.files_list.setHeaderHidden(True)
        self.files_list.setRootIsDecorated(True)
        self.files_list.setAlternatingRowColors(True)
        self.files_list.setStyleSheet("""
            QTreeWidget {
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                background-color: white;
                selection-background-color: #e3f2fd;
            }
            QTreeWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
            }
            QTreeWidget::item:hover {
                background-color: #f8f9fa;
            }
            QTreeWidget::item:selected {
                background-color: #e3f2fd;
            }
        """)

        # Files container
        files_container = QWidget()
        files_layout = QVBoxLayout(files_container)
        files_layout.setContentsMargins(0, 0, 0, 0)
        files_layout.setSpacing(8)
        files_layout.addWidget(files_label)
        files_layout.addWidget(self.files_list)

        # Add to parent layout
        parent_layout.addWidget(files_container)


    def _create_action_section(self, parent_layout: QVBoxLayout) -> None:
        """Create action section with button and status."""
        # Create Markdown button
        self.create_markdown_btn = QPushButton("Создать Markdown")
        self.create_markdown_btn.setMinimumHeight(50)
        self.create_markdown_btn.setEnabled(False)
        self.create_markdown_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0078d4, stop:1 #00bcf2);
                color: white;
                font-weight: bold;
                font-size: 16px;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #106ebe, stop:1 #00a8e8);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #005a9e, stop:1 #0096d6);
            }
            QPushButton:disabled {
                background: #cccccc;
                color: #666666;
            }
        """)

        # Status info
        self.status_label = QLabel("Найдено файлов: 0, Показано: 0, Выбрано: 0")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 14px;
                padding: 8px 0px;
            }
        """)

        # Progress bar (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                text-align: center;
                background-color: #f8f9fa;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0078d4, stop:1 #00bcf2);
                border-radius: 6px;
            }
        """)

        # Cancel button (hidden by default)
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setVisible(False)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f8f9fa;
                color: #333333;
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                font-weight: 500;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                border-color: #dc3545;
            }
        """)
        self.cancel_btn.clicked.connect(self._cancel_operation)

        # Layout
        action_layout = QVBoxLayout()
        action_layout.setSpacing(12)
        action_layout.addWidget(self.create_markdown_btn)
        action_layout.addWidget(self.status_label)
        action_layout.addWidget(self.progress_bar)
        action_layout.addWidget(self.cancel_btn)

        parent_layout.addLayout(action_layout)


    def _setup_connections(self) -> None:
        """Set up signal connections."""
        self.select_folder_btn.clicked.connect(self._select_folder)
        self.create_markdown_btn.clicked.connect(self._create_markdown)

        # Files list selection - use itemChanged for checkboxes
        self.files_list.itemChanged.connect(self._on_file_item_changed)

    def _load_settings(self) -> None:
        """Load window settings."""
        settings = QSettings("CodeToMarkdown", "MainWindow")

        # Restore geometry
        geometry = settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)

        # Restore splitter state
        splitter_state = settings.value("splitterState")
        if splitter_state and hasattr(self, "main_splitter"):
            self.main_splitter.restoreState(splitter_state)

    def _save_settings(self) -> None:
        """Save window settings."""
        settings = QSettings("CodeToMarkdown", "MainWindow")
        settings.setValue("geometry", self.saveGeometry())
        if hasattr(self, "main_splitter"):
            settings.setValue("splitterState", self.main_splitter.saveState())

    def _select_folder(self) -> None:
        """Select project folder."""
        folder = QFileDialog.getExistingDirectory(
            self,
            get_text("select_folder"),
            self.config.last_project_path or str(Path.home()),
        )

        if folder:
            project_path = Path(folder)
            self._set_project_path(project_path)

    def _set_project_path(self, project_path: Path) -> None:
        """Set project path and update UI.
        
        Args:
            project_path: Path to project directory.
        """
        self.current_project_path = project_path
        self.project_path_input.setText(str(project_path))

        # Save to config
        self.config.last_project_path = str(project_path)
        self.config.save_config()

        # Enable buttons
        self.create_markdown_btn.setEnabled(True)

        # Clear previous data
        self.files_list.clear()
        self.current_files = []
        self.selected_files = set()

        # Reset statistics
        self.total_files_in_project = 0
        self.shown_files_count = 0

        # Reset file selection state
        # (select all checkbox was removed as requested)

        # Update status
        self._update_status()

        # Start file discovery
        self._discover_files()

    def _discover_files(self) -> None:
        """Start file discovery process."""
        if not self.current_project_path:
            return

        self._set_processing_state(True, "Сканирование файлов...")

        signals = self.worker_manager.start_file_discovery(
            project_path=self.current_project_path,
            include_gitignore=True,  # Always include .gitignore
            include_config_files=True,  # Always include config files
            max_file_size_mb=5,
        )

        signals.files_discovered.connect(self._on_files_discovered)
        signals.task_completed.connect(self._on_discovery_completed)
        signals.error_occurred.connect(self._on_error_occurred)

    def _on_files_discovered(self, files: list[Path]) -> None:
        """Handle files discovered.
        
        Args:
            files: List of discovered files.
        """
        self.current_files = files
        self._populate_file_tree_optimized(files)

    def _populate_file_tree_optimized(self, files: list[Path]) -> None:
        """Оптимизированное заполнение дерева файлов.
        
        Args:
            files: List of file paths that can be added to markdown.
        """
        self.files_list.clear()
        self._initializing = True

        try:
            # Создаем set of allowed files
            allowed = {str(p.relative_to(self.current_project_path)) for p in files}

            # Получаем все файлы в проекте
            all_files = []
            for file_path in self.current_project_path.rglob("*"):
                if file_path.is_file():
                    rel_path = file_path.relative_to(self.current_project_path)
                    all_files.append(rel_path)

            # Сохраняем общее количество файлов в проекте
            self.total_files_in_project = len(all_files)

            # Если файлов слишком много, показываем только разрешенные
            if len(all_files) > self.max_tree_items and not self.show_all_files:
                self._populate_tree_with_allowed_only(allowed)
                self.shown_files_count = len(allowed)
            else:
                self._populate_tree_with_all_files(all_files, allowed)
                self.shown_files_count = min(len(all_files), self.max_tree_items)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при заполнении дерева файлов: {e}")
        finally:
            self._initializing = False
            self._update_selected_files()
            self._update_status()

    def _populate_tree_with_allowed_only(self, allowed: set) -> None:
        """Заполнение дерева только разрешенными файлами.
        
        Args:
            allowed: Set of allowed file paths.
        """
        # Группируем файлы по директориям
        dirs = {}
        for file_path in allowed:
            path = Path(file_path)
            parent_dir = str(path.parent) if path.parent != Path() else "."

            if parent_dir not in dirs:
                dirs[parent_dir] = []
            dirs[parent_dir].append(path)

        # Создаем элементы дерева
        for dir_path in sorted(dirs.keys()):
            if dir_path == ".":
                parent_item = self.files_list.invisibleRootItem()
            else:
                parent_item = QTreeWidgetItem(self.files_list, [dir_path])
                parent_item.setExpanded(True)
                parent_item.setFlags(parent_item.flags() & ~Qt.ItemIsUserCheckable)
                parent_item.setData(0, Qt.UserRole, f"dir:{dir_path}")

            for file_path in sorted(dirs[dir_path]):
                self._create_file_item(parent_item, str(file_path), True)

    def _populate_tree_with_all_files(self, all_files: list[Path], allowed: set) -> None:
        """Заполнение дерева всеми файлами (с ограничением).
        
        Args:
            all_files: List of all file paths.
            allowed: Set of allowed file paths.
        """
        # Группируем файлы по директориям
        dirs = {}
        for file_path in all_files:
            parent_dir = str(file_path.parent) if file_path.parent != Path() else "."

            if parent_dir not in dirs:
                dirs[parent_dir] = []
            dirs[parent_dir].append(file_path)

        # Создаем элементы дерева
        items_created = 0
        for dir_path in sorted(dirs.keys()):
            if items_created >= self.max_tree_items:
                # Добавляем элемент "Показать больше..."
                more_item = QTreeWidgetItem(self.files_list, [f"... и еще {len(all_files) - items_created} файлов"])
                more_item.setFlags(more_item.flags() & ~Qt.ItemIsUserCheckable)
                more_item.setForeground(0, QBrush(QColor(100, 100, 100)))
                break

            if dir_path == ".":
                parent_item = self.files_list.invisibleRootItem()
            else:
                parent_item = QTreeWidgetItem(self.files_list, [dir_path])
                parent_item.setExpanded(True)
                parent_item.setFlags(parent_item.flags() & ~Qt.ItemIsUserCheckable)
                parent_item.setData(0, Qt.UserRole, f"dir:{dir_path}")
                items_created += 1

            for file_path in sorted(dirs[dir_path]):
                if items_created >= self.max_tree_items:
                    break

                can_add = str(file_path) in allowed and "PROJECT_CODEBUNDLE" not in str(file_path)
                self._create_file_item(parent_item, str(file_path), can_add)
                items_created += 1

        # Обновляем количество показанных файлов
        self.shown_files_count = items_created

    def _create_file_item(self, parent_item: QTreeWidgetItem, file_path: str, can_add: bool) -> None:
        """Создание элемента файла.
        
        Args:
            parent_item: Parent tree item.
            file_path: File path.
            can_add: Whether file can be added to markdown.
        """
        file_item = QTreeWidgetItem(parent_item, [file_path])

        if can_add:
            file_item.setFlags(file_item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            file_item.setCheckState(0, Qt.Checked)
            file_item.setToolTip(0, "Можно добавить в Markdown")
        else:
            flags = file_item.flags()
            flags &= ~(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            file_item.setFlags(flags)
            file_item.setDisabled(True)
            file_item.setCheckState(0, Qt.Unchecked)
            file_item.setForeground(0, QBrush(QColor(154, 160, 166)))

            if "PROJECT_CODEBUNDLE" in file_path:
                file_item.setToolTip(0, "Нельзя добавить в Markdown (содержит PROJECT_CODEBUNDLE)")
            else:
                file_item.setToolTip(0, "Нельзя добавить в Markdown (неподходящий тип/размер)")

        file_item.setData(0, Qt.UserRole, f"file:{file_path}")

    def _on_file_item_changed(self, item: QTreeWidgetItem, column: int) -> None:
        """Handle file item checkbox change in tree.
        
        Args:
            item: Changed tree item.
            column: Column index.
        """
        # Update selected files
        self._update_selected_files()
        self._update_status()


    def _update_selected_files(self) -> None:
        """Update the set of selected files."""
        self.selected_files.clear()

        def collect_selected_files(item):
            if item.flags() & Qt.ItemIsUserCheckable:
                if item.checkState(0) == Qt.Checked:
                    data = item.data(0, Qt.UserRole)
                    if data and data.startswith("file:"):
                        file_path = data[5:]  # Remove "file:" prefix
                        self.selected_files.add(file_path)
            for i in range(item.childCount()):
                collect_selected_files(item.child(i))

        for i in range(self.files_list.topLevelItemCount()):
            collect_selected_files(self.files_list.topLevelItem(i))

    def _update_status(self) -> None:
        """Update status label."""
        total_files = len(self.current_files)
        selected_count = len(self.selected_files)

        # Отображаем статистику: Найдено, Показано, Выбрано
        self.status_label.setText(
            f"Найдено файлов: {self.total_files_in_project}, "
            f"Показано: {self.shown_files_count}, "
            f"Выбрано: {selected_count}",
        )

        # Enable/disable create button based on selection
        self.create_markdown_btn.setEnabled(selected_count > 0)


    def _generate_preview(self) -> None:
        """Generate markdown preview."""
        if not self.current_files or not self.current_project_path:
            QMessageBox.warning(
                self,
                "Предупреждение",
                "Сначала выберите папку проекта и дождитесь завершения сканирования файлов.",
            )
            return

        self._set_processing_state(True, "Генерация предпросмотра...")

        signals = self.worker_manager.start_preview_generation(
            project_path=self.current_project_path,
            files=self.current_files,
            max_lines=200,
        )

        signals.preview_generated.connect(self._on_preview_generated)
        signals.task_completed.connect(self._on_preview_completed)
        signals.error_occurred.connect(self._on_error_occurred)

    def _on_preview_generated(self, preview_content: str) -> None:
        """Handle preview generated.
        
        Args:
            preview_content: Generated preview content.
        """
        # Show preview in a dialog
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Предпросмотр Markdown")
        dialog.setText("Предпросмотр сгенерирован успешно!")
        dialog.setDetailedText(preview_content)
        dialog.setIcon(QMessageBox.Information)
        dialog.exec()

    def _on_preview_completed(self, success: bool) -> None:
        """Handle preview generation completed.
        
        Args:
            success: Whether generation was successful.
        """
        self._set_processing_state(False)


    def _create_markdown(self) -> None:
        """Create markdown file."""
        if not self.selected_files or not self.current_project_path:
            return

        # Convert selected file paths to full paths
        selected_full_paths = []
        for rel_path in self.selected_files:
            full_path = self.current_project_path / Path(rel_path)
            if full_path.exists():
                selected_full_paths.append(full_path)

        if not selected_full_paths:
            QMessageBox.warning(
                self,
                "Предупреждение",
                "Выбранные файлы не найдены.",
            )
            return

        # Choose output file
        output_file, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить Markdown файл",
            str(self.current_project_path / "PROJECT_CODEBUNDLE.md"),
            "Markdown файлы (*.md);;Все файлы (*)",
        )

        if not output_file:
            return

        output_path = Path(output_file)
        self._set_processing_state(True, "Создание Markdown...")

        signals = self.worker_manager.start_markdown_generation(
            project_path=self.current_project_path,
            files=selected_full_paths,  # Use only selected files
            output_path=output_path,
            include_gitignore=True,  # Always include .gitignore
            include_large_files=True,  # Always include large files
            include_config_files=True,  # Always include config files
            max_file_size_mb=5,
        )

        signals.markdown_generated.connect(self._on_markdown_generated)
        signals.task_completed.connect(self._on_markdown_completed)
        signals.error_occurred.connect(self._on_error_occurred)

    def _on_markdown_generated(self, output_path: str) -> None:
        """Handle markdown generated.
        
        Args:
            output_path: Path to generated markdown file.
        """
        # Show success message
        msg = QMessageBox(self)
        msg.setWindowTitle(get_text("file_saved"))
        msg.setText(get_text("file_saved_message", path=output_path))
        msg.setIcon(QMessageBox.Information)

        open_folder_btn = msg.addButton(get_text("open_folder"), QMessageBox.ActionRole)
        msg.addButton("OK", QMessageBox.AcceptRole)

        msg.exec()

        if msg.clickedButton() == open_folder_btn:
            self._open_folder(Path(output_path).parent)

    def _open_folder(self, folder_path: Path) -> None:
        """Open folder in file explorer.
        
        Args:
            folder_path: Path to folder.
        """
        open_file_explorer(folder_path)


    def _set_processing_state(self, processing: bool, message: str = "") -> None:
        """Set processing state.
        
        Args:
            processing: Whether processing is active.
            message: Status message.
        """
        self.progress_bar.setVisible(processing)
        self.cancel_btn.setVisible(processing)

        if processing:
            self.progress_bar.setRange(0, 0)  # Indeterminate progress
            self.status_label.setText(message)
            self.status_bar.showMessage(message)
        else:
            self.progress_bar.setRange(0, 100)
            self.status_label.setText(get_text("ready"))
            self.status_bar.showMessage(get_text("ready"))

    def _cancel_operation(self) -> None:
        """Cancel current operation."""
        self.worker_manager.cancel_all_workers()
        self._set_processing_state(False)

    def _on_discovery_completed(self, success: bool) -> None:
        """Handle file discovery completed.
        
        Args:
            success: Whether discovery was successful.
        """
        self._set_processing_state(False)
        if success:
            self._update_status()


    def _on_markdown_completed(self, success: bool) -> None:
        """Handle markdown generation completed.
        
        Args:
            success: Whether generation was successful.
        """
        self._set_processing_state(False)

    def _on_error_occurred(self, error_message: str) -> None:
        """Handle error occurred.
        
        Args:
            error_message: Error message.
        """
        self._set_processing_state(False)

        msg = QMessageBox(self)
        msg.setWindowTitle(get_text("error_occurred"))
        msg.setText(error_message)
        msg.setIcon(QMessageBox.Critical)
        msg.exec()

    def _show_about(self) -> None:
        """Show about dialog."""
        msg = QMessageBox(self)
        msg.setWindowTitle("О программе")
        msg.setText("""
        <h3>Code to Markdown</h3>
        <p>Версия 1.0.0</p>
        <p>Инструмент для конвертации исходного кода проекта в Markdown файл.</p>
        <p>Разработано с использованием PySide6 и Python.</p>
        """)
        msg.setIcon(QMessageBox.Information)
        msg.exec()

    def closeEvent(self, event) -> None:
        """Handle window close event.
        
        Args:
            event: Close event.
        """
        # Cancel any running operations
        self.worker_manager.cancel_all_workers()

        # Save settings
        self._save_settings()

        # Save config
        self.config.save_config()

        event.accept()

```

## app\utils.py

**Описание:** Utility functions for the application.

**Размер:** 0.00 МБ | **Строки:** 94 | **Хэш:** `96a0edbf019c`

```python
"""Utility functions for the application."""

import logging
import os
import subprocess
import sys
from pathlib import Path


def open_file_explorer(folder_path: Path) -> None:
    """Open file explorer for the given folder.
    
    Args:
        folder_path: Path to the folder to open.
    """
    try:
        if sys.platform == "win32":
            os.startfile(str(folder_path))
        elif sys.platform == "darwin":
            subprocess.run(["open", str(folder_path)], check=True)
        else:  # Linux and others
            subprocess.run(["xdg-open", str(folder_path)], check=True)
    except Exception as e:
        logging.getLogger(__name__).warning(f"Failed to open file explorer: {e}")


def read_file_safe(file_path: Path, encodings: tuple[str, ...] = ("utf-8", "latin-1")) -> str | None:
    """Safely read file content with multiple encoding fallbacks.
    
    Args:
        file_path: Path to the file to read.
        encodings: Tuple of encodings to try in order.
        
    Returns:
        File content or None if all encodings fail.
    """
    for encoding in encodings:
        try:
            with open(file_path, encoding=encoding) as f:
                return f.read()
        except (UnicodeDecodeError, OSError):
            continue

    logging.getLogger(__name__).warning(f"Failed to read file {file_path} with any encoding")
    return None


def get_file_size_mb(file_path: Path) -> float:
    """Get file size in megabytes.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        File size in MB.
    """
    try:
        return file_path.stat().st_size / (1024 * 1024)
    except OSError:
        return 0.0


def is_binary_file(file_path: Path, chunk_size: int = 8192) -> bool:
    """Check if file contains binary data.
    
    Args:
        file_path: Path to the file.
        chunk_size: Size of chunk to read for analysis.
        
    Returns:
        True if file appears to be binary.
    """
    try:
        with open(file_path, "rb") as f:
            chunk = f.read(chunk_size)
            return b"\x00" in chunk
    except OSError:
        return True


def clean_filename_for_anchor(filename: str) -> str:
    """Clean filename for use as markdown anchor.
    
    Args:
        filename: Original filename.
        
    Returns:
        Cleaned anchor string.
    """
    # Convert to string and replace problematic characters
    anchor = str(filename).replace("\\", "-").replace("/", "-")
    anchor = anchor.replace(" ", "-").replace(".", "-")
    anchor = "".join(c.lower() if c.isalnum() or c == "-" else "" for c in anchor)
    return anchor

```

## app\worker.py

**Описание:** Background worker for file processing and markdown generation.

**Размер:** 0.01 МБ | **Строки:** 348 | **Хэш:** `f5c8cbbc3d1b`

```python
"""Background worker for file processing and markdown generation."""

import logging
from pathlib import Path

from PySide6.QtCore import QMutex, QMutexLocker, QObject, QRunnable, QThreadPool, Signal

from app.file_discovery import FileDiscovery
from app.i18n import get_text
from app.md_builder import MarkdownBuilder


class WorkerSignals(QObject):
    """Signals for worker communication."""

    # Progress signals
    progress = Signal(int, str)  # progress_percent, status_message
    file_processed = Signal(str)  # file_name
    error_occurred = Signal(str)  # error_message

    # Completion signals
    files_discovered = Signal(list)  # list of file paths
    markdown_generated = Signal(str)  # output_file_path
    preview_generated = Signal(str)  # preview_content
    task_completed = Signal(bool)  # success
    task_cancelled = Signal()


class FileDiscoveryWorker(QRunnable):
    """Worker for file discovery."""

    def __init__(
        self,
        project_path: Path,
        include_gitignore: bool = True,
        include_config_files: bool = True,
        max_file_size_mb: int = 5,
    ):
        """Initialize file discovery worker.
        
        Args:
            project_path: Path to project directory.
            include_gitignore: Whether to respect .gitignore.
            include_config_files: Whether to include config files.
            max_file_size_mb: Maximum file size in MB.
        """
        super().__init__()
        self.project_path = project_path
        self.include_gitignore = include_gitignore
        self.include_config_files = include_config_files
        self.max_file_size_mb = max_file_size_mb
        self.signals = WorkerSignals()
        self.logger = logging.getLogger(__name__)
        self._cancelled = False

    def run(self) -> None:
        """Run file discovery."""
        try:
            self.signals.progress.emit(0, get_text("scanning_files"))

            discovery = FileDiscovery(
                include_gitignore=self.include_gitignore,
                include_config=self.include_config_files,
            )

            files = discovery.discover_files(self.project_path, self.max_file_size_mb)

            if self._cancelled:
                self.signals.task_cancelled.emit()
                return

            self.signals.files_discovered.emit(files)
            self.signals.progress.emit(100, get_text("completed"))
            self.signals.task_completed.emit(True)

        except Exception as e:
            self.logger.error(f"Error in file discovery: {e}")
            self.signals.error_occurred.emit(str(e))
            self.signals.task_completed.emit(False)

    def cancel(self) -> None:
        """Cancel the task."""
        self._cancelled = True


class MarkdownGenerationWorker(QRunnable):
    """Worker for markdown generation."""

    def __init__(
        self,
        project_path: Path,
        files: list[Path],
        output_path: Path,
        include_gitignore: bool = True,
        include_large_files: bool = False,
        include_config_files: bool = True,
        max_file_size_mb: int = 5,
    ):
        """Initialize markdown generation worker.
        
        Args:
            project_path: Path to project directory.
            files: List of files to process.
            output_path: Path to output markdown file.
            include_gitignore: Whether to respect .gitignore.
            include_large_files: Whether to include large files.
            include_config_files: Whether to include config files.
            max_file_size_mb: Maximum file size in MB.
        """
        super().__init__()
        self.project_path = project_path
        self.files = files
        self.output_path = output_path
        self.include_gitignore = include_gitignore
        self.include_large_files = include_large_files
        self.include_config_files = include_config_files
        self.max_file_size_mb = max_file_size_mb
        self.signals = WorkerSignals()
        self.logger = logging.getLogger(__name__)
        self._cancelled = False

    def run(self) -> None:
        """Run markdown generation."""
        try:
            self.signals.progress.emit(0, get_text("generating_markdown"))

            builder = MarkdownBuilder()

            def progress_callback(percent: int, message: str) -> None:
                if self._cancelled:
                    return
                self.signals.progress.emit(percent, message)

            success = builder.build_markdown(
                project_path=self.project_path,
                output_path=self.output_path,
                include_gitignore=self.include_gitignore,
                include_large_files=self.include_large_files,
                include_config_files=self.include_config_files,
                max_file_size_mb=self.max_file_size_mb,
                progress_callback=progress_callback,
            )

            if self._cancelled:
                self.signals.task_cancelled.emit()
                return

            if success:
                self.signals.markdown_generated.emit(str(self.output_path))
                self.signals.task_completed.emit(True)
            else:
                self.signals.error_occurred.emit("Failed to generate markdown")
                self.signals.task_completed.emit(False)

        except Exception as e:
            self.logger.error(f"Error in markdown generation: {e}")
            self.signals.error_occurred.emit(str(e))
            self.signals.task_completed.emit(False)

    def cancel(self) -> None:
        """Cancel the task."""
        self._cancelled = True


class PreviewGenerationWorker(QRunnable):
    """Worker for preview generation."""

    def __init__(
        self,
        project_path: Path,
        files: list[Path],
        max_lines: int = 200,
    ):
        """Initialize preview generation worker.
        
        Args:
            project_path: Path to project directory.
            files: List of files to process.
            max_lines: Maximum lines in preview.
        """
        super().__init__()
        self.project_path = project_path
        self.files = files
        self.max_lines = max_lines
        self.signals = WorkerSignals()
        self.logger = logging.getLogger(__name__)
        self._cancelled = False

    def run(self) -> None:
        """Run preview generation."""
        try:
            self.signals.progress.emit(0, "Generating preview...")

            builder = MarkdownBuilder()
            preview = builder.generate_preview(
                project_path=self.project_path,
                files=self.files,
                max_lines=self.max_lines,
            )

            if self._cancelled:
                self.signals.task_cancelled.emit()
                return

            self.signals.preview_generated.emit(preview)
            self.signals.progress.emit(100, get_text("completed"))
            self.signals.task_completed.emit(True)

        except Exception as e:
            self.logger.error(f"Error in preview generation: {e}")
            self.signals.error_occurred.emit(str(e))
            self.signals.task_completed.emit(False)

    def cancel(self) -> None:
        """Cancel the task."""
        self._cancelled = True


class WorkerManager:
    """Manager for background workers."""

    def __init__(self) -> None:
        """Initialize worker manager."""
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(2)  # Limit concurrent workers
        self.logger = logging.getLogger(__name__)
        self._active_workers = []
        self._mutex = QMutex()

    def start_file_discovery(
        self,
        project_path: Path,
        include_gitignore: bool = True,
        include_config_files: bool = True,
        max_file_size_mb: int = 5,
    ) -> WorkerSignals:
        """Start file discovery worker.
        
        Args:
            project_path: Path to project directory.
            include_gitignore: Whether to respect .gitignore.
            include_config_files: Whether to include config files.
            max_file_size_mb: Maximum file size in MB.
            
        Returns:
            Worker signals for communication.
        """
        worker = FileDiscoveryWorker(
            project_path=project_path,
            include_gitignore=include_gitignore,
            include_config_files=include_config_files,
            max_file_size_mb=max_file_size_mb,
        )

        with QMutexLocker(self._mutex):
            self._active_workers.append(worker)

        self.thread_pool.start(worker)
        return worker.signals

    def start_markdown_generation(
        self,
        project_path: Path,
        files: list[Path],
        output_path: Path,
        include_gitignore: bool = True,
        include_large_files: bool = False,
        include_config_files: bool = True,
        max_file_size_mb: int = 5,
    ) -> WorkerSignals:
        """Start markdown generation worker.
        
        Args:
            project_path: Path to project directory.
            files: List of files to process.
            output_path: Path to output markdown file.
            include_gitignore: Whether to respect .gitignore.
            include_large_files: Whether to include large files.
            include_config_files: Whether to include config files.
            max_file_size_mb: Maximum file size in MB.
            
        Returns:
            Worker signals for communication.
        """
        worker = MarkdownGenerationWorker(
            project_path=project_path,
            files=files,
            output_path=output_path,
            include_gitignore=include_gitignore,
            include_large_files=include_large_files,
            include_config_files=include_config_files,
            max_file_size_mb=max_file_size_mb,
        )

        with QMutexLocker(self._mutex):
            self._active_workers.append(worker)

        self.thread_pool.start(worker)
        return worker.signals

    def start_preview_generation(
        self,
        project_path: Path,
        files: list[Path],
        max_lines: int = 200,
    ) -> WorkerSignals:
        """Start preview generation worker.
        
        Args:
            project_path: Path to project directory.
            files: List of files to process.
            max_lines: Maximum lines in preview.
            
        Returns:
            Worker signals for communication.
        """
        worker = PreviewGenerationWorker(
            project_path=project_path,
            files=files,
            max_lines=max_lines,
        )

        with QMutexLocker(self._mutex):
            self._active_workers.append(worker)

        self.thread_pool.start(worker)
        return worker.signals

    def cancel_all_workers(self) -> None:
        """Cancel all active workers."""
        with QMutexLocker(self._mutex):
            for worker in self._active_workers:
                if hasattr(worker, "cancel"):
                    worker.cancel()
            self._active_workers.clear()

        self.thread_pool.clear()

    def wait_for_completion(self, timeout: int = 30000) -> bool:
        """Wait for all workers to complete.
        
        Args:
            timeout: Timeout in milliseconds.
            
        Returns:
            True if all workers completed, False if timeout.
        """
        return self.thread_pool.waitForDone(timeout)

```

## build.py

**Описание:** Python модуль с 7 функциями и 0 классами

**Размер:** 0.01 МБ | **Строки:** 233 | **Хэш:** `98663b140160`

```python
#!/usr/bin/env python3
"""
Скрипт сборки исполняемого файла Code to Markdown.

Автоматизирует процесс сборки .exe файла с помощью PyInstaller.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(cmd: list, description: str) -> bool:
    """Выполнить команду с обработкой ошибок.
    
    Args:
        cmd: Команда для выполнения.
        description: Описание команды.
        
    Returns:
        True если команда выполнена успешно.
    """
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} завершено успешно")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при {description}:")
        print(f"   Код возврата: {e.returncode}")
        print(f"   Вывод: {e.stdout}")
        print(f"   Ошибки: {e.stderr}")
        return False


def check_requirements() -> bool:
    """Проверить наличие необходимых зависимостей.
    
    Returns:
        True если все зависимости установлены.
    """
    print("🔍 Проверка зависимостей...")
    
    required_packages = {
        "PySide6": "PySide6",
        "pathspec": "pathspec", 
        "PyInstaller": "PyInstaller"
    }
    
    missing_packages = []
    
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"❌ Отсутствуют пакеты: {', '.join(missing_packages)}")
        print("   Установите их командой: pip install -e .")
        return False
    
    print("✅ Все зависимости установлены")
    return True


def clean_build_dirs() -> None:
    """Очистить папки сборки."""
    print("🧹 Очистка папок сборки...")
    
    dirs_to_clean = ["build", "dist", "__pycache__"]
    
    for dir_name in dirs_to_clean:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"   Удалена папка: {dir_name}")
    
    # Удалить .spec файлы
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()
        print(f"   Удален файл: {spec_file}")


def build_executable() -> bool:
    """Собрать исполняемый файл.
    
    Returns:
        True если сборка успешна.
    """
    print("🔨 Сборка исполняемого файла...")
    
    # Команда PyInstaller
    cmd = [
        "pyinstaller",
        "app/main.py",
        "--name", "CodeToMarkdown",
        "--onefile",
        "--noconsole",
        "--clean",
        "--noconfirm"
    ]
    
    # Добавить иконку если есть
    icon_path = Path("app/icon.ico")
    if icon_path.exists():
        cmd.extend(["--icon", str(icon_path)])
        print(f"   Используется иконка: {icon_path}")
    
    # Добавить дополнительные файлы
    cmd.extend([
        "--add-data", "app;app",
        "--hidden-import", "PySide6.QtCore",
        "--hidden-import", "PySide6.QtWidgets", 
        "--hidden-import", "PySide6.QtGui",
        "--hidden-import", "pathspec"
    ])
    
    return run_command(cmd, "Сборка с PyInstaller")


def test_executable() -> bool:
    """Протестировать собранный исполняемый файл.
    
    Returns:
        True если тест прошел успешно.
    """
    exe_path = Path("dist/CodeToMarkdown.exe")
    
    if not exe_path.exists():
        print("❌ Исполняемый файл не найден")
        return False
    
    print(f"🧪 Тестирование {exe_path}...")
    
    # Простой тест - запуск с --help (если поддерживается)
    try:
        result = subprocess.run(
            [str(exe_path), "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        print("✅ Исполняемый файл запускается")
        return True
    except subprocess.TimeoutExpired:
        print("⚠️  Таймаут при тестировании (возможно, GUI запустился)")
        return True
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        return False


def create_installer_script() -> None:
    """Создать скрипт установки."""
    print("📝 Создание скрипта установки...")
    
    installer_content = '''@echo off
echo Установка Code to Markdown...
echo.

REM Создать папку в Program Files
set "INSTALL_DIR=%PROGRAMFILES%\\CodeToMarkdown"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Копировать файлы
copy "CodeToMarkdown.exe" "%INSTALL_DIR%\\"
if exist "README.md" copy "README.md" "%INSTALL_DIR%\\"

REM Создать ярлык на рабочем столе
set "DESKTOP=%USERPROFILE%\\Desktop"
echo [InternetShortcut] > "%DESKTOP%\\Code to Markdown.url"
echo URL=file:///%INSTALL_DIR%\\CodeToMarkdown.exe >> "%DESKTOP%\\Code to Markdown.url"
echo IconFile=%INSTALL_DIR%\\CodeToMarkdown.exe >> "%DESKTOP%\\Code to Markdown.url"
echo IconIndex=0 >> "%DESKTOP%\\Code to Markdown.url"

echo.
echo Установка завершена!
echo Ярлык создан на рабочем столе.
echo.
pause
'''
    
    installer_path = Path("dist/install.bat")
    installer_path.write_text(installer_content, encoding='utf-8')
    print(f"   Создан: {installer_path}")


def main() -> int:
    """Главная функция сборки.
    
    Returns:
        Код завершения.
    """
    print("🚀 Сборка Code to Markdown")
    print("=" * 50)
    
    # Проверка зависимостей
    if not check_requirements():
        return 1
    
    # Очистка
    clean_build_dirs()
    
    # Сборка
    if not build_executable():
        return 1
    
    # Тестирование
    if not test_executable():
        print("⚠️  Тестирование не прошло, но сборка завершена")
    
    # Создание скрипта установки
    create_installer_script()
    
    # Информация о результате
    exe_path = Path("dist/CodeToMarkdown.exe")
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"\n✅ Сборка завершена успешно!")
        print(f"   Файл: {exe_path}")
        print(f"   Размер: {size_mb:.1f} МБ")
        print(f"   Папка: {exe_path.parent.absolute()}")
    else:
        print("\n❌ Сборка не удалась")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

```

## build_release.py

**Описание:** Python модуль с 6 функциями и 0 классами

**Размер:** 0.01 МБ | **Строки:** 221 | **Хэш:** `7c86a678ae62`

```python
#!/usr/bin/env python3
"""
Скрипт для сборки релиза Code to Markdown v1.2.0
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

def run_command(cmd, cwd=None):
    """Выполнить команду и вернуть результат"""
    print(f"Выполняем: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Ошибка: {result.stderr}")
        return False
    print(f"Успешно: {result.stdout}")
    return True

def clean_build_dirs():
    """Очистка директорий сборки"""
    print("🧹 Очистка директорий сборки...")
    
    dirs_to_clean = ["build", "dist", "release"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Удалена папка: {dir_name}")
    
    # Очистка кэша Python
    for root, dirs, files in os.walk("."):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                shutil.rmtree(os.path.join(root, dir_name))
                print(f"   Удален кэш: {os.path.join(root, dir_name)}")

def run_tests():
    """Запуск тестов"""
    print("🧪 Запуск тестов...")
    
    if not run_command("python -m pytest tests/ -v"):
        print("❌ Тесты не прошли!")
        return False
    
    print("✅ Все тесты прошли успешно!")
    return True

def build_executable():
    """Сборка исполняемого файла"""
    print("🔨 Сборка исполняемого файла...")
    
    # Создаем spec файл для PyInstaller
    spec_content = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CodeToMarkdown',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
"""
    
    with open("CodeToMarkdown.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    # Сборка с PyInstaller
    if not run_command("pyinstaller CodeToMarkdown.spec --clean"):
        print("❌ Ошибка сборки!")
        return False
    
    print("✅ Исполняемый файл собран успешно!")
    return True

def create_release_package():
    """Создание пакета релиза"""
    print("📦 Создание пакета релиза...")
    
    version = "1.2.0"
    release_dir = Path("release")
    release_dir.mkdir(exist_ok=True)
    
    # Копируем исполняемый файл
    exe_path = Path("dist/CodeToMarkdown.exe")
    if exe_path.exists():
        shutil.copy2(exe_path, release_dir / f"CodeToMarkdown_v{version}.exe")
        print(f"   Скопирован: CodeToMarkdown_v{version}.exe")
    else:
        print("❌ Исполняемый файл не найден!")
        return False
    
    # Копируем README
    shutil.copy2("README.md", release_dir / "README.md")
    print("   Скопирован: README.md")
    
    # Создаем CHANGELOG
    changelog_content = f"""# Changelog

## [1.2.0] - {datetime.now().strftime('%Y-%m-%d')}

### Добавлено
- ⚡ Автоматическая оптимизация для больших проектов (>1000 файлов)
- 📊 Улучшенная статистика: "Найдено/Показано/Выбрано" файлов
- 🎯 Умная фильтрация файлов по умолчанию
- 🔧 Незаметная оптимизация без настроек

### Исправлено
- Решена проблема зависания на больших проектах (5000+ файлов)
- Улучшена отзывчивость интерфейса
- Оптимизировано создание дерева файлов
- Исправлены проблемы с производительностью

### Технические улучшения
- Интегрирован алгоритм оптимизации в оригинальную версию
- Добавлено отслеживание статистики файлов
- Улучшена логика принятия решений для разных размеров проектов

## [1.1.0] - 2024-09-16

### Добавлено
- Базовая функциональность приложения
- GUI интерфейс на PySide6
- Поддержка .gitignore
- Автоматические аннотации файлов
- Локализация на русском языке
"""
    
    with open(release_dir / "CHANGELOG.md", "w", encoding="utf-8") as f:
        f.write(changelog_content)
    print("   Создан: CHANGELOG.md")
    
    # Создаем архив
    archive_name = f"CodeToMarkdown_v{version}_optimized.zip"
    shutil.make_archive(
        str(release_dir / archive_name.replace('.zip', '')),
        'zip',
        str(release_dir)
    )
    print(f"   Создан архив: {archive_name}")
    
    return True

def main():
    """Главная функция сборки релиза"""
    print("🚀 Начинаем сборку релиза Code to Markdown v1.2.0")
    print("=" * 60)
    
    # Проверяем, что мы в правильной директории
    if not os.path.exists("pyproject.toml"):
        print("❌ Ошибка: Запустите скрипт из корневой папки проекта!")
        sys.exit(1)
    
    try:
        # 1. Очистка
        clean_build_dirs()
        
        # 2. Тесты
        if not run_tests():
            print("❌ Сборка прервана из-за ошибок в тестах!")
            sys.exit(1)
        
        # 3. Сборка исполняемого файла
        if not build_executable():
            print("❌ Сборка прервана из-за ошибки сборки!")
            sys.exit(1)
        
        # 4. Создание пакета релиза
        if not create_release_package():
            print("❌ Сборка прервана из-за ошибки создания пакета!")
            sys.exit(1)
        
        print("=" * 60)
        print("🎉 Релиз v1.2.0 успешно собран!")
        print("📁 Файлы находятся в папке 'release/'")
        print("📦 Архив готов к распространению")
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

```

## CLEAN_OPTIMIZATION_REPORT.md

**Описание:** Markdown файл

**Размер:** 0.01 МБ | **Строки:** 106 | **Хэш:** `b4672868d9e5`

```markdown
# Отчет об удалении настроек производительности из интерфейса

## ✅ Задача выполнена

Настройки производительности успешно удалены из интерфейса, но оптимизация продолжает работать автоматически в фоновом режиме.

## 🔧 Внесенные изменения

### 1. Удалена группа "Настройки производительности"
- ❌ Убрана группа `QGroupBox("Настройки производительности")`
- ❌ Убран спинбокс "Макс. файлов в дереве"
- ❌ Убран чекбокс "Показать все файлы"
- ❌ Удалены методы `_update_max_files()` и `_toggle_show_all()`
- ❌ Убран импорт `QSpinBox`

### 2. Сохранена оптимизация в фоновом режиме
- ✅ Алгоритм `_populate_file_tree_optimized()` работает автоматически
- ✅ Настройки `max_tree_items = 1000` и `show_all_files = False` остались
- ✅ Умная фильтрация работает по умолчанию
- ✅ Ограничение элементов действует автоматически

## 📊 Результаты тестирования

### На папке `D:\_GIT\count-life` (5,120 файлов):

- ⚡ **Время создания дерева**: 0.77 секунды
- 📁 **Показано файлов**: 87 (только подходящие для Markdown)
- ✅ **UI остается отзывчивым**
- ✅ **Оптимизация работает автоматически**

## 🎯 Как работает оптимизация

### Автоматические настройки:
```python
# Настройки оптимизации (в коде)
self.max_tree_items = 1000  # Максимальное количество элементов в дереве
self.show_all_files = False  # Показывать только подходящие файлы
```

### Логика оптимизации:
```python
# Если файлов слишком много, показываем только разрешенные
if len(all_files) > self.max_tree_items and not self.show_all_files:
    self._populate_tree_with_allowed_only(allowed)  # Быстрый режим
else:
    self._populate_tree_with_all_files(all_files, allowed)  # Полный режим
```

## 🎨 Интерфейс

### До изменений:
- Группа "Настройки производительности"
- Спинбокс "Макс. файлов в дереве"
- Чекбокс "Показать все файлы"

### После изменений:
- ✅ Чистый интерфейс без настроек производительности
- ✅ Только основные элементы: путь к проекту, дерево файлов, кнопка создания
- ✅ Оптимизация работает незаметно для пользователя

## 🚀 Преимущества

### 1. Простота использования
- Пользователь не видит сложных настроек
- Приложение работает быстро "из коробки"
- Не нужно настраивать параметры производительности

### 2. Автоматическая оптимизация
- Умная фильтрация файлов по умолчанию
- Ограничение элементов для больших проектов
- Быстрая работа с любыми размерами проектов

### 3. Обратная совместимость
- Все функции работают как раньше
- Дизайн остался прежним
- Производительность улучшена

## 📈 Сравнение производительности

### До оптимизации:
- ⏱️ Время создания дерева: 12+ секунд
- 🚫 UI блокируется
- 😤 Пользователь думает, что приложение зависло

### После оптимизации (с настройками):
- ⚡ Время создания дерева: 1-2 секунды
- ⚙️ Пользователь может настраивать параметры
- ✅ UI остается отзывчивым

### После оптимизации (без настроек):
- ⚡ Время создания дерева: 0.77 секунды
- 🤖 Оптимизация работает автоматически
- ✅ UI остается отзывчивым
- 🎯 Простота использования

## ✅ Заключение

**Задача выполнена успешно!**

1. ✅ Настройки производительности удалены из интерфейса
2. ✅ Оптимизация продолжает работать автоматически
3. ✅ Интерфейс стал чище и проще
4. ✅ Производительность не пострадала
5. ✅ Проблема зависания решена незаметно для пользователя

**Приложение теперь работает быстро и эффективно с чистым интерфейсом!** 🎉

```

## code_to_markdown.egg-info\dependency_links.txt

**Описание:** Неизвестный тип файла

**Размер:** 0.00 МБ | **Строки:** 1 | **Хэш:** `01ba4719c80b`

```text


```

## code_to_markdown.egg-info\requires.txt

**Описание:** Неизвестный тип файла

**Размер:** 0.00 МБ | **Строки:** 10 | **Хэш:** `f3873413f0f3`

```text
PySide6>=6.5.0
pathspec>=0.11.0

[dev]
pytest>=7.0.0
pytest-qt>=4.2.0
ruff>=0.1.0
black>=23.0.0
mypy>=1.0.0
PyInstaller>=5.0.0

```

## code_to_markdown.egg-info\SOURCES.txt

**Описание:** Неизвестный тип файла

**Размер:** 0.00 МБ | **Строки:** 21 | **Хэш:** `56b780b861ba`

```text
README.md
pyproject.toml
app/__init__.py
app/annotations.py
app/config.py
app/file_discovery.py
app/i18n.py
app/logging_setup.py
app/main.py
app/md_builder.py
app/preview.py
app/ui.py
app/worker.py
code_to_markdown.egg-info/PKG-INFO
code_to_markdown.egg-info/SOURCES.txt
code_to_markdown.egg-info/dependency_links.txt
code_to_markdown.egg-info/requires.txt
code_to_markdown.egg-info/top_level.txt
tests/test_annotations.py
tests/test_file_discovery.py
tests/test_md_builder.py
```

## code_to_markdown.egg-info\top_level.txt

**Описание:** Неизвестный тип файла

**Размер:** 0.00 МБ | **Строки:** 1 | **Хэш:** `8a8f60ecb09b`

```text
app

```

## demo_project\config\config.json

**Описание:** Файл конфигурации

**Размер:** 0.00 МБ | **Строки:** 21 | **Хэш:** `22667c294d4a`

```json
{
  "app_name": "Demo Application",
  "version": "1.0.0",
  "debug": true,
  "port": 8080,
  "host": "localhost",
  "database_url": "sqlite:///demo.db",
  "log_level": "INFO",
  "max_workers": 4,
  "timeout": 30,
  "features": {
    "enable_caching": true,
    "enable_metrics": false,
    "enable_debug_toolbar": true
  },
  "paths": {
    "data_dir": "./data",
    "log_dir": "./logs",
    "temp_dir": "./temp"
  }
}

```

## demo_project\config\settings.py

**Описание:** Python модуль с 14 функциями и 1 классами

**Размер:** 0.01 МБ | **Строки:** 201 | **Хэш:** `f216e3ad2ad9`

```python
"""
Модуль настроек приложения.

Содержит класс для управления конфигурацией приложения,
включая загрузку из файлов и валидацию параметров.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from utils.validators import validate_config, create_default_schema


class AppConfig:
    """Класс для управления конфигурацией приложения."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Инициализация конфигурации.
        
        Args:
            config_path: Путь к файлу конфигурации.
        """
        self.config_path = config_path or "config.json"
        self.config_data: Dict[str, Any] = {}
        self.schema = create_default_schema()
    
    def load(self) -> Dict[str, Any]:
        """Загрузка конфигурации из файла.
        
        Returns:
            Словарь с конфигурацией.
            
        Raises:
            FileNotFoundError: Если файл конфигурации не найден.
            json.JSONDecodeError: Если файл содержит некорректный JSON.
        """
        config_file = Path(self.config_path)
        
        if not config_file.exists():
            # Создать конфигурацию по умолчанию
            self.config_data = self._get_default_config()
            self.save()
            return self.config_data
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config_data = json.load(f)
            
            # Валидация конфигурации
            if not validate_config(self.config_data):
                raise ValueError("Конфигурация не прошла валидацию")
            
            return self.config_data
            
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Ошибка парсинга JSON в {self.config_path}: {e}")
    
    def save(self) -> None:
        """Сохранение конфигурации в файл."""
        config_file = Path(self.config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config_data, f, indent=2, ensure_ascii=False)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Получение значения конфигурации.
        
        Args:
            key: Ключ конфигурации.
            default: Значение по умолчанию.
            
        Returns:
            Значение конфигурации или значение по умолчанию.
        """
        return self.config_data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Установка значения конфигурации.
        
        Args:
            key: Ключ конфигурации.
            value: Значение для установки.
        """
        self.config_data[key] = value
    
    def update(self, config_dict: Dict[str, Any]) -> None:
        """Обновление конфигурации из словаря.
        
        Args:
            config_dict: Словарь с новыми значениями.
        """
        self.config_data.update(config_dict)
    
    def validate(self) -> tuple[bool, list]:
        """Валидация текущей конфигурации.
        
        Returns:
            Кортеж (успех, список ошибок).
        """
        from utils.validators import ConfigValidator
        
        validator = ConfigValidator(self.schema)
        return validator.validate(self.config_data)
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Получение конфигурации по умолчанию.
        
        Returns:
            Словарь с конфигурацией по умолчанию.
        """
        return {
            'app_name': 'Demo Application',
            'version': '1.0.0',
            'debug': False,
            'port': 8080,
            'host': 'localhost',
            'database_url': 'sqlite:///demo.db',
            'log_level': 'INFO',
            'max_workers': 4,
            'timeout': 30,
            'features': {
                'enable_caching': True,
                'enable_metrics': False,
                'enable_debug_toolbar': False
            },
            'paths': {
                'data_dir': './data',
                'log_dir': './logs',
                'temp_dir': './temp'
            }
        }
    
    def get_database_config(self) -> Dict[str, Any]:
        """Получение конфигурации базы данных.
        
        Returns:
            Словарь с конфигурацией БД.
        """
        return {
            'url': self.get('database_url', 'sqlite:///demo.db'),
            'pool_size': self.get('db_pool_size', 5),
            'max_overflow': self.get('db_max_overflow', 10),
            'echo': self.get('debug', False)
        }
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Получение конфигурации логирования.
        
        Returns:
            Словарь с конфигурацией логирования.
        """
        return {
            'level': self.get('log_level', 'INFO'),
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'file': self.get('log_file', 'app.log'),
            'max_size': self.get('log_max_size', 10 * 1024 * 1024),  # 10 MB
            'backup_count': self.get('log_backup_count', 5)
        }
    
    def is_development(self) -> bool:
        """Проверка режима разработки.
        
        Returns:
            True если приложение в режиме разработки.
        """
        return self.get('debug', False) or os.getenv('DEMO_DEBUG', '').lower() == 'true'
    
    def is_production(self) -> bool:
        """Проверка режима продакшена.
        
        Returns:
            True если приложение в режиме продакшена.
        """
        return not self.is_development()
    
    def get_feature_flag(self, feature: str) -> bool:
        """Получение флага функции.
        
        Args:
            feature: Имя функции.
            
        Returns:
            True если функция включена.
        """
        features = self.get('features', {})
        return features.get(feature, False)
    
    def set_feature_flag(self, feature: str, enabled: bool) -> None:
        """Установка флага функции.
        
        Args:
            feature: Имя функции.
            enabled: Включена ли функция.
        """
        if 'features' not in self.config_data:
            self.config_data['features'] = {}
        
        self.config_data['features'][feature] = enabled

```

## demo_project\config.json

**Описание:** Файл конфигурации

**Размер:** 0.00 МБ | **Строки:** 21 | **Хэш:** `ad95a04dce3c`

```json
{
  "app_name": "Demo Application",
  "version": "1.0.0",
  "debug": false,
  "port": 8080,
  "host": "localhost",
  "database_url": "sqlite:///demo.db",
  "log_level": "INFO",
  "max_workers": 4,
  "timeout": 30,
  "features": {
    "enable_caching": true,
    "enable_metrics": false,
    "enable_debug_toolbar": false
  },
  "paths": {
    "data_dir": "./data",
    "log_dir": "./logs",
    "temp_dir": "./temp"
  }
}
```

## demo_project\main.py

**Описание:** Python модуль с 7 функциями и 1 классами

**Размер:** 0.00 МБ | **Строки:** 124 | **Хэш:** `7b3bfb7461d3`

```python
"""
Главный модуль демонстрационного приложения.

Этот модуль содержит основную логику приложения и демонстрирует
различные возможности Python для генерации аннотаций.
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional

from utils.helpers import format_message, calculate_hash
from utils.validators import validate_config
from config.settings import AppConfig


class DemoApp:
    """Демонстрационное приложение."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Инициализация приложения.
        
        Args:
            config_path: Путь к файлу конфигурации.
        """
        self.config = AppConfig(config_path)
        self.data: Dict[str, any] = {}
    
    def run(self) -> int:
        """Запуск приложения.
        
        Returns:
            Код завершения.
        """
        try:
            print("Запуск демонстрационного приложения...")
            
            # Загрузка конфигурации
            if not self._load_config():
                return 1
            
            # Инициализация данных
            self._initialize_data()
            
            # Основной цикл
            self._main_loop()
            
            print("Приложение завершено успешно.")
            return 0
            
        except KeyboardInterrupt:
            print("\nПриложение прервано пользователем.")
            return 1
        except Exception as e:
            print(f"Ошибка: {e}")
            return 1
    
    def _load_config(self) -> bool:
        """Загрузка конфигурации.
        
        Returns:
            True если конфигурация загружена успешно.
        """
        try:
            config_data = self.config.load()
            if not validate_config(config_data):
                print("Ошибка валидации конфигурации.")
                return False
            
            self.data.update(config_data)
            print("Конфигурация загружена успешно.")
            return True
            
        except Exception as e:
            print(f"Ошибка загрузки конфигурации: {e}")
            return False
    
    def _initialize_data(self) -> None:
        """Инициализация данных приложения."""
        self.data['items'] = []
        self.data['processed_count'] = 0
        print("Данные инициализированы.")
    
    def _main_loop(self) -> None:
        """Основной цикл приложения."""
        for i in range(5):
            item = {
                'id': i + 1,
                'name': f'Item {i + 1}',
                'hash': calculate_hash(f'item_{i + 1}'),
                'message': format_message(f'Обработка элемента {i + 1}')
            }
            
            self.data['items'].append(item)
            self.data['processed_count'] += 1
            
            print(f"Обработано: {item['message']}")
    
    def get_statistics(self) -> Dict[str, int]:
        """Получение статистики приложения.
        
        Returns:
            Словарь со статистикой.
        """
        return {
            'total_items': len(self.data.get('items', [])),
            'processed_count': self.data.get('processed_count', 0),
            'config_loaded': 'config' in self.data
        }


def main() -> int:
    """Точка входа в приложение.
    
    Returns:
        Код завершения.
    """
    app = DemoApp()
    return app.run()


if __name__ == '__main__':
    sys.exit(main())

```

## demo_project\README.md

**Описание:** Markdown файл

**Размер:** 0.00 МБ | **Строки:** 27 | **Хэш:** `41504e35641f`

```markdown
# Demo Project

Это демонстрационный проект для тестирования инструмента Code to Markdown.

## Описание

Проект содержит различные типы файлов для демонстрации возможностей конвертации в Markdown.

## Структура

- `main.py` - основной модуль приложения
- `utils/` - вспомогательные модули
- `tests/` - тестовые файлы
- `config/` - файлы конфигурации
- `static/` - статические файлы (CSS, JS)

## Использование

```bash
python main.py
```

## Требования

- Python 3.8+
- requests
- flask

```

## demo_project\static\app.js

**Описание:** app_js

**Размер:** 0.01 МБ | **Строки:** 463 | **Хэш:** `557f9aaa99da`

```javascript
/**
 * JavaScript модуль для демонстрационного приложения.
 * 
 * Содержит функции для интерактивности, валидации форм
 * и работы с API.
 */

// Основной объект приложения
const DemoApp = {
    // Конфигурация
    config: {
        apiUrl: '/api',
        timeout: 5000,
        debug: false
    },
    
    // Инициализация
    init() {
        console.log('Инициализация демонстрационного приложения...');
        this.setupEventListeners();
        this.loadConfiguration();
        this.initializeComponents();
    },
    
    // Настройка обработчиков событий
    setupEventListeners() {
        // Обработчик для кнопок
        document.addEventListener('click', (e) => {
            if (e.target.matches('.btn')) {
                this.handleButtonClick(e.target);
            }
        });
        
        // Обработчик для форм
        document.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleFormSubmit(e.target);
        });
        
        // Обработчик для полей ввода
        document.addEventListener('input', (e) => {
            if (e.target.matches('.form-control')) {
                this.handleInputChange(e.target);
            }
        });
    },
    
    // Загрузка конфигурации
    loadConfiguration() {
        try {
            const config = localStorage.getItem('demoAppConfig');
            if (config) {
                this.config = { ...this.config, ...JSON.parse(config) };
            }
        } catch (error) {
            console.warn('Ошибка загрузки конфигурации:', error);
        }
    },
    
    // Сохранение конфигурации
    saveConfiguration() {
        try {
            localStorage.setItem('demoAppConfig', JSON.stringify(this.config));
        } catch (error) {
            console.warn('Ошибка сохранения конфигурации:', error);
        }
    },
    
    // Инициализация компонентов
    initializeComponents() {
        this.initializeTooltips();
        this.initializeModals();
        this.initializeTabs();
    },
    
    // Инициализация подсказок
    initializeTooltips() {
        const tooltipElements = document.querySelectorAll('[data-tooltip]');
        tooltipElements.forEach(element => {
            element.addEventListener('mouseenter', this.showTooltip);
            element.addEventListener('mouseleave', this.hideTooltip);
        });
    },
    
    // Инициализация модальных окон
    initializeModals() {
        const modalTriggers = document.querySelectorAll('[data-modal]');
        modalTriggers.forEach(trigger => {
            trigger.addEventListener('click', this.openModal);
        });
        
        const modalCloses = document.querySelectorAll('.modal-close');
        modalCloses.forEach(close => {
            close.addEventListener('click', this.closeModal);
        });
    },
    
    // Инициализация вкладок
    initializeTabs() {
        const tabTriggers = document.querySelectorAll('[data-tab]');
        tabTriggers.forEach(trigger => {
            trigger.addEventListener('click', this.switchTab);
        });
    },
    
    // Обработка клика по кнопке
    handleButtonClick(button) {
        const action = button.dataset.action;
        
        switch (action) {
            case 'save':
                this.saveData();
                break;
            case 'load':
                this.loadData();
                break;
            case 'reset':
                this.resetForm();
                break;
            case 'validate':
                this.validateForm();
                break;
            default:
                console.log('Неизвестное действие:', action);
        }
    },
    
    // Обработка отправки формы
    handleFormSubmit(form) {
        if (this.validateForm(form)) {
            this.submitForm(form);
        }
    },
    
    // Обработка изменения поля ввода
    handleInputChange(input) {
        this.validateField(input);
        this.updateFormState();
    },
    
    // Валидация формы
    validateForm(form = null) {
        const targetForm = form || document.querySelector('form');
        if (!targetForm) return false;
        
        const fields = targetForm.querySelectorAll('.form-control[required]');
        let isValid = true;
        
        fields.forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
            }
        });
        
        return isValid;
    },
    
    // Валидация поля
    validateField(field) {
        const value = field.value.trim();
        const type = field.type;
        const required = field.hasAttribute('required');
        
        // Очистка предыдущих ошибок
        this.clearFieldError(field);
        
        // Проверка обязательности
        if (required && !value) {
            this.showFieldError(field, 'Это поле обязательно для заполнения');
            return false;
        }
        
        // Проверка типа
        if (value) {
            switch (type) {
                case 'email':
                    if (!this.isValidEmail(value)) {
                        this.showFieldError(field, 'Введите корректный email');
                        return false;
                    }
                    break;
                case 'url':
                    if (!this.isValidUrl(value)) {
                        this.showFieldError(field, 'Введите корректный URL');
                        return false;
                    }
                    break;
                case 'number':
                    if (isNaN(value)) {
                        this.showFieldError(field, 'Введите корректное число');
                        return false;
                    }
                    break;
            }
        }
        
        return true;
    },
    
    // Проверка email
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },
    
    // Проверка URL
    isValidUrl(url) {
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    },
    
    // Показать ошибку поля
    showFieldError(field, message) {
        field.classList.add('is-invalid');
        
        const errorElement = document.createElement('div');
        errorElement.className = 'invalid-feedback';
        errorElement.textContent = message;
        
        field.parentNode.appendChild(errorElement);
    },
    
    // Очистить ошибку поля
    clearFieldError(field) {
        field.classList.remove('is-invalid');
        
        const errorElement = field.parentNode.querySelector('.invalid-feedback');
        if (errorElement) {
            errorElement.remove();
        }
    },
    
    // Обновить состояние формы
    updateFormState() {
        const form = document.querySelector('form');
        if (!form) return;
        
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            const isValid = this.validateForm(form);
            submitButton.disabled = !isValid;
        }
    },
    
    // Отправить форму
    submitForm(form) {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        console.log('Отправка данных:', data);
        
        // Показать индикатор загрузки
        this.showLoading();
        
        // Имитация отправки
        setTimeout(() => {
            this.hideLoading();
            this.showAlert('Данные успешно отправлены!', 'success');
            form.reset();
        }, 1000);
    },
    
    // Сохранить данные
    saveData() {
        const data = this.collectFormData();
        localStorage.setItem('demoAppData', JSON.stringify(data));
        this.showAlert('Данные сохранены!', 'success');
    },
    
    // Загрузить данные
    loadData() {
        try {
            const data = localStorage.getItem('demoAppData');
            if (data) {
                const parsedData = JSON.parse(data);
                this.populateForm(parsedData);
                this.showAlert('Данные загружены!', 'info');
            } else {
                this.showAlert('Нет сохраненных данных', 'warning');
            }
        } catch (error) {
            this.showAlert('Ошибка загрузки данных', 'danger');
        }
    },
    
    // Сбросить форму
    resetForm() {
        const form = document.querySelector('form');
        if (form) {
            form.reset();
            this.clearAllErrors();
            this.showAlert('Форма сброшена', 'info');
        }
    },
    
    // Собрать данные формы
    collectFormData() {
        const form = document.querySelector('form');
        if (!form) return {};
        
        const formData = new FormData(form);
        return Object.fromEntries(formData.entries());
    },
    
    // Заполнить форму данными
    populateForm(data) {
        Object.entries(data).forEach(([key, value]) => {
            const field = document.querySelector(`[name="${key}"]`);
            if (field) {
                field.value = value;
            }
        });
    },
    
    // Очистить все ошибки
    clearAllErrors() {
        const errorElements = document.querySelectorAll('.invalid-feedback');
        errorElements.forEach(element => element.remove());
        
        const invalidFields = document.querySelectorAll('.is-invalid');
        invalidFields.forEach(field => field.classList.remove('is-invalid'));
    },
    
    // Показать подсказку
    showTooltip(event) {
        const element = event.target;
        const text = element.dataset.tooltip;
        
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = text;
        tooltip.style.cssText = `
            position: absolute;
            background: #333;
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 12px;
            z-index: 1000;
            pointer-events: none;
        `;
        
        document.body.appendChild(tooltip);
        
        const rect = element.getBoundingClientRect();
        tooltip.style.left = rect.left + 'px';
        tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
        
        element._tooltip = tooltip;
    },
    
    // Скрыть подсказку
    hideTooltip(event) {
        const element = event.target;
        if (element._tooltip) {
            element._tooltip.remove();
            delete element._tooltip;
        }
    },
    
    // Открыть модальное окно
    openModal(event) {
        const modalId = event.target.dataset.modal;
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'block';
            modal.classList.add('show');
        }
    },
    
    // Закрыть модальное окно
    closeModal(event) {
        const modal = event.target.closest('.modal');
        if (modal) {
            modal.style.display = 'none';
            modal.classList.remove('show');
        }
    },
    
    // Переключить вкладку
    switchTab(event) {
        const tabId = event.target.dataset.tab;
        
        // Скрыть все вкладки
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        
        // Убрать активность с всех кнопок
        document.querySelectorAll('[data-tab]').forEach(button => {
            button.classList.remove('active');
        });
        
        // Показать выбранную вкладку
        const tabContent = document.getElementById(tabId);
        if (tabContent) {
            tabContent.classList.add('active');
            event.target.classList.add('active');
        }
    },
    
    // Показать индикатор загрузки
    showLoading() {
        const loading = document.createElement('div');
        loading.id = 'loading';
        loading.innerHTML = '<div class="spinner"></div>';
        loading.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        `;
        
        document.body.appendChild(loading);
    },
    
    // Скрыть индикатор загрузки
    hideLoading() {
        const loading = document.getElementById('loading');
        if (loading) {
            loading.remove();
        }
    },
    
    // Показать уведомление
    showAlert(message, type = 'info') {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} fade-in`;
        alert.textContent = message;
        alert.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            min-width: 300px;
        `;
        
        document.body.appendChild(alert);
        
        // Автоматически скрыть через 3 секунды
        setTimeout(() => {
            alert.remove();
        }, 3000);
    }
};

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    DemoApp.init();
});

// Экспорт для использования в других модулях
window.DemoApp = DemoApp;

```

## demo_project\static\style.css

**Описание:** style_css

**Размер:** 0.01 МБ | **Строки:** 332 | **Хэш:** `a24db9e52646`

```css
/* Стили для демонстрационного приложения */

/* Основные стили */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f5f5f5;
    color: #333;
    line-height: 1.6;
}

/* Контейнер */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

/* Заголовки */
h1, h2, h3, h4, h5, h6 {
    color: #2c3e50;
    margin-top: 0;
    margin-bottom: 15px;
}

h1 {
    font-size: 2.5em;
    border-bottom: 3px solid #3498db;
    padding-bottom: 10px;
}

h2 {
    font-size: 2em;
    color: #34495e;
}

h3 {
    font-size: 1.5em;
    color: #7f8c8d;
}

/* Навигация */
.navbar {
    background-color: #2c3e50;
    padding: 15px 0;
    margin-bottom: 30px;
}

.navbar ul {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
}

.navbar li {
    margin: 0 20px;
}

.navbar a {
    color: #ecf0f1;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s ease;
}

.navbar a:hover {
    color: #3498db;
}

/* Карточки */
.card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 25px;
    margin-bottom: 20px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.card-header {
    border-bottom: 1px solid #ecf0f1;
    padding-bottom: 15px;
    margin-bottom: 15px;
}

.card-title {
    font-size: 1.3em;
    color: #2c3e50;
    margin: 0;
}

/* Кнопки */
.btn {
    display: inline-block;
    padding: 12px 24px;
    background-color: #3498db;
    color: white;
    text-decoration: none;
    border-radius: 5px;
    border: none;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s ease;
}

.btn:hover {
    background-color: #2980b9;
}

.btn-success {
    background-color: #27ae60;
}

.btn-success:hover {
    background-color: #229954;
}

.btn-danger {
    background-color: #e74c3c;
}

.btn-danger:hover {
    background-color: #c0392b;
}

.btn-secondary {
    background-color: #95a5a6;
}

.btn-secondary:hover {
    background-color: #7f8c8d;
}

/* Формы */
.form-group {
    margin-bottom: 20px;
}

.form-label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
    color: #2c3e50;
}

.form-control {
    width: 100%;
    padding: 10px;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    font-size: 16px;
    transition: border-color 0.3s ease;
}

.form-control:focus {
    outline: none;
    border-color: #3498db;
    box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

/* Таблицы */
.table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
}

.table th,
.table td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #ecf0f1;
}

.table th {
    background-color: #f8f9fa;
    font-weight: 600;
    color: #2c3e50;
}

.table tbody tr:hover {
    background-color: #f8f9fa;
}

/* Алерты */
.alert {
    padding: 15px;
    margin-bottom: 20px;
    border-radius: 4px;
    border-left: 4px solid;
}

.alert-success {
    background-color: #d4edda;
    border-color: #27ae60;
    color: #155724;
}

.alert-warning {
    background-color: #fff3cd;
    border-color: #f39c12;
    color: #856404;
}

.alert-danger {
    background-color: #f8d7da;
    border-color: #e74c3c;
    color: #721c24;
}

.alert-info {
    background-color: #d1ecf1;
    border-color: #17a2b8;
    color: #0c5460;
}

/* Утилиты */
.text-center {
    text-align: center;
}

.text-right {
    text-align: right;
}

.mb-0 {
    margin-bottom: 0;
}

.mb-1 {
    margin-bottom: 10px;
}

.mb-2 {
    margin-bottom: 20px;
}

.mb-3 {
    margin-bottom: 30px;
}

.mt-0 {
    margin-top: 0;
}

.mt-1 {
    margin-top: 10px;
}

.mt-2 {
    margin-top: 20px;
}

.mt-3 {
    margin-top: 30px;
}

/* Адаптивность */
@media (max-width: 768px) {
    .container {
        padding: 10px;
    }
    
    .navbar ul {
        flex-direction: column;
        text-align: center;
    }
    
    .navbar li {
        margin: 5px 0;
    }
    
    h1 {
        font-size: 2em;
    }
    
    h2 {
        font-size: 1.5em;
    }
    
    .card {
        padding: 15px;
    }
}

/* Анимации */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in {
    animation: fadeIn 0.5s ease-out;
}

/* Код */
code {
    background-color: #f8f9fa;
    padding: 2px 4px;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
    color: #e74c3c;
}

pre {
    background-color: #2c3e50;
    color: #ecf0f1;
    padding: 20px;
    border-radius: 5px;
    overflow-x: auto;
    margin: 20px 0;
}

pre code {
    background-color: transparent;
    color: inherit;
    padding: 0;
}

```

## demo_project\tests\test_main.py

**Описание:** Python модуль с 12 функциями и 2 классами. Unit test file

**Размер:** 0.01 МБ | **Строки:** 168 | **Хэш:** `0684c49ec770`

```python
"""
Тесты для основного модуля приложения.

Содержит unit-тесты для проверки корректности работы
главного модуля демонстрационного приложения.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import DemoApp


class TestDemoApp(unittest.TestCase):
    """Тесты для класса DemoApp."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.config_file = self.temp_dir / "test_config.json"
        
        # Создание тестовой конфигурации
        self.test_config = {
            "app_name": "Test App",
            "version": "1.0.0",
            "debug": True
        }
        
        import json
        with open(self.config_file, 'w') as f:
            json.dump(self.test_config, f)
    
    def tearDown(self):
        """Очистка тестового окружения."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_app_initialization(self):
        """Тест инициализации приложения."""
        app = DemoApp(str(self.config_file))
        
        self.assertIsNotNone(app.config)
        self.assertIsInstance(app.data, dict)
    
    def test_app_initialization_without_config(self):
        """Тест инициализации приложения без конфигурации."""
        app = DemoApp()
        
        self.assertIsNotNone(app.config)
        self.assertIsInstance(app.data, dict)
    
    @patch('main.DemoApp._load_config')
    @patch('main.DemoApp._initialize_data')
    @patch('main.DemoApp._main_loop')
    def test_run_success(self, mock_main_loop, mock_init_data, mock_load_config):
        """Тест успешного запуска приложения."""
        mock_load_config.return_value = True
        
        app = DemoApp(str(self.config_file))
        result = app.run()
        
        self.assertEqual(result, 0)
        mock_load_config.assert_called_once()
        mock_init_data.assert_called_once()
        mock_main_loop.assert_called_once()
    
    @patch('main.DemoApp._load_config')
    def test_run_config_load_failure(self, mock_load_config):
        """Тест запуска при неудачной загрузке конфигурации."""
        mock_load_config.return_value = False
        
        app = DemoApp(str(self.config_file))
        result = app.run()
        
        self.assertEqual(result, 1)
    
    @patch('main.DemoApp._load_config')
    @patch('main.DemoApp._initialize_data')
    def test_run_keyboard_interrupt(self, mock_init_data, mock_load_config):
        """Тест обработки прерывания клавиатурой."""
        mock_load_config.return_value = True
        mock_init_data.side_effect = KeyboardInterrupt()
        
        app = DemoApp(str(self.config_file))
        result = app.run()
        
        self.assertEqual(result, 1)
    
    @patch('main.DemoApp._load_config')
    @patch('main.DemoApp._initialize_data')
    def test_run_general_exception(self, mock_init_data, mock_load_config):
        """Тест обработки общего исключения."""
        mock_load_config.return_value = True
        mock_init_data.side_effect = Exception("Test error")
        
        app = DemoApp(str(self.config_file))
        result = app.run()
        
        self.assertEqual(result, 1)
    
    def test_initialize_data(self):
        """Тест инициализации данных."""
        app = DemoApp(str(self.config_file))
        app._initialize_data()
        
        self.assertIn('items', app.data)
        self.assertIn('processed_count', app.data)
        self.assertEqual(app.data['items'], [])
        self.assertEqual(app.data['processed_count'], 0)
    
    def test_main_loop(self):
        """Тест основного цикла."""
        app = DemoApp(str(self.config_file))
        app.data = {'items': [], 'processed_count': 0}
        
        app._main_loop()
        
        self.assertEqual(len(app.data['items']), 5)
        self.assertEqual(app.data['processed_count'], 5)
        
        # Проверка структуры элементов
        for i, item in enumerate(app.data['items']):
            self.assertEqual(item['id'], i + 1)
            self.assertEqual(item['name'], f'Item {i + 1}')
            self.assertIn('hash', item)
            self.assertIn('message', item)
    
    def test_get_statistics(self):
        """Тест получения статистики."""
        app = DemoApp(str(self.config_file))
        app.data = {
            'items': [{'id': 1}, {'id': 2}],
            'processed_count': 2,
            'config': {'loaded': True}
        }
        
        stats = app.get_statistics()
        
        self.assertEqual(stats['total_items'], 2)
        self.assertEqual(stats['processed_count'], 2)
        self.assertTrue(stats['config_loaded'])


class TestMainFunction(unittest.TestCase):
    """Тесты для функции main."""
    
    @patch('main.DemoApp')
    def test_main_function(self, mock_demo_app_class):
        """Тест функции main."""
        mock_app = MagicMock()
        mock_app.run.return_value = 0
        mock_demo_app_class.return_value = mock_app
        
        from main import main
        result = main()
        
        self.assertEqual(result, 0)
        mock_demo_app_class.assert_called_once()
        mock_app.run.assert_called_once()


if __name__ == '__main__':
    unittest.main()

```

## demo_project\utils\__init__.py

**Описание:** Вспомогательные модули для демонстрационного приложения.

**Размер:** 0.00 МБ | **Строки:** 4 | **Хэш:** `4cc7b8874642`

```python
"""Вспомогательные модули для демонстрационного приложения."""

__version__ = "1.0.0"
__author__ = "Demo Team"

```

## demo_project\utils\helpers.py

**Описание:** Python модуль с 9 функциями и 1 классами

**Размер:** 0.00 МБ | **Строки:** 153 | **Хэш:** `841a52523979`

```python
"""
Вспомогательные функции для демонстрационного приложения.

Этот модуль содержит утилитарные функции для работы с данными,
форматирования сообщений и вычисления хэшей.
"""

import hashlib
import datetime
from typing import Any, Union


def format_message(text: str, timestamp: bool = True) -> str:
    """Форматирование сообщения с временной меткой.
    
    Args:
        text: Текст сообщения.
        timestamp: Добавлять ли временную метку.
        
    Returns:
        Отформатированное сообщение.
    """
    if timestamp:
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M:%S")
        return f"[{time_str}] {text}"
    return text


def calculate_hash(data: Union[str, bytes]) -> str:
    """Вычисление SHA-256 хэша для данных.
    
    Args:
        data: Данные для хэширования.
        
    Returns:
        SHA-256 хэш в шестнадцатеричном формате.
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    hash_obj = hashlib.sha256()
    hash_obj.update(data)
    return hash_obj.hexdigest()[:12]  # Первые 12 символов


def safe_divide(a: float, b: float, default: float = 0.0) -> float:
    """Безопасное деление с обработкой деления на ноль.
    
    Args:
        a: Делимое.
        b: Делитель.
        default: Значение по умолчанию при делении на ноль.
        
    Returns:
        Результат деления или значение по умолчанию.
    """
    try:
        return a / b if b != 0 else default
    except (TypeError, ZeroDivisionError):
        return default


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Обрезание строки до указанной длины.
    
    Args:
        text: Исходная строка.
        max_length: Максимальная длина.
        suffix: Суффикс для обрезанных строк.
        
    Returns:
        Обрезанная строка.
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def merge_dictionaries(*dicts: dict) -> dict:
    """Объединение нескольких словарей.
    
    Args:
        *dicts: Словари для объединения.
        
    Returns:
        Объединенный словарь.
    """
    result = {}
    for d in dicts:
        if isinstance(d, dict):
            result.update(d)
    return result


class DataProcessor:
    """Класс для обработки данных."""
    
    def __init__(self, batch_size: int = 10):
        """Инициализация процессора.
        
        Args:
            batch_size: Размер пакета для обработки.
        """
        self.batch_size = batch_size
        self.processed_count = 0
    
    def process_item(self, item: Any) -> dict:
        """Обработка одного элемента.
        
        Args:
            item: Элемент для обработки.
            
        Returns:
            Результат обработки.
        """
        self.processed_count += 1
        
        return {
            'original': item,
            'processed_at': datetime.datetime.now().isoformat(),
            'hash': calculate_hash(str(item)),
            'batch_number': (self.processed_count - 1) // self.batch_size + 1
        }
    
    def process_batch(self, items: list) -> list:
        """Обработка пакета элементов.
        
        Args:
            items: Список элементов для обработки.
            
        Returns:
            Список обработанных элементов.
        """
        results = []
        for item in items:
            result = self.process_item(item)
            results.append(result)
        
        return results
    
    def get_statistics(self) -> dict:
        """Получение статистики обработки.
        
        Returns:
            Словарь со статистикой.
        """
        return {
            'processed_count': self.processed_count,
            'batch_size': self.batch_size,
            'total_batches': (self.processed_count - 1) // self.batch_size + 1
        }

```

## demo_project\utils\validators.py

**Описание:** Python модуль с 10 функциями и 1 классами

**Размер:** 0.01 МБ | **Строки:** 248 | **Хэш:** `1e1f189af49d`

```python
"""
Модуль валидации данных для демонстрационного приложения.

Содержит функции для проверки корректности различных типов данных
и конфигурационных параметров.
"""

import re
from typing import Any, Dict, List, Optional, Union


def validate_email(email: str) -> bool:
    """Валидация email адреса.
    
    Args:
        email: Email адрес для проверки.
        
    Returns:
        True если email корректен.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_url(url: str) -> bool:
    """Валидация URL.
    
    Args:
        url: URL для проверки.
        
    Returns:
        True если URL корректен.
    """
    # Поддержка различных схем URL включая sqlite
    pattern = r'^(https?|sqlite)://[^\s]*$'
    return bool(re.match(pattern, url))


def validate_positive_number(value: Union[int, float]) -> bool:
    """Валидация положительного числа.
    
    Args:
        value: Число для проверки.
        
    Returns:
        True если число положительное.
    """
    return isinstance(value, (int, float)) and value > 0


def validate_string_length(text: str, min_length: int = 1, max_length: int = 1000) -> bool:
    """Валидация длины строки.
    
    Args:
        text: Строка для проверки.
        min_length: Минимальная длина.
        max_length: Максимальная длина.
        
    Returns:
        True если длина строки в допустимых пределах.
    """
    return isinstance(text, str) and min_length <= len(text) <= max_length


def validate_config(config: Dict[str, Any]) -> bool:
    """Валидация конфигурации приложения.
    
    Args:
        config: Словарь конфигурации.
        
    Returns:
        True если конфигурация корректна.
    """
    if not isinstance(config, dict):
        return False
    
    # Обязательные поля
    required_fields = ['app_name', 'version', 'debug']
    for field in required_fields:
        if field not in config:
            return False
    
    # Проверка типов
    if not isinstance(config.get('app_name'), str):
        return False
    
    if not isinstance(config.get('version'), str):
        return False
    
    if not isinstance(config.get('debug'), bool):
        return False
    
    # Проверка опциональных полей
    if 'port' in config:
        if not validate_positive_number(config['port']):
            return False
    
    if 'host' in config:
        if not validate_string_length(config['host'], 1, 255):
            return False
    
    if 'database_url' in config:
        if not validate_url(config['database_url']):
            return False
    
    return True


def validate_list_items(items: List[Any], validator_func: callable) -> bool:
    """Валидация элементов списка.
    
    Args:
        items: Список элементов для проверки.
        validator_func: Функция валидации для каждого элемента.
        
    Returns:
        True если все элементы прошли валидацию.
    """
    if not isinstance(items, list):
        return False
    
    for item in items:
        if not validator_func(item):
            return False
    
    return True


class ConfigValidator:
    """Класс для валидации конфигурации."""
    
    def __init__(self, schema: Dict[str, Any]):
        """Инициализация валидатора.
        
        Args:
            schema: Схема валидации.
        """
        self.schema = schema
    
    def validate(self, config: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Валидация конфигурации по схеме.
        
        Args:
            config: Конфигурация для проверки.
            
        Returns:
            Кортеж (успех, список ошибок).
        """
        errors = []
        
        # Проверка обязательных полей
        for field, rules in self.schema.items():
            if rules.get('required', False) and field not in config:
                errors.append(f"Обязательное поле '{field}' отсутствует")
                continue
            
            if field in config:
                value = config[field]
                field_errors = self._validate_field(field, value, rules)
                errors.extend(field_errors)
        
        return len(errors) == 0, errors
    
    def _validate_field(self, field_name: str, value: Any, rules: Dict[str, Any]) -> List[str]:
        """Валидация отдельного поля.
        
        Args:
            field_name: Имя поля.
            value: Значение поля.
            rules: Правила валидации.
            
        Returns:
            Список ошибок валидации.
        """
        errors = []
        
        # Проверка типа
        expected_type = rules.get('type')
        if expected_type and not isinstance(value, expected_type):
            errors.append(f"Поле '{field_name}' должно быть типа {expected_type.__name__}")
            return errors
        
        # Проверка строки
        if expected_type == str:
            min_length = rules.get('min_length', 0)
            max_length = rules.get('max_length', float('inf'))
            
            if not validate_string_length(value, min_length, max_length):
                errors.append(f"Поле '{field_name}' имеет недопустимую длину")
        
        # Проверка числа
        elif expected_type in (int, float):
            min_value = rules.get('min_value', float('-inf'))
            max_value = rules.get('max_value', float('inf'))
            
            if not (min_value <= value <= max_value):
                errors.append(f"Поле '{field_name}' вне допустимого диапазона")
        
        # Проверка списка
        elif expected_type == list:
            item_validator = rules.get('item_validator')
            if item_validator and not validate_list_items(value, item_validator):
                errors.append(f"Поле '{field_name}' содержит недопустимые элементы")
        
        return errors


def create_default_schema() -> Dict[str, Any]:
    """Создание схемы валидации по умолчанию.
    
    Returns:
        Схема валидации.
    """
    return {
        'app_name': {
            'type': str,
            'required': True,
            'min_length': 1,
            'max_length': 100
        },
        'version': {
            'type': str,
            'required': True,
            'min_length': 1,
            'max_length': 20
        },
        'debug': {
            'type': bool,
            'required': True
        },
        'port': {
            'type': int,
            'required': False,
            'min_value': 1,
            'max_value': 65535
        },
        'host': {
            'type': str,
            'required': False,
            'min_length': 1,
            'max_length': 255
        },
        'database_url': {
            'type': str,
            'required': False,
            'min_length': 1
        }
    }

```

## pyproject.toml

**Описание:** pyproject_file

**Размер:** 0.00 МБ | **Строки:** 81 | **Хэш:** `1b5ed6096a39`

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
include = ["app*"]
exclude = ["tests*", "demo_project*", "release*", "build*", "dist*"]

[project]
name = "code-to-markdown"
version = "1.2.0"
description = "Desktop GUI tool to convert project source code to Markdown"
authors = [{name = "Code to Markdown Team"}]
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "PySide6>=6.5.0",
    "pathspec>=0.11.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-qt>=4.2.0",
    "ruff>=0.1.0",
    "black>=23.0.0",
    "mypy>=1.0.0",
    "PyInstaller>=5.0.0",
]

[tool.ruff]
target-version = "py311"
line-length = 88
select = ["E", "F", "W", "C90", "I", "N", "UP", "YTT", "S", "BLE", "FBT", "B", "A", "COM", "C4", "DTZ", "T10", "EM", "EXE", "FA", "ISC", "ICN", "G", "INP", "PIE", "T20", "PYI", "PT", "Q", "RSE", "RET", "SLF", "SLOT", "SIM", "TID", "TCH", "INT", "ARG", "PTH", "TD", "FIX", "ERA", "PD", "PGH", "PL", "TRY", "FLY", "NPY", "AIR", "PERF", "FURB", "LOG", "RUF"]
ignore = ["E501", "S101", "S104", "S108", "S110", "S112", "S311", "S701"]

[tool.ruff.per-file-ignores]
"tests/*" = ["S101", "S106", "S108"]

[tool.black]
target-version = ['py311']
line-length = 88
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | venv
  | _build
  | buck-out
  | build
  | dist
)/
'''

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"

```

## README.md

**Описание:** Markdown файл

**Размер:** 0.01 МБ | **Строки:** 348 | **Хэш:** `72fd3a3252c6`

```markdown
# Code to Markdown

Настольное GUI-приложение для конвертации исходного кода проекта в единый Markdown-файл с аккуратными комментариями и оглавлением.

## 🚀 Версия 1.2.0 - Оптимизация производительности

**Новые возможности:**
- ⚡ **Автоматическая оптимизация** - умная фильтрация файлов для больших проектов
- 📊 **Улучшенная статистика** - отображение "Найдено/Показано/Выбрано" файлов
- 🎯 **Быстрая работа** - в 6-10 раз быстрее с проектами >1000 файлов
- 🔧 **Незаметная оптимизация** - работает автоматически без настроек

**Исправления:**
- Решена проблема зависания на больших проектах (5000+ файлов)
- Улучшена отзывчивость интерфейса
- Оптимизировано создание дерева файлов

## Возможности

- 🗂️ **Выбор папки проекта** - интуитивный выбор папки с исходным кодом
- 📝 **Автоматические аннотации** - умная генерация описаний файлов на основе AST-анализа и эвристик
- 🔍 **Предпросмотр** - быстрый предпросмотр результата перед генерацией
- 📊 **Подробная статистика** - информация о типах файлов, размерах и метаданных
- 🚫 **Умная фильтрация** - поддержка .gitignore и исключение бинарных файлов
- 🌐 **Локализация** - интерфейс на русском языке с возможностью расширения
- ⚡ **Производительность** - потоковая обработка больших проектов

## Технологический стек

- **Python 3.11+** - основной язык программирования
- **PySide6** - современный GUI фреймворк на основе Qt
- **PyInstaller** - сборка в исполняемый .exe файл
- **pathspec** - поддержка .gitignore файлов
- **ruff + black** - линтинг и форматирование кода
- **pytest** - тестирование

## Установка и запуск

### Для разработчиков

1. **Клонирование репозитория**
   ```bash
   git clone <repository-url>
   cd code-to-md
   ```

2. **Создание виртуального окружения**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Установка зависимостей**
   ```bash
   pip install -e .
   pip install -e ".[dev]"
   ```

4. **Запуск приложения**
   ```bash
   python -m app.main
   ```

### Для пользователей

1. **Скачайте готовый .exe файл** из раздела Releases
2. **Запустите CodeToMarkdown.exe**
3. **Выберите папку с проектом** и настройте параметры
4. **Нажмите "Создать Markdown"** для генерации файла

## Сборка исполняемого файла

### Требования

- Python 3.11+
- PyInstaller
- Все зависимости проекта

### Команда сборки

```bash
pyinstaller app/main.py --name CodeToMarkdown --onefile --noconsole --add-data "app/i18n.json;app"
```

### Альтернативная сборка с иконкой

```bash
pyinstaller app/main.py --name CodeToMarkdown --onefile --noconsole --icon=app/icon.ico --add-data "app/i18n.json;app"
```

## Использование

### Основной рабочий процесс

1. **Запустите приложение**
2. **Выберите папку проекта** с помощью кнопки "Выбрать папку"
3. **Настройте параметры:**
   - ☑️ Учитывать .gitignore
   - ☑️ Включать большие файлы (>5 МБ)
   - ☑️ Включать конфиги/разметку
4. **Просмотрите предпросмотр** (опционально)
5. **Нажмите "Создать Markdown"**
6. **Выберите место сохранения** файла
7. **Дождитесь завершения** генерации

### Поддерживаемые типы файлов

#### Код
- Python (.py)
- JavaScript (.js, .jsx)
- TypeScript (.ts, .tsx)
- Java (.java)
- C/C++ (.c, .cpp, .h, .hpp)
- Go (.go)
- Rust (.rs)
- PHP (.php)
- Ruby (.rb)
- Swift (.swift)
- Kotlin (.kt)
- C# (.cs)

#### Скрипты
- Shell (.sh)
- PowerShell (.ps1)
- Batch (.bat, .cmd)

#### Конфигурация и разметка
- JSON (.json)
- YAML (.yaml, .yml)
- TOML (.toml)
- INI (.ini)
- Environment (.env)
- Markdown (.md)
- Text (.txt)
- Config (.cfg)

#### Веб
- HTML (.html)
- CSS (.css, .scss, .sass)
- Less (.less)

### Исключаемые папки

По умолчанию исключаются следующие папки:
- `.git`, `.hg`, `.svn` - системы контроля версий
- `__pycache__`, `.mypy_cache`, `.pytest_cache` - кэши Python
- `node_modules`, `dist`, `build`, `out` - артефакты сборки
- `.venv`, `venv` - виртуальные окружения
- `.idea`, `.vscode` - настройки IDE

## Структура проекта

```
code-to-markdown/
├── app/                      # Основной пакет приложения
│   ├── __init__.py
│   ├── main.py              # Точка входа
│   ├── ui.py                # GUI интерфейс
│   ├── worker.py            # Фоновые задачи
│   ├── md_builder.py        # Генератор Markdown
│   ├── file_discovery.py    # Поиск и фильтрация файлов
│   ├── annotations.py       # Генерация аннотаций
│   ├── preview.py           # Предпросмотр
│   ├── config.py            # Управление конфигурацией
│   ├── i18n.py              # Локализация
│   └── logging_setup.py     # Настройка логирования
├── tests/                   # Тесты
│   ├── test_file_discovery.py
│   ├── test_annotations.py
│   └── test_md_builder.py
├── demo_project/            # Демонстрационный проект
│   ├── main.py
│   ├── utils/
│   ├── config/
│   ├── tests/
│   └── static/
├── pyproject.toml           # Конфигурация проекта
└── README.md               # Документация
```

## Конфигурация

### Файл конфигурации

Приложение сохраняет настройки в `%APPDATA%/CodeToMarkdown/config.json`:

```json
{
  "last_project_path": "C:\\Projects\\MyProject",
  "include_gitignore": true,
  "include_large_files": false,
  "include_config_files": true,
  "max_file_size_mb": 5,
  "window_geometry": "...",
  "splitter_state": "..."
}
```

### Переменные окружения

- `DEMO_DEBUG=true` - включить режим отладки
- `LOG_LEVEL=INFO` - уровень логирования

## Логирование

Логи сохраняются в:
- **Windows**: `%USERPROFILE%/CodeToMarkdown/logs/app.log`
- **Linux/macOS**: `~/.local/share/CodeToMarkdown/logs/app.log`

Настройки логирования:
- Ротация файлов (1 МБ × 3 файла)
- Уровни: INFO, WARNING, ERROR
- Кодировка: UTF-8

## Тестирование

### Запуск тестов

```bash
# Все тесты
pytest

# Конкретный модуль
pytest tests/test_file_discovery.py

# С покрытием
pytest --cov=app

# С подробным выводом
pytest -v
```

### Тестовые сценарии

1. **Базовый путь**: выбор папки → предпросмотр → создание Markdown
2. **.gitignore**: проверка исключения файлов согласно .gitignore
3. **Большие файлы**: обработка файлов >5 МБ
4. **Кодировки**: чтение файлов в UTF-8 и Latin-1
5. **AST-анализ**: генерация аннотаций для Python файлов

## Разработка

### Установка зависимостей для разработки

```bash
pip install -e ".[dev]"
```

### Линтинг и форматирование

```bash
# Ruff (быстрый линтер)
ruff check app/ tests/

# Black (форматирование)
black app/ tests/

# MyPy (проверка типов)
mypy app/
```

### Структура кода

- **Модульность**: каждый компонент в отдельном файле
- **Типизация**: использование type hints
- **Документация**: docstrings для всех публичных функций
- **Обработка ошибок**: graceful handling с логированием

## Производительность

### Рекомендации

- **Малые проекты** (<100 файлов): мгновенная обработка
- **Средние проекты** (100-1000 файлов): <10 секунд
- **Большие проекты** (1000+ файлов): <30 секунд

### Оптимизации

- Потоковое чтение файлов
- Ленивая загрузка контента
- Кэширование результатов
- Параллельная обработка

## Устранение неполадок

### Частые проблемы

1. **Приложение не запускается**
   - Проверьте версию Python (требуется 3.11+)
   - Установите зависимости: `pip install -e .`

2. **Ошибки чтения файлов**
   - Проверьте права доступа к папке
   - Убедитесь, что файлы не заблокированы

3. **Медленная обработка**
   - Отключите "Включать большие файлы"
   - Проверьте .gitignore на исключение ненужных папок

4. **Проблемы с кодировкой**
   - Файлы автоматически читаются в UTF-8, затем Latin-1
   - Проверьте логи для деталей ошибок

### Логи и отладка

```bash
# Просмотр логов
tail -f ~/.local/share/CodeToMarkdown/logs/app.log

# Запуск с отладкой
DEMO_DEBUG=true python -m app.main
```

## Лицензия

MIT License - см. файл LICENSE для деталей.

## Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения с тестами
4. Запустите линтеры и тесты
5. Создайте Pull Request

## Поддержка

- **Issues**: GitHub Issues для багов и предложений
- **Discussions**: GitHub Discussions для вопросов
- **Email**: [ваш-email@example.com]

## Changelog

### v1.0.0 (2024-01-XX)
- Первый релиз
- Поддержка основных языков программирования
- GUI интерфейс на PySide6
- Автоматическая генерация аннотаций
- Поддержка .gitignore
- Предпросмотр результата
- Локализация на русском языке

---

**Code to Markdown** - превратите ваш код в красивую документацию! 📚✨

```

## release\CHANGELOG.md

**Описание:** Markdown файл

**Размер:** 0.00 МБ | **Строки:** 29 | **Хэш:** `e007ee8e5c07`

```markdown
# Changelog

## [1.2.0] - 2025-09-17

### Добавлено
- ⚡ Автоматическая оптимизация для больших проектов (>1000 файлов)
- 📊 Улучшенная статистика: "Найдено/Показано/Выбрано" файлов
- 🎯 Умная фильтрация файлов по умолчанию
- 🔧 Незаметная оптимизация без настроек

### Исправлено
- Решена проблема зависания на больших проектах (5000+ файлов)
- Улучшена отзывчивость интерфейса
- Оптимизировано создание дерева файлов
- Исправлены проблемы с производительностью

### Технические улучшения
- Интегрирован алгоритм оптимизации в оригинальную версию
- Добавлено отслеживание статистики файлов
- Улучшена логика принятия решений для разных размеров проектов

## [1.1.0] - 2024-09-16

### Добавлено
- Базовая функциональность приложения
- GUI интерфейс на PySide6
- Поддержка .gitignore
- Автоматические аннотации файлов
- Локализация на русском языке

```

## release\README.md

**Описание:** Markdown файл

**Размер:** 0.01 МБ | **Строки:** 348 | **Хэш:** `72fd3a3252c6`

```markdown
# Code to Markdown

Настольное GUI-приложение для конвертации исходного кода проекта в единый Markdown-файл с аккуратными комментариями и оглавлением.

## 🚀 Версия 1.2.0 - Оптимизация производительности

**Новые возможности:**
- ⚡ **Автоматическая оптимизация** - умная фильтрация файлов для больших проектов
- 📊 **Улучшенная статистика** - отображение "Найдено/Показано/Выбрано" файлов
- 🎯 **Быстрая работа** - в 6-10 раз быстрее с проектами >1000 файлов
- 🔧 **Незаметная оптимизация** - работает автоматически без настроек

**Исправления:**
- Решена проблема зависания на больших проектах (5000+ файлов)
- Улучшена отзывчивость интерфейса
- Оптимизировано создание дерева файлов

## Возможности

- 🗂️ **Выбор папки проекта** - интуитивный выбор папки с исходным кодом
- 📝 **Автоматические аннотации** - умная генерация описаний файлов на основе AST-анализа и эвристик
- 🔍 **Предпросмотр** - быстрый предпросмотр результата перед генерацией
- 📊 **Подробная статистика** - информация о типах файлов, размерах и метаданных
- 🚫 **Умная фильтрация** - поддержка .gitignore и исключение бинарных файлов
- 🌐 **Локализация** - интерфейс на русском языке с возможностью расширения
- ⚡ **Производительность** - потоковая обработка больших проектов

## Технологический стек

- **Python 3.11+** - основной язык программирования
- **PySide6** - современный GUI фреймворк на основе Qt
- **PyInstaller** - сборка в исполняемый .exe файл
- **pathspec** - поддержка .gitignore файлов
- **ruff + black** - линтинг и форматирование кода
- **pytest** - тестирование

## Установка и запуск

### Для разработчиков

1. **Клонирование репозитория**
   ```bash
   git clone <repository-url>
   cd code-to-md
   ```

2. **Создание виртуального окружения**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Установка зависимостей**
   ```bash
   pip install -e .
   pip install -e ".[dev]"
   ```

4. **Запуск приложения**
   ```bash
   python -m app.main
   ```

### Для пользователей

1. **Скачайте готовый .exe файл** из раздела Releases
2. **Запустите CodeToMarkdown.exe**
3. **Выберите папку с проектом** и настройте параметры
4. **Нажмите "Создать Markdown"** для генерации файла

## Сборка исполняемого файла

### Требования

- Python 3.11+
- PyInstaller
- Все зависимости проекта

### Команда сборки

```bash
pyinstaller app/main.py --name CodeToMarkdown --onefile --noconsole --add-data "app/i18n.json;app"
```

### Альтернативная сборка с иконкой

```bash
pyinstaller app/main.py --name CodeToMarkdown --onefile --noconsole --icon=app/icon.ico --add-data "app/i18n.json;app"
```

## Использование

### Основной рабочий процесс

1. **Запустите приложение**
2. **Выберите папку проекта** с помощью кнопки "Выбрать папку"
3. **Настройте параметры:**
   - ☑️ Учитывать .gitignore
   - ☑️ Включать большие файлы (>5 МБ)
   - ☑️ Включать конфиги/разметку
4. **Просмотрите предпросмотр** (опционально)
5. **Нажмите "Создать Markdown"**
6. **Выберите место сохранения** файла
7. **Дождитесь завершения** генерации

### Поддерживаемые типы файлов

#### Код
- Python (.py)
- JavaScript (.js, .jsx)
- TypeScript (.ts, .tsx)
- Java (.java)
- C/C++ (.c, .cpp, .h, .hpp)
- Go (.go)
- Rust (.rs)
- PHP (.php)
- Ruby (.rb)
- Swift (.swift)
- Kotlin (.kt)
- C# (.cs)

#### Скрипты
- Shell (.sh)
- PowerShell (.ps1)
- Batch (.bat, .cmd)

#### Конфигурация и разметка
- JSON (.json)
- YAML (.yaml, .yml)
- TOML (.toml)
- INI (.ini)
- Environment (.env)
- Markdown (.md)
- Text (.txt)
- Config (.cfg)

#### Веб
- HTML (.html)
- CSS (.css, .scss, .sass)
- Less (.less)

### Исключаемые папки

По умолчанию исключаются следующие папки:
- `.git`, `.hg`, `.svn` - системы контроля версий
- `__pycache__`, `.mypy_cache`, `.pytest_cache` - кэши Python
- `node_modules`, `dist`, `build`, `out` - артефакты сборки
- `.venv`, `venv` - виртуальные окружения
- `.idea`, `.vscode` - настройки IDE

## Структура проекта

```
code-to-markdown/
├── app/                      # Основной пакет приложения
│   ├── __init__.py
│   ├── main.py              # Точка входа
│   ├── ui.py                # GUI интерфейс
│   ├── worker.py            # Фоновые задачи
│   ├── md_builder.py        # Генератор Markdown
│   ├── file_discovery.py    # Поиск и фильтрация файлов
│   ├── annotations.py       # Генерация аннотаций
│   ├── preview.py           # Предпросмотр
│   ├── config.py            # Управление конфигурацией
│   ├── i18n.py              # Локализация
│   └── logging_setup.py     # Настройка логирования
├── tests/                   # Тесты
│   ├── test_file_discovery.py
│   ├── test_annotations.py
│   └── test_md_builder.py
├── demo_project/            # Демонстрационный проект
│   ├── main.py
│   ├── utils/
│   ├── config/
│   ├── tests/
│   └── static/
├── pyproject.toml           # Конфигурация проекта
└── README.md               # Документация
```

## Конфигурация

### Файл конфигурации

Приложение сохраняет настройки в `%APPDATA%/CodeToMarkdown/config.json`:

```json
{
  "last_project_path": "C:\\Projects\\MyProject",
  "include_gitignore": true,
  "include_large_files": false,
  "include_config_files": true,
  "max_file_size_mb": 5,
  "window_geometry": "...",
  "splitter_state": "..."
}
```

### Переменные окружения

- `DEMO_DEBUG=true` - включить режим отладки
- `LOG_LEVEL=INFO` - уровень логирования

## Логирование

Логи сохраняются в:
- **Windows**: `%USERPROFILE%/CodeToMarkdown/logs/app.log`
- **Linux/macOS**: `~/.local/share/CodeToMarkdown/logs/app.log`

Настройки логирования:
- Ротация файлов (1 МБ × 3 файла)
- Уровни: INFO, WARNING, ERROR
- Кодировка: UTF-8

## Тестирование

### Запуск тестов

```bash
# Все тесты
pytest

# Конкретный модуль
pytest tests/test_file_discovery.py

# С покрытием
pytest --cov=app

# С подробным выводом
pytest -v
```

### Тестовые сценарии

1. **Базовый путь**: выбор папки → предпросмотр → создание Markdown
2. **.gitignore**: проверка исключения файлов согласно .gitignore
3. **Большие файлы**: обработка файлов >5 МБ
4. **Кодировки**: чтение файлов в UTF-8 и Latin-1
5. **AST-анализ**: генерация аннотаций для Python файлов

## Разработка

### Установка зависимостей для разработки

```bash
pip install -e ".[dev]"
```

### Линтинг и форматирование

```bash
# Ruff (быстрый линтер)
ruff check app/ tests/

# Black (форматирование)
black app/ tests/

# MyPy (проверка типов)
mypy app/
```

### Структура кода

- **Модульность**: каждый компонент в отдельном файле
- **Типизация**: использование type hints
- **Документация**: docstrings для всех публичных функций
- **Обработка ошибок**: graceful handling с логированием

## Производительность

### Рекомендации

- **Малые проекты** (<100 файлов): мгновенная обработка
- **Средние проекты** (100-1000 файлов): <10 секунд
- **Большие проекты** (1000+ файлов): <30 секунд

### Оптимизации

- Потоковое чтение файлов
- Ленивая загрузка контента
- Кэширование результатов
- Параллельная обработка

## Устранение неполадок

### Частые проблемы

1. **Приложение не запускается**
   - Проверьте версию Python (требуется 3.11+)
   - Установите зависимости: `pip install -e .`

2. **Ошибки чтения файлов**
   - Проверьте права доступа к папке
   - Убедитесь, что файлы не заблокированы

3. **Медленная обработка**
   - Отключите "Включать большие файлы"
   - Проверьте .gitignore на исключение ненужных папок

4. **Проблемы с кодировкой**
   - Файлы автоматически читаются в UTF-8, затем Latin-1
   - Проверьте логи для деталей ошибок

### Логи и отладка

```bash
# Просмотр логов
tail -f ~/.local/share/CodeToMarkdown/logs/app.log

# Запуск с отладкой
DEMO_DEBUG=true python -m app.main
```

## Лицензия

MIT License - см. файл LICENSE для деталей.

## Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения с тестами
4. Запустите линтеры и тесты
5. Создайте Pull Request

## Поддержка

- **Issues**: GitHub Issues для багов и предложений
- **Discussions**: GitHub Discussions для вопросов
- **Email**: [ваш-email@example.com]

## Changelog

### v1.0.0 (2024-01-XX)
- Первый релиз
- Поддержка основных языков программирования
- GUI интерфейс на PySide6
- Автоматическая генерация аннотаций
- Поддержка .gitignore
- Предпросмотр результата
- Локализация на русском языке

---

**Code to Markdown** - превратите ваш код в красивую документацию! 📚✨

```

## release_v1.1.0\CHANGELOG.md

**Описание:** Markdown файл

**Размер:** 0.00 МБ | **Строки:** 53 | **Хэш:** `47d821efa4a6`

```markdown
# Changelog

Все важные изменения в проекте будут документированы в этом файле.

## [1.1.0] - 2024-09-12

### Добавлено
- Модуль утилит (`app/utils.py`) с общими функциями
- Улучшенная обработка пустых проектов
- Более эффективная проверка бинарных файлов
- Оптимизированная работа с кодировками файлов

### Изменено
- **ПРОИЗВОДИТЕЛЬНОСТЬ**: Улучшена производительность поиска файлов
- **ПРОИЗВОДИТЕЛЬНОСТЬ**: Оптимизирована обработка больших файлов
- **ПРОИЗВОДИТЕЛЬНОСТЬ**: Ускорена генерация статистики
- **КОД**: Устранено дублирование кода (DRY принцип)
- **КОД**: Улучшена читаемость и поддерживаемость
- **КОД**: Удалены неиспользуемые импорты и функции

### Исправлено
- Исправлена обработка исключенных директорий
- Улучшена совместимость с различными кодировками файлов
- Исправлены тесты для работы с локализацией

### Технические улучшения
- Создан модуль `app/utils.py` с переиспользуемыми функциями:
  - `open_file_explorer()` - универсальное открытие папок
  - `read_file_safe()` - безопасное чтение файлов с fallback кодировок
  - `get_file_size_mb()` - получение размера файла в МБ
  - `is_binary_file()` - проверка бинарных файлов
  - `clean_filename_for_anchor()` - очистка имен файлов для якорей
- Удалены дублирующиеся методы из различных модулей
- Упрощены сложные конструкции и улучшена читаемость
- Оптимизированы алгоритмы сортировки и подсчета

## [1.0.1] - 2024-09-11

### Изменено
- Удален предпросмотр из релиза для уменьшения размера

## [1.0.0] - 2024-09-10

### Добавлено
- Первоначальный релиз
- Графический интерфейс на PySide6
- Поддержка множества языков программирования
- Автоматическое определение типов файлов
- Генерация умных аннотаций
- Поддержка .gitignore
- Предпросмотр результатов
- Статистика проекта
- Конфигурация через GUI

```

## release_v1.1.0\INSTALL.txt

**Описание:** Неизвестный тип файла

**Размер:** 0.00 МБ | **Строки:** 41 | **Хэш:** `e4220a3aee34`

```text
Code to Markdown v1.1.0 - Установка и запуск
==============================================

БЫСТРЫЙ СТАРТ:
1. Скачайте CodeToMarkdown.exe
2. Поместите в любую папку
3. Запустите двойным кликом

СИСТЕМНЫЕ ТРЕБОВАНИЯ:
- Windows 10/11 (64-bit)
- 4 ГБ RAM (рекомендуется 8 ГБ)
- 50 МБ свободного места

ОСОБЕННОСТИ v1.1.0:
- Улучшена производительность
- Оптимизирован код
- Устранено дублирование
- Добавлены утилиты

ПОДДЕРЖИВАЕМЫЕ ФАЙЛЫ:
- Python, JavaScript, TypeScript
- Java, C/C++, C#, Go, Rust
- PHP, Ruby, Swift, Kotlin
- JSON, YAML, TOML, INI
- HTML, CSS, Markdown
- И многие другие...

ИСКЛЮЧАЕМЫЕ ПАПКИ:
- .git, node_modules, __pycache__
- dist, build, .venv, .idea

ПРОБЛЕМЫ?
- Убедитесь в Windows 10/11 (64-bit)
- Проверьте антивирус
- Запустите от имени администратора

ВЕРСИЯ: 1.1.0
РАЗМЕР: ~43 МБ
АРХИТЕКТУРА: x64

Copyright (C) 2024 Code to Markdown Team

```

## release_v1.1.0\README.md

**Описание:** Markdown файл

**Размер:** 0.01 МБ | **Строки:** 136 | **Хэш:** `82f90620abb7`

```markdown
# Code to Markdown v1.1.0

## Описание

**Code to Markdown** - это настольное приложение с графическим интерфейсом для конвертации исходного кода проекта в Markdown документ.

## Новые возможности v1.1.0

### 🚀 Оптимизация производительности
- Улучшена производительность поиска файлов
- Оптимизирована обработка больших файлов
- Ускорена генерация статистики

### 🔧 Улучшения кода
- Устранено дублирование кода (DRY принцип)
- Создан модуль утилит для переиспользуемых функций
- Улучшена читаемость и поддерживаемость кода
- Удалены неиспользуемые импорты и функции

### 🎯 Новые функции
- Улучшенная обработка пустых проектов
- Более эффективная проверка бинарных файлов
- Оптимизированная работа с кодировками файлов

## Системные требования

- **Операционная система:** Windows 10/11 (64-bit)
- **Память:** 4 ГБ RAM (рекомендуется 8 ГБ)
- **Место на диске:** 50 МБ для установки
- **Дополнительно:** Не требует установки Python

## Установка

1. Скачайте `CodeToMarkdown.exe`
2. Поместите файл в любую папку
3. Запустите двойным кликом

## Использование

1. **Запустите приложение** - дважды кликните на `CodeToMarkdown.exe`
2. **Выберите папку проекта** - нажмите "Выбрать папку"
3. **Настройте параметры** (опционально):
   - Учитывать .gitignore
   - Включать большие файлы (>5 МБ)
   - Включать конфиги/разметку
4. **Выберите файлы** - отметьте нужные файлы в списке
5. **Создайте Markdown** - нажмите "Создать Markdown"
6. **Сохраните файл** - выберите место для сохранения

## Поддерживаемые форматы

### Языки программирования
- Python (.py)
- JavaScript (.js, .jsx)
- TypeScript (.ts, .tsx)
- Java (.java)
- C/C++ (.c, .cpp, .h, .hpp)
- C# (.cs)
- Go (.go)
- Rust (.rs)
- PHP (.php)
- Ruby (.rb)
- Swift (.swift)
- Kotlin (.kt)
- И многие другие...

### Конфигурация и разметка
- JSON (.json)
- YAML (.yaml, .yml)
- TOML (.toml)
- INI (.ini)
- Environment (.env)
- Markdown (.md)
- Text (.txt)
- Config (.cfg)

### Веб
- HTML (.html)
- CSS (.css, .scss, .sass)
- Less (.less)

## Исключаемые папки

По умолчанию исключаются следующие папки:
- `.git`, `.hg`, `.svn` - системы контроля версий
- `__pycache__`, `.mypy_cache`, `.pytest_cache` - кэши Python
- `node_modules`, `dist`, `build`, `out` - артефакты сборки
- `.venv`, `venv` - виртуальные окружения
- `.idea`, `.vscode` - настройки IDE

## Особенности

- **Автоматическое определение типов файлов** - приложение само определяет язык программирования
- **Умные аннотации** - генерирует описания файлов на основе их содержимого
- **Поддержка .gitignore** - автоматически исключает файлы из .gitignore
- **Предпросмотр** - возможность просмотреть результат перед сохранением
- **Статистика проекта** - подробная информация о файлах и их размерах
- **Кроссплатформенность** - работает на Windows, Linux, macOS

## Устранение неполадок

### Приложение не запускается
- Убедитесь, что у вас Windows 10/11 (64-bit)
- Проверьте, что файл не заблокирован антивирусом
- Запустите от имени администратора

### Ошибки при обработке файлов
- Проверьте права доступа к папке проекта
- Убедитесь, что файлы не используются другими программами
- Попробуйте уменьшить размер файлов в настройках

### Медленная работа
- Закройте другие приложения
- Увеличьте лимит размера файлов
- Исключите большие папки через .gitignore

## Техническая информация

- **Версия:** 1.1.0
- **Размер:** ~43 МБ
- **Архитектура:** x64
- **Python:** 3.12.3
- **GUI:** PySide6 (Qt6)
- **Сборка:** PyInstaller

## Лицензия

Copyright (C) 2024 Code to Markdown Team

## Поддержка

Если у вас возникли проблемы или есть предложения, создайте issue в репозитории проекта.

---

**Code to Markdown v1.1.0** - Быстрая и удобная конвертация кода в документацию!

```

## run.py

**Описание:** Executable script

**Размер:** 0.00 МБ | **Строки:** 18 | **Хэш:** `874895e80ab4`

```python
#!/usr/bin/env python3
"""
Скрипт запуска приложения Code to Markdown.

Этот файл служит точкой входа для запуска приложения
как из командной строки, так и при разработке.
"""

import sys
from pathlib import Path

# Добавляем корневую папку в путь для импорта модулей
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

if __name__ == "__main__":
    from app.main import main
    sys.exit(main())

```

## tests\__init__.py

**Описание:** Test package for Code to Markdown.

**Размер:** 0.00 МБ | **Строки:** 1 | **Хэш:** `d54f7836e414`

```python
"""Test package for Code to Markdown."""

```

## tests\test_annotations.py

**Описание:** Tests for annotations module.

**Размер:** 0.01 МБ | **Строки:** 259 | **Хэш:** `ebeb3e861860`

```python
"""Tests for annotations module."""

import tempfile
import shutil
from pathlib import Path
import pytest

from app.annotations import FileAnnotator


class TestFileAnnotator:
    """Test cases for FileAnnotator class."""
    
    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.annotator = FileAnnotator()
    
    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_python_docstring_extraction(self):
        """Test Python docstring extraction."""
        # Create Python file with docstring
        py_file = self.temp_dir / "test.py"
        content = '''"""
This is a test module for demonstration purposes.
It contains sample functions and classes.
"""

def hello():
    """Print hello message."""
    print("Hello, world!")

class TestClass:
    """A test class for demonstration."""
    pass
'''
        py_file.write_text(content)
        
        # Generate annotation
        annotation = self.annotator.generate_annotation(py_file)
        
        # Should extract docstring or have Python module info
        annotation_lower = annotation.lower()
        assert ("test module" in annotation_lower or "модуль" in annotation_lower or "python" in annotation_lower)
        assert ("demonstration" in annotation_lower or "демонстрации" in annotation_lower or "функци" in annotation_lower)
    
    def test_python_ast_analysis(self):
        """Test Python AST analysis."""
        # Create Python file with functions and classes
        py_file = self.temp_dir / "test.py"
        content = '''
def function1():
    pass

def function2():
    pass

class Class1:
    pass

class Class2:
    pass
'''
        py_file.write_text(content)
        
        # Generate annotation
        annotation = self.annotator.generate_annotation(py_file)
        
        # Should include function and class counts (check for both languages)
        annotation_lower = annotation.lower()
        assert ("2 функция" in annotation_lower or "2 functions" in annotation_lower)
        assert ("2 класс" in annotation_lower or "2 classes" in annotation_lower)
    
    def test_heuristic_analysis(self):
        """Test heuristic analysis."""
        # Test setup.py
        setup_file = self.temp_dir / "setup.py"
        setup_file.write_text("from setuptools import setup")
        annotation = self.annotator.generate_annotation(setup_file)
        annotation_lower = annotation.lower()
        assert ("setup" in annotation_lower or "настройка" in annotation_lower)
        
        # Test requirements.txt
        req_file = self.temp_dir / "requirements.txt"
        req_file.write_text("requests==2.25.1")
        annotation = self.annotator.generate_annotation(req_file)
        annotation_lower = annotation.lower()
        assert ("requirements" in annotation_lower or "требования" in annotation_lower)
        
        # Test test file
        test_file = self.temp_dir / "test_example.py"
        test_file.write_text("def test_something(): pass")
        annotation = self.annotator.generate_annotation(test_file)
        annotation_lower = annotation.lower()
        assert ("test" in annotation_lower or "тест" in annotation_lower or "python" in annotation_lower)
    
    def test_javascript_file(self):
        """Test JavaScript file annotation."""
        js_file = self.temp_dir / "app.js"
        content = '''
// This is a JavaScript application
// It handles user interactions

function greetUser(name) {
    console.log("Hello, " + name);
}

const config = {
    apiUrl: "https://api.example.com"
};
'''
        js_file.write_text(content)
        
        # Generate annotation
        annotation = self.annotator.generate_annotation(js_file)
        
        # Should detect JavaScript
        assert "javascript" in annotation.lower() or "js" in annotation.lower()
    
    def test_config_file_annotation(self):
        """Test config file annotation."""
        # JSON config
        json_file = self.temp_dir / "config.json"
        json_file.write_text('{"database": "sqlite"}')
        annotation = self.annotator.generate_annotation(json_file)
        annotation_lower = annotation.lower()
        assert ("config" in annotation_lower or "конфигурации" in annotation_lower)
        
        # YAML config
        yaml_file = self.temp_dir / "config.yaml"
        yaml_file.write_text("database: sqlite")
        annotation = self.annotator.generate_annotation(yaml_file)
        annotation_lower = annotation.lower()
        assert ("config" in annotation_lower or "конфигурации" in annotation_lower)
    
    def test_html_file_annotation(self):
        """Test HTML file annotation."""
        html_file = self.temp_dir / "index.html"
        content = '''
<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <h1>Hello World</h1>
</body>
</html>
'''
        html_file.write_text(content)
        
        # Generate annotation
        annotation = self.annotator.generate_annotation(html_file)
        
        # Should detect HTML
        assert "html" in annotation.lower() or "markup" in annotation.lower()
    
    def test_css_file_annotation(self):
        """Test CSS file annotation."""
        css_file = self.temp_dir / "style.css"
        content = '''
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
}

.header {
    background-color: #333;
    color: white;
}
'''
        css_file.write_text(content)
        
        # Generate annotation
        annotation = self.annotator.generate_annotation(css_file)
        
        # Should detect CSS
        assert "css" in annotation.lower() or "style" in annotation.lower()
    
    def test_unknown_file_type(self):
        """Test unknown file type handling."""
        unknown_file = self.temp_dir / "unknown.xyz"
        unknown_file.write_text("some content")
        
        # Generate annotation
        annotation = self.annotator.generate_annotation(unknown_file)
        
        # Should return fallback
        assert annotation is not None
        assert len(annotation) > 0
    
    def test_empty_file(self):
        """Test empty file handling."""
        empty_file = self.temp_dir / "empty.txt"
        empty_file.write_text("")
        
        # Generate annotation
        annotation = self.annotator.generate_annotation(empty_file)
        
        # Should handle empty file gracefully
        assert annotation is not None
    
    def test_encoding_error_handling(self):
        """Test encoding error handling."""
        # Create file with invalid UTF-8
        invalid_file = self.temp_dir / "invalid.txt"
        invalid_file.write_bytes(b'\xff\xfe\x00\x00')  # Invalid UTF-8
        
        # Should handle encoding error gracefully
        annotation = self.annotator.generate_annotation(invalid_file)
        assert annotation is not None
    
    def test_clean_docstring(self):
        """Test docstring cleaning."""
        # Test various docstring formats
        test_cases = [
            ("This file contains utility functions", "utility functions"),
            ("This module handles database operations", "handles database operations"),
            ("This is a test script for automation", "test script for automation"),
        ]
        
        for input_doc, expected in test_cases:
            result = self.annotator._clean_docstring(input_doc)
            assert expected.lower() in result.lower()
    
    def test_import_analysis(self):
        """Test import analysis for context."""
        # Test Flask app
        flask_file = self.temp_dir / "app.py"
        content = '''
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
'''
        flask_file.write_text(content)
        
        annotation = self.annotator.generate_annotation(flask_file)
        assert "flask" in annotation.lower()
        
        # Test test file
        test_file = self.temp_dir / "test_app.py"
        content = '''
import pytest
import unittest
from app import app

def test_home():
    assert app is not None
'''
        test_file.write_text(content)
        
        annotation = self.annotator.generate_annotation(test_file)
        assert "test" in annotation.lower()

```

## tests\test_file_discovery.py

**Описание:** Tests for file discovery module.

**Размер:** 0.01 МБ | **Строки:** 165 | **Хэш:** `89347d3994a6`

```python
"""Tests for file discovery module."""

import tempfile
import shutil
from pathlib import Path
import pytest

from app.file_discovery import FileDiscovery


class TestFileDiscovery:
    """Test cases for FileDiscovery class."""
    
    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.discovery = FileDiscovery()
    
    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_text_file_detection(self):
        """Test text file detection."""
        # Create test files
        py_file = self.temp_dir / "test.py"
        py_file.write_text("print('hello')")
        
        js_file = self.temp_dir / "test.js"
        js_file.write_text("console.log('hello')")
        
        txt_file = self.temp_dir / "test.txt"
        txt_file.write_text("hello world")
        
        # Test detection (using public method)
        assert py_file.suffix.lower() in self.discovery.TEXT_EXTENSIONS
        assert js_file.suffix.lower() in self.discovery.TEXT_EXTENSIONS
        assert txt_file.suffix.lower() in self.discovery.TEXT_EXTENSIONS
    
    def test_binary_file_detection(self):
        """Test binary file detection."""
        # Create binary file
        bin_file = self.temp_dir / "test.bin"
        bin_file.write_bytes(b'\x00\x01\x02\x03')
        
        # Test detection (using public methods)
        assert bin_file.suffix.lower() not in self.discovery.TEXT_EXTENSIONS
        from app.utils import is_binary_file
        assert is_binary_file(bin_file)
    
    def test_excluded_directories(self):
        """Test excluded directories."""
        # Create excluded directories
        (self.temp_dir / ".git").mkdir()
        (self.temp_dir / "node_modules").mkdir()
        (self.temp_dir / "__pycache__").mkdir()
        
        # Create files in excluded directories
        (self.temp_dir / ".git" / "config").write_text("git config")
        (self.temp_dir / "node_modules" / "package.json").write_text("{}")
        (self.temp_dir / "__pycache__" / "test.pyc").write_bytes(b'\x00')
        
        # Create regular files
        (self.temp_dir / "main.py").write_text("print('hello')")
        (self.temp_dir / "README.md").write_text("# Test")
        
        # Discover files
        files = self.discovery.discover_files(self.temp_dir)
        file_names = [f.name for f in files]
        
        # Should not include files from excluded directories
        assert "config" not in file_names
        assert "package.json" not in file_names
        assert "test.pyc" not in file_names
        
        # Should include regular files
        assert "main.py" in file_names
        assert "README.md" in file_names
    
    def test_gitignore_support(self):
        """Test .gitignore support."""
        # Create .gitignore
        gitignore = self.temp_dir / ".gitignore"
        gitignore.write_text("*.log\n*.tmp\nbuild/\n")
        
        # Create files
        (self.temp_dir / "main.py").write_text("print('hello')")
        (self.temp_dir / "app.log").write_text("log content")
        (self.temp_dir / "temp.tmp").write_text("temp content")
        (self.temp_dir / "build").mkdir()
        (self.temp_dir / "build" / "output.txt").write_text("build output")
        
        # Discover files with gitignore
        discovery = FileDiscovery(include_gitignore=True)
        files = discovery.discover_files(self.temp_dir)
        file_names = [f.name for f in files]
        
        # Should exclude gitignored files
        assert "app.log" not in file_names
        assert "temp.tmp" not in file_names
        assert "output.txt" not in file_names
        
        # Should include non-gitignored files
        assert "main.py" in file_names
    
    def test_file_size_limit(self):
        """Test file size limit."""
        # Create large file
        large_file = self.temp_dir / "large.txt"
        large_file.write_text("x" * (6 * 1024 * 1024))  # 6 MB
        
        # Create small file
        small_file = self.temp_dir / "small.txt"
        small_file.write_text("small content")
        
        # Discover files with 5 MB limit
        files = self.discovery.discover_files(self.temp_dir, max_file_size_mb=5)
        file_names = [f.name for f in files]
        
        # Should exclude large file
        assert "large.txt" not in file_names
        
        # Should include small file
        assert "small.txt" in file_names
    
    def test_file_stats(self):
        """Test file statistics calculation."""
        # Create test file
        test_file = self.temp_dir / "test.py"
        content = "print('hello')\nprint('world')\n"
        test_file.write_text(content)
        
        # Get stats
        size, lines, file_hash = self.discovery.get_file_stats(test_file)
        
        # Check stats - allow for small differences in file size calculation
        expected_size = len(content.encode('utf-8'))
        assert abs(size - expected_size) <= 2  # Allow small difference
        assert lines == 2
        assert len(file_hash) == 12
        assert file_hash.isalnum()
    
    def test_config_file_detection(self):
        """Test config file detection."""
        # Create config files
        json_file = self.temp_dir / "config.json"
        json_file.write_text('{"key": "value"}')
        
        yaml_file = self.temp_dir / "config.yaml"
        yaml_file.write_text("key: value")
        
        # Test detection
        assert self.discovery._is_config_file(json_file)
        assert self.discovery._is_config_file(yaml_file)
    
    def test_empty_directory(self):
        """Test empty directory handling."""
        files = self.discovery.discover_files(self.temp_dir)
        assert files == []
    
    def test_nonexistent_directory(self):
        """Test nonexistent directory handling."""
        nonexistent = self.temp_dir / "nonexistent"
        files = self.discovery.discover_files(nonexistent)
        assert files == []

```

## tests\test_md_builder.py

**Описание:** Tests for markdown builder module.

**Размер:** 0.01 МБ | **Строки:** 284 | **Хэш:** `8c6076b777ad`

```python
"""Tests for markdown builder module."""

import tempfile
import shutil
from pathlib import Path
import pytest

from app.md_builder import MarkdownBuilder


class TestMarkdownBuilder:
    """Test cases for MarkdownBuilder class."""
    
    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.builder = MarkdownBuilder()
    
    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_language_mapping(self):
        """Test language mapping for code blocks."""
        # Test various file extensions
        test_cases = [
            (".py", "python"),
            (".js", "javascript"),
            (".ts", "typescript"),
            (".html", "html"),
            (".css", "css"),
            (".json", "json"),
            (".yaml", "yaml"),
            (".md", "markdown"),
            (".unknown", "text"),
        ]
        
        for ext, expected_lang in test_cases:
            file_path = Path(f"test{ext}")
            result = self.builder._get_language(file_path)
            assert result == expected_lang
    
    def test_file_to_anchor(self):
        """Test file path to anchor conversion."""
        test_cases = [
            (Path("test.py"), "test-py"),
            (Path("folder/test.py"), "folder-test-py"),
            (Path("folder/subfolder/file.js"), "folder-subfolder-file-js"),
            (Path("file with spaces.py"), "file-with-spaces-py"),
            (Path("file.with.dots.py"), "file-with-dots-py"),
        ]
        
        for file_path, expected_anchor in test_cases:
            result = self.builder._file_to_anchor(file_path)
            assert result == expected_anchor
    
    def test_markdown_generation(self):
        """Test markdown generation."""
        # Create test project structure
        project_dir = self.temp_dir / "test_project"
        project_dir.mkdir()
        
        # Create test files
        (project_dir / "main.py").write_text('print("Hello, world!")')
        (project_dir / "README.md").write_text("# Test Project\n\nA simple test project.")
        (project_dir / "config.json").write_text('{"name": "test"}')
        
        # Create subdirectory
        (project_dir / "utils").mkdir()
        (project_dir / "utils" / "helper.py").write_text('def helper(): pass')
        
        # Generate markdown
        output_file = self.temp_dir / "output.md"
        success = self.builder.build_markdown(
            project_path=project_dir,
            output_path=output_file,
            include_gitignore=False,
            include_config_files=True,
            max_file_size_mb=5
        )
        
        assert success
        assert output_file.exists()
        
        # Check content
        content = output_file.read_text(encoding='utf-8')
        
        # Should contain project name
        assert "# test_project" in content
        
        # Should contain file sections
        assert "## main.py" in content
        assert "## README.md" in content
        assert "## config.json" in content
        # Check for both forward and backward slashes
        assert ("## utils/helper.py" in content or "## utils\\helper.py" in content)
        
        # Should contain code blocks
        assert "```python" in content
        assert "```markdown" in content
        assert "```json" in content
        
        # Should contain table of contents
        assert "## Оглавление" in content
        
        # Should contain appendices
        assert "## Приложения" in content
    
    def test_preview_generation(self):
        """Test preview generation."""
        # Create test project
        project_dir = self.temp_dir / "test_project"
        project_dir.mkdir()
        
        (project_dir / "main.py").write_text('print("Hello, world!")')
        (project_dir / "README.md").write_text("# Test Project")
        
        files = list(project_dir.rglob("*"))
        files = [f for f in files if f.is_file()]
        
        # Generate preview
        preview = self.builder.generate_preview(
            project_path=project_dir,
            files=files,
            max_lines=50
        )
        
        # Check preview content
        assert "# test_project" in preview
        assert "## Сводка" in preview
        assert "## Оглавление" in preview
        assert "main.py" in preview
        assert "README.md" in preview
    
    def test_large_file_handling(self):
        """Test large file handling."""
        # Create project with large file
        project_dir = self.temp_dir / "test_project"
        project_dir.mkdir()
        
        # Create large file (6 MB)
        large_file = project_dir / "large.txt"
        large_file.write_text("x" * (6 * 1024 * 1024))
        
        # Create small file
        small_file = project_dir / "small.py"
        small_file.write_text('print("small")')
        
        # Generate markdown with 5 MB limit
        output_file = self.temp_dir / "output.md"
        success = self.builder.build_markdown(
            project_path=project_dir,
            output_path=output_file,
            include_large_files=False,
            max_file_size_mb=5
        )
        
        assert success
        content = output_file.read_text(encoding='utf-8')
        
        # Should not include large file
        assert "## large.txt" not in content
        
        # Should include small file
        assert "## small.py" in content
    
    def test_encoding_handling(self):
        """Test encoding handling."""
        # Create project with different encodings
        project_dir = self.temp_dir / "test_project"
        project_dir.mkdir()
        
        # UTF-8 file
        utf8_file = project_dir / "utf8.txt"
        utf8_file.write_text("Привет, мир!", encoding='utf-8')
        
        # Latin-1 file
        latin1_file = project_dir / "latin1.txt"
        latin1_file.write_text("Héllo, wørld!", encoding='latin-1')
        
        # Generate markdown
        output_file = self.temp_dir / "output.md"
        success = self.builder.build_markdown(
            project_path=project_dir,
            output_path=output_file
        )
        
        assert success
        content = output_file.read_text(encoding='utf-8')
        
        # Should handle both encodings
        assert "Привет, мир!" in content
        assert "Héllo, wørld!" in content
    
    def test_empty_project(self):
        """Test empty project handling."""
        # Create empty project
        project_dir = self.temp_dir / "empty_project"
        project_dir.mkdir()
        
        # Generate markdown
        output_file = self.temp_dir / "output.md"
        success = self.builder.build_markdown(
            project_path=project_dir,
            output_path=output_file
        )
        
        # Should handle empty project gracefully
        assert success
        assert output_file.exists()
        
        content = output_file.read_text(encoding='utf-8')
        assert "# empty_project" in content
        # Check for any mention of 0 files
        assert ("файлов: 0" in content or "файлов:** 0" in content)
    
    def test_file_stats_in_appendices(self):
        """Test file statistics in appendices."""
        # Create project with different file types
        project_dir = self.temp_dir / "test_project"
        project_dir.mkdir()
        
        (project_dir / "main.py").write_text('print("hello")')
        (project_dir / "app.js").write_text('console.log("hello")')
        (project_dir / "style.css").write_text('body { margin: 0; }')
        (project_dir / "config.json").write_text('{"key": "value"}')
        
        # Generate markdown
        output_file = self.temp_dir / "output.md"
        success = self.builder.build_markdown(
            project_path=project_dir,
            output_path=output_file
        )
        
        assert success
        content = output_file.read_text(encoding='utf-8')
        
        # Should contain file type statistics
        assert "### Статистика по типам файлов" in content
        assert ".py" in content
        assert ".js" in content
        assert ".css" in content
        assert ".json" in content
        
        # Should contain largest files section
        assert "### Топ-10 самых больших файлов" in content
        
        # Should contain environment metadata
        assert "### Метаданные окружения" in content
        assert "Python версия:" in content
        assert "Операционная система:" in content
    
    def test_directory_structure_in_toc(self):
        """Test directory structure in table of contents."""
        # Create nested project structure
        project_dir = self.temp_dir / "test_project"
        project_dir.mkdir()
        
        # Root files
        (project_dir / "main.py").write_text('print("main")')
        (project_dir / "README.md").write_text('# Project')
        
        # Subdirectory files
        (project_dir / "src").mkdir()
        (project_dir / "src" / "app.py").write_text('print("app")')
        (project_dir / "src" / "utils.py").write_text('def util(): pass')
        
        (project_dir / "tests").mkdir()
        (project_dir / "tests" / "test_app.py").write_text('def test(): pass')
        
        # Generate markdown
        output_file = self.temp_dir / "output.md"
        success = self.builder.build_markdown(
            project_path=project_dir,
            output_path=output_file
        )
        
        assert success
        content = output_file.read_text(encoding='utf-8')
        
        # Should organize TOC by directory
        assert "## Оглавление" in content
        assert "**src/**" in content
        assert "**tests/**" in content

```

## version_info.txt

**Описание:** For more details about fixed file info 'ffi' see:

**Размер:** 0.00 МБ | **Строки:** 43 | **Хэш:** `a4616322d3ac`

```text
# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers=(1,1,0,0),
    prodvers=(1,1,0,0),
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x4,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Code to Markdown Team'),
        StringStruct(u'FileDescription', u'Desktop GUI tool to convert project source code to Markdown'),
        StringStruct(u'FileVersion', u'1.1.0'),
        StringStruct(u'InternalName', u'CodeToMarkdown'),
        StringStruct(u'LegalCopyright', u'Copyright (C) 2024 Code to Markdown Team'),
        StringStruct(u'OriginalFilename', u'CodeToMarkdown.exe'),
        StringStruct(u'ProductName', u'Code to Markdown'),
        StringStruct(u'ProductVersion', u'1.1.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)

```

## Приложения

### Статистика по типам файлов

| Расширение | Количество файлов |
|------------|-------------------|
| .css | 1 |
| .js | 1 |
| .json | 4 |
| .md | 7 |
| .py | 24 |
| .toml | 1 |
| .txt | 6 |

### Топ-10 самых больших файлов

| Файл | Размер (МБ) | Строки |
|------|-------------|--------|
| `app\ui.py` | 0.03 | 767 |
| `app\md_builder.py` | 0.02 | 434 |
| `demo_project\static\app.js` | 0.01 | 463 |
| `README.md` | 0.01 | 348 |
| `release\README.md` | 0.01 | 348 |
| `app\annotations.py` | 0.01 | 321 |
| `app\worker.py` | 0.01 | 348 |
| `tests\test_md_builder.py` | 0.01 | 284 |
| `app\file_discovery.py` | 0.01 | 256 |
| `tests\test_annotations.py` | 0.01 | 259 |

### Метаданные окружения

- **Python версия:** 3.12.3 (tags/v3.12.3:f6650f9, Apr  9 2024, 14:05:25) [MSC v.1938 64 bit (AMD64)]
- **Операционная система:** Windows 11
- **Архитектура:** AMD64
- **Время генерации:** 2025-09-19T22:49:57.514921
