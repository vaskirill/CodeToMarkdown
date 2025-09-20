"""
Модуль валидации данных для демонстрационного приложения.

Содержит функции для проверки корректности различных типов данных
и конфигурационных параметров.
"""

import re
from typing import Any, Dict, List, Optional, Union


def validate_email(email: str) -> bool:
    """Валидация email адреса.
    
    Args:
        email: Email адрес для проверки.
        
    Returns:
        True если email корректен.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_url(url: str) -> bool:
    """Валидация URL.
    
    Args:
        url: URL для проверки.
        
    Returns:
        True если URL корректен.
    """
    # Поддержка различных схем URL включая sqlite
    pattern = r'^(https?|sqlite)://[^\s]*$'
    return bool(re.match(pattern, url))


def validate_positive_number(value: Union[int, float]) -> bool:
    """Валидация положительного числа.
    
    Args:
        value: Число для проверки.
        
    Returns:
        True если число положительное.
    """
    return isinstance(value, (int, float)) and value > 0


def validate_string_length(text: str, min_length: int = 1, max_length: int = 1000) -> bool:
    """Валидация длины строки.
    
    Args:
        text: Строка для проверки.
        min_length: Минимальная длина.
        max_length: Максимальная длина.
        
    Returns:
        True если длина строки в допустимых пределах.
    """
    return isinstance(text, str) and min_length <= len(text) <= max_length


def validate_config(config: Dict[str, Any]) -> bool:
    """Валидация конфигурации приложения.
    
    Args:
        config: Словарь конфигурации.
        
    Returns:
        True если конфигурация корректна.
    """
    if not isinstance(config, dict):
        return False
    
    # Обязательные поля
    required_fields = ['app_name', 'version', 'debug']
    for field in required_fields:
        if field not in config:
            return False
    
    # Проверка типов
    if not isinstance(config.get('app_name'), str):
        return False
    
    if not isinstance(config.get('version'), str):
        return False
    
    if not isinstance(config.get('debug'), bool):
        return False
    
    # Проверка опциональных полей
    if 'port' in config:
        if not validate_positive_number(config['port']):
            return False
    
    if 'host' in config:
        if not validate_string_length(config['host'], 1, 255):
            return False
    
    if 'database_url' in config:
        if not validate_url(config['database_url']):
            return False
    
    return True


def validate_list_items(items: List[Any], validator_func: callable) -> bool:
    """Валидация элементов списка.
    
    Args:
        items: Список элементов для проверки.
        validator_func: Функция валидации для каждого элемента.
        
    Returns:
        True если все элементы прошли валидацию.
    """
    if not isinstance(items, list):
        return False
    
    for item in items:
        if not validator_func(item):
            return False
    
    return True


class ConfigValidator:
    """Класс для валидации конфигурации."""
    
    def __init__(self, schema: Dict[str, Any]):
        """Инициализация валидатора.
        
        Args:
            schema: Схема валидации.
        """
        self.schema = schema
    
    def validate(self, config: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Валидация конфигурации по схеме.
        
        Args:
            config: Конфигурация для проверки.
            
        Returns:
            Кортеж (успех, список ошибок).
        """
        errors = []
        
        # Проверка обязательных полей
        for field, rules in self.schema.items():
            if rules.get('required', False) and field not in config:
                errors.append(f"Обязательное поле '{field}' отсутствует")
                continue
            
            if field in config:
                value = config[field]
                field_errors = self._validate_field(field, value, rules)
                errors.extend(field_errors)
        
        return len(errors) == 0, errors
    
    def _validate_field(self, field_name: str, value: Any, rules: Dict[str, Any]) -> List[str]:
        """Валидация отдельного поля.
        
        Args:
            field_name: Имя поля.
            value: Значение поля.
            rules: Правила валидации.
            
        Returns:
            Список ошибок валидации.
        """
        errors = []
        
        # Проверка типа
        expected_type = rules.get('type')
        if expected_type and not isinstance(value, expected_type):
            errors.append(f"Поле '{field_name}' должно быть типа {expected_type.__name__}")
            return errors
        
        # Проверка строки
        if expected_type == str:
            min_length = rules.get('min_length', 0)
            max_length = rules.get('max_length', float('inf'))
            
            if not validate_string_length(value, min_length, max_length):
                errors.append(f"Поле '{field_name}' имеет недопустимую длину")
        
        # Проверка числа
        elif expected_type in (int, float):
            min_value = rules.get('min_value', float('-inf'))
            max_value = rules.get('max_value', float('inf'))
            
            if not (min_value <= value <= max_value):
                errors.append(f"Поле '{field_name}' вне допустимого диапазона")
        
        # Проверка списка
        elif expected_type == list:
            item_validator = rules.get('item_validator')
            if item_validator and not validate_list_items(value, item_validator):
                errors.append(f"Поле '{field_name}' содержит недопустимые элементы")
        
        return errors


def create_default_schema() -> Dict[str, Any]:
    """Создание схемы валидации по умолчанию.
    
    Returns:
        Схема валидации.
    """
    return {
        'app_name': {
            'type': str,
            'required': True,
            'min_length': 1,
            'max_length': 100
        },
        'version': {
            'type': str,
            'required': True,
            'min_length': 1,
            'max_length': 20
        },
        'debug': {
            'type': bool,
            'required': True
        },
        'port': {
            'type': int,
            'required': False,
            'min_value': 1,
            'max_value': 65535
        },
        'host': {
            'type': str,
            'required': False,
            'min_length': 1,
            'max_length': 255
        },
        'database_url': {
            'type': str,
            'required': False,
            'min_length': 1
        }
    }
