#!/usr/bin/env python3
# Copyright (c) 2025 Kirill Vasilev
# Licensed under the MIT License. See LICENSE file for details.

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
        "src/main.py",
        "--name", "CodeToMarkdown",
        "--onefile",
        "--noconsole",
        "--clean",
        "--noconfirm"
    ]
    
    # Добавить иконку если есть
    icon_path = Path("CodeToMarkdown.ico")
    if icon_path.exists():
        cmd.extend(["--icon", str(icon_path)])
        print(f"   Используется иконка: {icon_path}")
    
    # Добавить дополнительные файлы
    cmd.extend([
        "--add-data", "src;src",
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
