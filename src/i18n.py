# Copyright (c) 2025 Kirill Vasilev
# Licensed under the MIT License. See LICENSE file for details.

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
