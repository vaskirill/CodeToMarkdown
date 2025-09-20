"""
Модуль настроек приложения.

Содержит класс для управления конфигурацией приложения,
включая загрузку из файлов и валидацию параметров.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from utils.validators import validate_config, create_default_schema


class AppConfig:
    """Класс для управления конфигурацией приложения."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Инициализация конфигурации.
        
        Args:
            config_path: Путь к файлу конфигурации.
        """
        self.config_path = config_path or "config.json"
        self.config_data: Dict[str, Any] = {}
        self.schema = create_default_schema()
    
    def load(self) -> Dict[str, Any]:
        """Загрузка конфигурации из файла.
        
        Returns:
            Словарь с конфигурацией.
            
        Raises:
            FileNotFoundError: Если файл конфигурации не найден.
            json.JSONDecodeError: Если файл содержит некорректный JSON.
        """
        config_file = Path(self.config_path)
        
        if not config_file.exists():
            # Создать конфигурацию по умолчанию
            self.config_data = self._get_default_config()
            self.save()
            return self.config_data
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config_data = json.load(f)
            
            # Валидация конфигурации
            if not validate_config(self.config_data):
                raise ValueError("Конфигурация не прошла валидацию")
            
            return self.config_data
            
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Ошибка парсинга JSON в {self.config_path}: {e}")
    
    def save(self) -> None:
        """Сохранение конфигурации в файл."""
        config_file = Path(self.config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config_data, f, indent=2, ensure_ascii=False)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Получение значения конфигурации.
        
        Args:
            key: Ключ конфигурации.
            default: Значение по умолчанию.
            
        Returns:
            Значение конфигурации или значение по умолчанию.
        """
        return self.config_data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Установка значения конфигурации.
        
        Args:
            key: Ключ конфигурации.
            value: Значение для установки.
        """
        self.config_data[key] = value
    
    def update(self, config_dict: Dict[str, Any]) -> None:
        """Обновление конфигурации из словаря.
        
        Args:
            config_dict: Словарь с новыми значениями.
        """
        self.config_data.update(config_dict)
    
    def validate(self) -> tuple[bool, list]:
        """Валидация текущей конфигурации.
        
        Returns:
            Кортеж (успех, список ошибок).
        """
        from utils.validators import ConfigValidator
        
        validator = ConfigValidator(self.schema)
        return validator.validate(self.config_data)
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Получение конфигурации по умолчанию.
        
        Returns:
            Словарь с конфигурацией по умолчанию.
        """
        return {
            'app_name': 'Demo Application',
            'version': '1.0.0',
            'debug': False,
            'port': 8080,
            'host': 'localhost',
            'database_url': 'sqlite:///demo.db',
            'log_level': 'INFO',
            'max_workers': 4,
            'timeout': 30,
            'features': {
                'enable_caching': True,
                'enable_metrics': False,
                'enable_debug_toolbar': False
            },
            'paths': {
                'data_dir': './data',
                'log_dir': './logs',
                'temp_dir': './temp'
            }
        }
    
    def get_database_config(self) -> Dict[str, Any]:
        """Получение конфигурации базы данных.
        
        Returns:
            Словарь с конфигурацией БД.
        """
        return {
            'url': self.get('database_url', 'sqlite:///demo.db'),
            'pool_size': self.get('db_pool_size', 5),
            'max_overflow': self.get('db_max_overflow', 10),
            'echo': self.get('debug', False)
        }
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Получение конфигурации логирования.
        
        Returns:
            Словарь с конфигурацией логирования.
        """
        return {
            'level': self.get('log_level', 'INFO'),
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'file': self.get('log_file', 'app.log'),
            'max_size': self.get('log_max_size', 10 * 1024 * 1024),  # 10 MB
            'backup_count': self.get('log_backup_count', 5)
        }
    
    def is_development(self) -> bool:
        """Проверка режима разработки.
        
        Returns:
            True если приложение в режиме разработки.
        """
        return self.get('debug', False) or os.getenv('DEMO_DEBUG', '').lower() == 'true'
    
    def is_production(self) -> bool:
        """Проверка режима продакшена.
        
        Returns:
            True если приложение в режиме продакшена.
        """
        return not self.is_development()
    
    def get_feature_flag(self, feature: str) -> bool:
        """Получение флага функции.
        
        Args:
            feature: Имя функции.
            
        Returns:
            True если функция включена.
        """
        features = self.get('features', {})
        return features.get(feature, False)
    
    def set_feature_flag(self, feature: str, enabled: bool) -> None:
        """Установка флага функции.
        
        Args:
            feature: Имя функции.
            enabled: Включена ли функция.
        """
        if 'features' not in self.config_data:
            self.config_data['features'] = {}
        
        self.config_data['features'][feature] = enabled
