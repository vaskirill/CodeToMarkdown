# Copyright (c) 2025 Kirill Vasilev
# Licensed under the MIT License. See LICENSE file for details.

"""Tests for markdown builder module."""

import tempfile
import shutil
from pathlib import Path
import pytest

from src.md_builder import MarkdownBuilder


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
