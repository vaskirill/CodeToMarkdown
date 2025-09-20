"""
Вспомогательные функции для демонстрационного приложения.

Этот модуль содержит утилитарные функции для работы с данными,
форматирования сообщений и вычисления хэшей.
"""

import hashlib
import datetime
from typing import Any, Union


def format_message(text: str, timestamp: bool = True) -> str:
    """Форматирование сообщения с временной меткой.
    
    Args:
        text: Текст сообщения.
        timestamp: Добавлять ли временную метку.
        
    Returns:
        Отформатированное сообщение.
    """
    if timestamp:
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M:%S")
        return f"[{time_str}] {text}"
    return text


def calculate_hash(data: Union[str, bytes]) -> str:
    """Вычисление SHA-256 хэша для данных.
    
    Args:
        data: Данные для хэширования.
        
    Returns:
        SHA-256 хэш в шестнадцатеричном формате.
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    hash_obj = hashlib.sha256()
    hash_obj.update(data)
    return hash_obj.hexdigest()[:12]  # Первые 12 символов


def safe_divide(a: float, b: float, default: float = 0.0) -> float:
    """Безопасное деление с обработкой деления на ноль.
    
    Args:
        a: Делимое.
        b: Делитель.
        default: Значение по умолчанию при делении на ноль.
        
    Returns:
        Результат деления или значение по умолчанию.
    """
    try:
        return a / b if b != 0 else default
    except (TypeError, ZeroDivisionError):
        return default


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Обрезание строки до указанной длины.
    
    Args:
        text: Исходная строка.
        max_length: Максимальная длина.
        suffix: Суффикс для обрезанных строк.
        
    Returns:
        Обрезанная строка.
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def merge_dictionaries(*dicts: dict) -> dict:
    """Объединение нескольких словарей.
    
    Args:
        *dicts: Словари для объединения.
        
    Returns:
        Объединенный словарь.
    """
    result = {}
    for d in dicts:
        if isinstance(d, dict):
            result.update(d)
    return result


class DataProcessor:
    """Класс для обработки данных."""
    
    def __init__(self, batch_size: int = 10):
        """Инициализация процессора.
        
        Args:
            batch_size: Размер пакета для обработки.
        """
        self.batch_size = batch_size
        self.processed_count = 0
    
    def process_item(self, item: Any) -> dict:
        """Обработка одного элемента.
        
        Args:
            item: Элемент для обработки.
            
        Returns:
            Результат обработки.
        """
        self.processed_count += 1
        
        return {
            'original': item,
            'processed_at': datetime.datetime.now().isoformat(),
            'hash': calculate_hash(str(item)),
            'batch_number': (self.processed_count - 1) // self.batch_size + 1
        }
    
    def process_batch(self, items: list) -> list:
        """Обработка пакета элементов.
        
        Args:
            items: Список элементов для обработки.
            
        Returns:
            Список обработанных элементов.
        """
        results = []
        for item in items:
            result = self.process_item(item)
            results.append(result)
        
        return results
    
    def get_statistics(self) -> dict:
        """Получение статистики обработки.
        
        Returns:
            Словарь со статистикой.
        """
        return {
            'processed_count': self.processed_count,
            'batch_size': self.batch_size,
            'total_batches': (self.processed_count - 1) // self.batch_size + 1
        }
