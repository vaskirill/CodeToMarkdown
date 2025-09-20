# Copyright (c) 2025 Kirill Vasilev
# Licensed under the MIT License. See LICENSE file for details.

"""Markdown builder with streaming support."""

import logging
import platform
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable

try:
    # Try relative imports first (for development)
    from .annotations import FileAnnotator
    from .file_discovery import FileDiscovery
    from .utils import clean_filename_for_anchor, read_file_safe
except ImportError:
    # Fallback to absolute imports (for PyInstaller)
    from src.annotations import FileAnnotator
    from src.file_discovery import FileDiscovery
    from src.utils import clean_filename_for_anchor, read_file_safe


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
