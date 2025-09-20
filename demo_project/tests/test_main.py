"""
Тесты для основного модуля приложения.

Содержит unit-тесты для проверки корректности работы
главного модуля демонстрационного приложения.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import DemoApp


class TestDemoApp(unittest.TestCase):
    """Тесты для класса DemoApp."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.config_file = self.temp_dir / "test_config.json"
        
        # Создание тестовой конфигурации
        self.test_config = {
            "app_name": "Test App",
            "version": "1.0.0",
            "debug": True
        }
        
        import json
        with open(self.config_file, 'w') as f:
            json.dump(self.test_config, f)
    
    def tearDown(self):
        """Очистка тестового окружения."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_app_initialization(self):
        """Тест инициализации приложения."""
        app = DemoApp(str(self.config_file))
        
        self.assertIsNotNone(app.config)
        self.assertIsInstance(app.data, dict)
    
    def test_app_initialization_without_config(self):
        """Тест инициализации приложения без конфигурации."""
        app = DemoApp()
        
        self.assertIsNotNone(app.config)
        self.assertIsInstance(app.data, dict)
    
    @patch('main.DemoApp._load_config')
    @patch('main.DemoApp._initialize_data')
    @patch('main.DemoApp._main_loop')
    def test_run_success(self, mock_main_loop, mock_init_data, mock_load_config):
        """Тест успешного запуска приложения."""
        mock_load_config.return_value = True
        
        app = DemoApp(str(self.config_file))
        result = app.run()
        
        self.assertEqual(result, 0)
        mock_load_config.assert_called_once()
        mock_init_data.assert_called_once()
        mock_main_loop.assert_called_once()
    
    @patch('main.DemoApp._load_config')
    def test_run_config_load_failure(self, mock_load_config):
        """Тест запуска при неудачной загрузке конфигурации."""
        mock_load_config.return_value = False
        
        app = DemoApp(str(self.config_file))
        result = app.run()
        
        self.assertEqual(result, 1)
    
    @patch('main.DemoApp._load_config')
    @patch('main.DemoApp._initialize_data')
    def test_run_keyboard_interrupt(self, mock_init_data, mock_load_config):
        """Тест обработки прерывания клавиатурой."""
        mock_load_config.return_value = True
        mock_init_data.side_effect = KeyboardInterrupt()
        
        app = DemoApp(str(self.config_file))
        result = app.run()
        
        self.assertEqual(result, 1)
    
    @patch('main.DemoApp._load_config')
    @patch('main.DemoApp._initialize_data')
    def test_run_general_exception(self, mock_init_data, mock_load_config):
        """Тест обработки общего исключения."""
        mock_load_config.return_value = True
        mock_init_data.side_effect = Exception("Test error")
        
        app = DemoApp(str(self.config_file))
        result = app.run()
        
        self.assertEqual(result, 1)
    
    def test_initialize_data(self):
        """Тест инициализации данных."""
        app = DemoApp(str(self.config_file))
        app._initialize_data()
        
        self.assertIn('items', app.data)
        self.assertIn('processed_count', app.data)
        self.assertEqual(app.data['items'], [])
        self.assertEqual(app.data['processed_count'], 0)
    
    def test_main_loop(self):
        """Тест основного цикла."""
        app = DemoApp(str(self.config_file))
        app.data = {'items': [], 'processed_count': 0}
        
        app._main_loop()
        
        self.assertEqual(len(app.data['items']), 5)
        self.assertEqual(app.data['processed_count'], 5)
        
        # Проверка структуры элементов
        for i, item in enumerate(app.data['items']):
            self.assertEqual(item['id'], i + 1)
            self.assertEqual(item['name'], f'Item {i + 1}')
            self.assertIn('hash', item)
            self.assertIn('message', item)
    
    def test_get_statistics(self):
        """Тест получения статистики."""
        app = DemoApp(str(self.config_file))
        app.data = {
            'items': [{'id': 1}, {'id': 2}],
            'processed_count': 2,
            'config': {'loaded': True}
        }
        
        stats = app.get_statistics()
        
        self.assertEqual(stats['total_items'], 2)
        self.assertEqual(stats['processed_count'], 2)
        self.assertTrue(stats['config_loaded'])


class TestMainFunction(unittest.TestCase):
    """Тесты для функции main."""
    
    @patch('main.DemoApp')
    def test_main_function(self, mock_demo_app_class):
        """Тест функции main."""
        mock_app = MagicMock()
        mock_app.run.return_value = 0
        mock_demo_app_class.return_value = mock_app
        
        from main import main
        result = main()
        
        self.assertEqual(result, 0)
        mock_demo_app_class.assert_called_once()
        mock_app.run.assert_called_once()


if __name__ == '__main__':
    unittest.main()
