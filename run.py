#!/usr/bin/env python3
# Copyright (c) 2025 Kirill Vasilev
# Licensed under the MIT License. See LICENSE file for details.

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
    from src.main import main
    sys.exit(main())
