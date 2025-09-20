# Copyright (c) 2025 Kirill Vasilev
# Licensed under the MIT License. See LICENSE file for details.

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
