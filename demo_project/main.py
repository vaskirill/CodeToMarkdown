"""
Главный модуль демонстрационного приложения.

Этот модуль содержит основную логику приложения и демонстрирует
различные возможности Python для генерации аннотаций.
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional

from utils.helpers import format_message, calculate_hash
from utils.validators import validate_config
from config.settings import AppConfig


class DemoApp:
    """Демонстрационное приложение."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Инициализация приложения.
        
        Args:
            config_path: Путь к файлу конфигурации.
        """
        self.config = AppConfig(config_path)
        self.data: Dict[str, any] = {}
    
    def run(self) -> int:
        """Запуск приложения.
        
        Returns:
            Код завершения.
        """
        try:
            print("Запуск демонстрационного приложения...")
            
            # Загрузка конфигурации
            if not self._load_config():
                return 1
            
            # Инициализация данных
            self._initialize_data()
            
            # Основной цикл
            self._main_loop()
            
            print("Приложение завершено успешно.")
            return 0
            
        except KeyboardInterrupt:
            print("\nПриложение прервано пользователем.")
            return 1
        except Exception as e:
            print(f"Ошибка: {e}")
            return 1
    
    def _load_config(self) -> bool:
        """Загрузка конфигурации.
        
        Returns:
            True если конфигурация загружена успешно.
        """
        try:
            config_data = self.config.load()
            if not validate_config(config_data):
                print("Ошибка валидации конфигурации.")
                return False
            
            self.data.update(config_data)
            print("Конфигурация загружена успешно.")
            return True
            
        except Exception as e:
            print(f"Ошибка загрузки конфигурации: {e}")
            return False
    
    def _initialize_data(self) -> None:
        """Инициализация данных приложения."""
        self.data['items'] = []
        self.data['processed_count'] = 0
        print("Данные инициализированы.")
    
    def _main_loop(self) -> None:
        """Основной цикл приложения."""
        for i in range(5):
            item = {
                'id': i + 1,
                'name': f'Item {i + 1}',
                'hash': calculate_hash(f'item_{i + 1}'),
                'message': format_message(f'Обработка элемента {i + 1}')
            }
            
            self.data['items'].append(item)
            self.data['processed_count'] += 1
            
            print(f"Обработано: {item['message']}")
    
    def get_statistics(self) -> Dict[str, int]:
        """Получение статистики приложения.
        
        Returns:
            Словарь со статистикой.
        """
        return {
            'total_items': len(self.data.get('items', [])),
            'processed_count': self.data.get('processed_count', 0),
            'config_loaded': 'config' in self.data
        }


def main() -> int:
    """Точка входа в приложение.
    
    Returns:
        Код завершения.
    """
    app = DemoApp()
    return app.run()


if __name__ == '__main__':
    sys.exit(main())
