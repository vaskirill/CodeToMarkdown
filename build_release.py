#!/usr/bin/env python3
# Copyright (c) 2025 Kirill Vasilev
# Licensed under the MIT License. See LICENSE file for details.

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
    icon='CodeToMarkdown.ico' if os.path.exists('CodeToMarkdown.ico') else None,
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
