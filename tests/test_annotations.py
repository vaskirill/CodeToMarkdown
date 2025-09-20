# Copyright (c) 2025 Kirill Vasilev
# Licensed under the MIT License. See LICENSE file for details.

"""Tests for annotations module."""

import tempfile
import shutil
from pathlib import Path
import pytest

from src.annotations import FileAnnotator


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
