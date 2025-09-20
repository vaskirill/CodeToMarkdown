# Copyright (c) 2025 Kirill Vasilev
# Licensed under the MIT License. See LICENSE file for details.

"""Tests for file discovery module."""

import tempfile
import shutil
from pathlib import Path
import pytest

from src.file_discovery import FileDiscovery


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
        from src.utils import is_binary_file
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
