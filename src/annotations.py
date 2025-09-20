# Copyright (c) 2025 Kirill Vasilev
# Licensed under the MIT License. See LICENSE file for details.

"""File annotation and AST analysis module."""

import ast
import logging
import re
from pathlib import Path

try:
    # Try relative imports first (for development)
    from .i18n import get_file_type_description, get_text
    from .utils import read_file_safe
except ImportError:
    # Fallback to absolute imports (for PyInstaller)
    from src.i18n import get_file_type_description, get_text
    from src.utils import read_file_safe


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
