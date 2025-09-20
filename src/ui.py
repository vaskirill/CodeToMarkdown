# Copyright (c) 2025 Kirill Vasilev
# Licensed under the MIT License. See LICENSE file for details.

"""Main UI implementation."""

from pathlib import Path

from PySide6.QtCore import QSettings, Qt
from PySide6.QtGui import QBrush, QColor, QFont
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QStatusBar,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

try:
    # Try relative imports first (for development)
    from .config import Config
    from .i18n import get_text
    from .utils import open_file_explorer
    from .worker import WorkerManager
except ImportError:
    # Fallback to absolute imports (for PyInstaller)
    from src.config import Config
    from src.i18n import get_text
    from src.utils import open_file_explorer
    from src.worker import WorkerManager


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self) -> None:
        """Initialize main window."""
        super().__init__()
        self.config = Config()
        self.worker_manager = WorkerManager()
        self.current_files = []
        self.selected_files = set()
        self.current_project_path = None
        self._initializing = False

        # Настройки оптимизации
        self.max_tree_items = 1000
        self.show_all_files = False
        self.total_files_in_project = 0
        self.shown_files_count = 0

        self._setup_ui()
        self._setup_connections()
        self._load_settings()

        # Don't load last project path automatically
        # User should explicitly select a folder

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        self.setWindowTitle("Project File Selector")
        self.setMinimumSize(800, 600)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Project path section
        self._create_project_path_section(main_layout)

        # Files section
        self._create_files_section(main_layout)

        # Action button and status
        self._create_action_section(main_layout)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готов")

    def _create_project_path_section(self, parent_layout: QVBoxLayout) -> None:
        """Create project path section."""
        # Section title
        path_label = QLabel("Путь к проекту")
        path_label.setFont(QFont("Arial", 12, QFont.Bold))
        path_label.setStyleSheet("color: #333333; margin-bottom: 8px;")

        # Path input and button layout
        path_layout = QHBoxLayout()
        path_layout.setSpacing(10)

        # Path input field
        self.project_path_input = QLineEdit()
        self.project_path_input.setPlaceholderText("Выберите папку проекта...")
        self.project_path_input.setMinimumHeight(40)
        self.project_path_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #0078d4;
            }
        """)

        # Select folder button
        self.select_folder_btn = QPushButton("Выбрать папку")
        self.select_folder_btn.setMinimumHeight(40)
        self.select_folder_btn.setMinimumWidth(120)
        self.select_folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #f8f9fa;
                color: #333333;
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                font-weight: 500;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                border-color: #0078d4;
            }
            QPushButton:pressed {
                background-color: #dee2e6;
            }
        """)

        path_layout.addWidget(self.project_path_input)
        path_layout.addWidget(self.select_folder_btn)

        # Add to parent layout
        parent_layout.addWidget(path_label)
        parent_layout.addLayout(path_layout)

    def _create_files_section(self, parent_layout: QVBoxLayout) -> None:
        """Create files section with checkboxes."""
        # Section title
        files_label = QLabel("Файлы проекта")
        files_label.setFont(QFont("Arial", 12, QFont.Bold))
        files_label.setStyleSheet("color: #333333; margin-bottom: 8px;")

        # Files list widget
        self.files_list = QTreeWidget()
        self.files_list.setHeaderHidden(True)
        self.files_list.setRootIsDecorated(True)
        self.files_list.setAlternatingRowColors(True)
        self.files_list.setStyleSheet("""
            QTreeWidget {
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                background-color: white;
                selection-background-color: #e3f2fd;
            }
            QTreeWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
            }
            QTreeWidget::item:hover {
                background-color: #f8f9fa;
            }
            QTreeWidget::item:selected {
                background-color: #e3f2fd;
            }
        """)

        # Files container
        files_container = QWidget()
        files_layout = QVBoxLayout(files_container)
        files_layout.setContentsMargins(0, 0, 0, 0)
        files_layout.setSpacing(8)
        files_layout.addWidget(files_label)
        files_layout.addWidget(self.files_list)

        # Add to parent layout
        parent_layout.addWidget(files_container)


    def _create_action_section(self, parent_layout: QVBoxLayout) -> None:
        """Create action section with button and status."""
        # Create Markdown button
        self.create_markdown_btn = QPushButton("Создать Markdown")
        self.create_markdown_btn.setMinimumHeight(50)
        self.create_markdown_btn.setEnabled(False)
        self.create_markdown_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0078d4, stop:1 #00bcf2);
                color: white;
                font-weight: bold;
                font-size: 16px;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #106ebe, stop:1 #00a8e8);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #005a9e, stop:1 #0096d6);
            }
            QPushButton:disabled {
                background: #cccccc;
                color: #666666;
            }
        """)

        # Status info
        self.status_label = QLabel("Найдено файлов: 0, Показано: 0, Выбрано: 0")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 14px;
                padding: 8px 0px;
            }
        """)

        # Progress bar (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                text-align: center;
                background-color: #f8f9fa;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0078d4, stop:1 #00bcf2);
                border-radius: 6px;
            }
        """)

        # Cancel button (hidden by default)
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setVisible(False)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f8f9fa;
                color: #333333;
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                font-weight: 500;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                border-color: #dc3545;
            }
        """)
        self.cancel_btn.clicked.connect(self._cancel_operation)

        # Layout
        action_layout = QVBoxLayout()
        action_layout.setSpacing(12)
        action_layout.addWidget(self.create_markdown_btn)
        action_layout.addWidget(self.status_label)
        action_layout.addWidget(self.progress_bar)
        action_layout.addWidget(self.cancel_btn)

        parent_layout.addLayout(action_layout)


    def _setup_connections(self) -> None:
        """Set up signal connections."""
        self.select_folder_btn.clicked.connect(self._select_folder)
        self.create_markdown_btn.clicked.connect(self._create_markdown)

        # Files list selection - use itemChanged for checkboxes
        self.files_list.itemChanged.connect(self._on_file_item_changed)

    def _load_settings(self) -> None:
        """Load window settings."""
        settings = QSettings("CodeToMarkdown", "MainWindow")

        # Restore geometry
        geometry = settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)

        # Restore splitter state
        splitter_state = settings.value("splitterState")
        if splitter_state and hasattr(self, "main_splitter"):
            self.main_splitter.restoreState(splitter_state)

    def _save_settings(self) -> None:
        """Save window settings."""
        settings = QSettings("CodeToMarkdown", "MainWindow")
        settings.setValue("geometry", self.saveGeometry())
        if hasattr(self, "main_splitter"):
            settings.setValue("splitterState", self.main_splitter.saveState())

    def _select_folder(self) -> None:
        """Select project folder."""
        folder = QFileDialog.getExistingDirectory(
            self,
            get_text("select_folder"),
            self.config.last_project_path or str(Path.home()),
        )

        if folder:
            project_path = Path(folder)
            self._set_project_path(project_path)

    def _set_project_path(self, project_path: Path) -> None:
        """Set project path and update UI.
        
        Args:
            project_path: Path to project directory.
        """
        self.current_project_path = project_path
        self.project_path_input.setText(str(project_path))

        # Save to config
        self.config.last_project_path = str(project_path)
        self.config.save_config()

        # Enable buttons
        self.create_markdown_btn.setEnabled(True)

        # Clear previous data
        self.files_list.clear()
        self.current_files = []
        self.selected_files = set()

        # Reset statistics
        self.total_files_in_project = 0
        self.shown_files_count = 0

        # Reset file selection state
        # (select all checkbox was removed as requested)

        # Update status
        self._update_status()

        # Start file discovery
        self._discover_files()

    def _discover_files(self) -> None:
        """Start file discovery process."""
        if not self.current_project_path:
            return

        self._set_processing_state(True, "Сканирование файлов...")

        signals = self.worker_manager.start_file_discovery(
            project_path=self.current_project_path,
            include_gitignore=True,  # Always include .gitignore
            include_config_files=True,  # Always include config files
            max_file_size_mb=5,
        )

        signals.files_discovered.connect(self._on_files_discovered)
        signals.task_completed.connect(self._on_discovery_completed)
        signals.error_occurred.connect(self._on_error_occurred)

    def _on_files_discovered(self, files: list[Path]) -> None:
        """Handle files discovered.
        
        Args:
            files: List of discovered files.
        """
        self.current_files = files
        self._populate_file_tree_optimized(files)

    def _populate_file_tree_optimized(self, files: list[Path]) -> None:
        """Оптимизированное заполнение дерева файлов.
        
        Args:
            files: List of file paths that can be added to markdown.
        """
        self.files_list.clear()
        self._initializing = True

        try:
            # Создаем set of allowed files
            allowed = {str(p.relative_to(self.current_project_path)) for p in files}

            # Получаем все файлы в проекте
            all_files = []
            for file_path in self.current_project_path.rglob("*"):
                if file_path.is_file():
                    rel_path = file_path.relative_to(self.current_project_path)
                    all_files.append(rel_path)

            # Сохраняем общее количество файлов в проекте
            self.total_files_in_project = len(all_files)

            # Если файлов слишком много, показываем только разрешенные
            if len(all_files) > self.max_tree_items and not self.show_all_files:
                self._populate_tree_with_allowed_only(allowed)
                self.shown_files_count = len(allowed)
            else:
                self._populate_tree_with_all_files(all_files, allowed)
                self.shown_files_count = min(len(all_files), self.max_tree_items)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при заполнении дерева файлов: {e}")
        finally:
            self._initializing = False
            self._update_selected_files()
            self._update_status()

    def _populate_tree_with_allowed_only(self, allowed: set) -> None:
        """Заполнение дерева только разрешенными файлами.
        
        Args:
            allowed: Set of allowed file paths.
        """
        # Группируем файлы по директориям
        dirs = {}
        for file_path in allowed:
            path = Path(file_path)
            parent_dir = str(path.parent) if path.parent != Path() else "."

            if parent_dir not in dirs:
                dirs[parent_dir] = []
            dirs[parent_dir].append(path)

        # Создаем элементы дерева
        for dir_path in sorted(dirs.keys()):
            if dir_path == ".":
                parent_item = self.files_list.invisibleRootItem()
            else:
                parent_item = QTreeWidgetItem(self.files_list, [dir_path])
                parent_item.setExpanded(True)
                parent_item.setFlags(parent_item.flags() & ~Qt.ItemIsUserCheckable)
                parent_item.setData(0, Qt.UserRole, f"dir:{dir_path}")

            for file_path in sorted(dirs[dir_path]):
                self._create_file_item(parent_item, str(file_path), True)

    def _populate_tree_with_all_files(self, all_files: list[Path], allowed: set) -> None:
        """Заполнение дерева всеми файлами (с ограничением).
        
        Args:
            all_files: List of all file paths.
            allowed: Set of allowed file paths.
        """
        # Группируем файлы по директориям
        dirs = {}
        for file_path in all_files:
            parent_dir = str(file_path.parent) if file_path.parent != Path() else "."

            if parent_dir not in dirs:
                dirs[parent_dir] = []
            dirs[parent_dir].append(file_path)

        # Создаем элементы дерева
        items_created = 0
        for dir_path in sorted(dirs.keys()):
            if items_created >= self.max_tree_items:
                # Добавляем элемент "Показать больше..."
                more_item = QTreeWidgetItem(self.files_list, [f"... и еще {len(all_files) - items_created} файлов"])
                more_item.setFlags(more_item.flags() & ~Qt.ItemIsUserCheckable)
                more_item.setForeground(0, QBrush(QColor(100, 100, 100)))
                break

            if dir_path == ".":
                parent_item = self.files_list.invisibleRootItem()
            else:
                parent_item = QTreeWidgetItem(self.files_list, [dir_path])
                parent_item.setExpanded(True)
                parent_item.setFlags(parent_item.flags() & ~Qt.ItemIsUserCheckable)
                parent_item.setData(0, Qt.UserRole, f"dir:{dir_path}")
                items_created += 1

            for file_path in sorted(dirs[dir_path]):
                if items_created >= self.max_tree_items:
                    break

                can_add = str(file_path) in allowed and "PROJECT_CODEBUNDLE" not in str(file_path)
                self._create_file_item(parent_item, str(file_path), can_add)
                items_created += 1

        # Обновляем количество показанных файлов
        self.shown_files_count = items_created

    def _create_file_item(self, parent_item: QTreeWidgetItem, file_path: str, can_add: bool) -> None:
        """Создание элемента файла.
        
        Args:
            parent_item: Parent tree item.
            file_path: File path.
            can_add: Whether file can be added to markdown.
        """
        file_item = QTreeWidgetItem(parent_item, [file_path])

        if can_add:
            file_item.setFlags(file_item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            file_item.setCheckState(0, Qt.Checked)
            file_item.setToolTip(0, "Можно добавить в Markdown")
        else:
            flags = file_item.flags()
            flags &= ~(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            file_item.setFlags(flags)
            file_item.setDisabled(True)
            file_item.setCheckState(0, Qt.Unchecked)
            file_item.setForeground(0, QBrush(QColor(154, 160, 166)))

            if "PROJECT_CODEBUNDLE" in file_path:
                file_item.setToolTip(0, "Нельзя добавить в Markdown (содержит PROJECT_CODEBUNDLE)")
            else:
                file_item.setToolTip(0, "Нельзя добавить в Markdown (неподходящий тип/размер)")

        file_item.setData(0, Qt.UserRole, f"file:{file_path}")

    def _on_file_item_changed(self, item: QTreeWidgetItem, column: int) -> None:
        """Handle file item checkbox change in tree.
        
        Args:
            item: Changed tree item.
            column: Column index.
        """
        # Update selected files
        self._update_selected_files()
        self._update_status()


    def _update_selected_files(self) -> None:
        """Update the set of selected files."""
        self.selected_files.clear()

        def collect_selected_files(item):
            if item.flags() & Qt.ItemIsUserCheckable:
                if item.checkState(0) == Qt.Checked:
                    data = item.data(0, Qt.UserRole)
                    if data and data.startswith("file:"):
                        file_path = data[5:]  # Remove "file:" prefix
                        self.selected_files.add(file_path)
            for i in range(item.childCount()):
                collect_selected_files(item.child(i))

        for i in range(self.files_list.topLevelItemCount()):
            collect_selected_files(self.files_list.topLevelItem(i))

    def _update_status(self) -> None:
        """Update status label."""
        total_files = len(self.current_files)
        selected_count = len(self.selected_files)

        # Отображаем статистику: Найдено, Показано, Выбрано
        self.status_label.setText(
            f"Найдено файлов: {self.total_files_in_project}, "
            f"Показано: {self.shown_files_count}, "
            f"Выбрано: {selected_count}",
        )

        # Enable/disable create button based on selection
        self.create_markdown_btn.setEnabled(selected_count > 0)


    def _generate_preview(self) -> None:
        """Generate markdown preview."""
        if not self.current_files or not self.current_project_path:
            QMessageBox.warning(
                self,
                "Предупреждение",
                "Сначала выберите папку проекта и дождитесь завершения сканирования файлов.",
            )
            return

        self._set_processing_state(True, "Генерация предпросмотра...")

        signals = self.worker_manager.start_preview_generation(
            project_path=self.current_project_path,
            files=self.current_files,
            max_lines=200,
        )

        signals.preview_generated.connect(self._on_preview_generated)
        signals.task_completed.connect(self._on_preview_completed)
        signals.error_occurred.connect(self._on_error_occurred)

    def _on_preview_generated(self, preview_content: str) -> None:
        """Handle preview generated.
        
        Args:
            preview_content: Generated preview content.
        """
        # Show preview in a dialog
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Предпросмотр Markdown")
        dialog.setText("Предпросмотр сгенерирован успешно!")
        dialog.setDetailedText(preview_content)
        dialog.setIcon(QMessageBox.Information)
        dialog.exec()

    def _on_preview_completed(self, success: bool) -> None:
        """Handle preview generation completed.
        
        Args:
            success: Whether generation was successful.
        """
        self._set_processing_state(False)


    def _create_markdown(self) -> None:
        """Create markdown file."""
        if not self.selected_files or not self.current_project_path:
            return

        # Convert selected file paths to full paths
        selected_full_paths = []
        for rel_path in self.selected_files:
            full_path = self.current_project_path / Path(rel_path)
            if full_path.exists():
                selected_full_paths.append(full_path)

        if not selected_full_paths:
            QMessageBox.warning(
                self,
                "Предупреждение",
                "Выбранные файлы не найдены.",
            )
            return

        # Choose output file
        output_file, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить Markdown файл",
            str(self.current_project_path / "PROJECT_CODEBUNDLE.md"),
            "Markdown файлы (*.md);;Все файлы (*)",
        )

        if not output_file:
            return

        output_path = Path(output_file)
        self._set_processing_state(True, "Создание Markdown...")

        signals = self.worker_manager.start_markdown_generation(
            project_path=self.current_project_path,
            files=selected_full_paths,  # Use only selected files
            output_path=output_path,
            include_gitignore=True,  # Always include .gitignore
            include_large_files=True,  # Always include large files
            include_config_files=True,  # Always include config files
            max_file_size_mb=5,
        )

        signals.markdown_generated.connect(self._on_markdown_generated)
        signals.task_completed.connect(self._on_markdown_completed)
        signals.error_occurred.connect(self._on_error_occurred)

    def _on_markdown_generated(self, output_path: str) -> None:
        """Handle markdown generated.
        
        Args:
            output_path: Path to generated markdown file.
        """
        # Show success message
        msg = QMessageBox(self)
        msg.setWindowTitle(get_text("file_saved"))
        msg.setText(get_text("file_saved_message", path=output_path))
        msg.setIcon(QMessageBox.Information)

        open_folder_btn = msg.addButton(get_text("open_folder"), QMessageBox.ActionRole)
        msg.addButton("OK", QMessageBox.AcceptRole)

        msg.exec()

        if msg.clickedButton() == open_folder_btn:
            self._open_folder(Path(output_path).parent)

    def _open_folder(self, folder_path: Path) -> None:
        """Open folder in file explorer.
        
        Args:
            folder_path: Path to folder.
        """
        open_file_explorer(folder_path)


    def _set_processing_state(self, processing: bool, message: str = "") -> None:
        """Set processing state.
        
        Args:
            processing: Whether processing is active.
            message: Status message.
        """
        self.progress_bar.setVisible(processing)
        self.cancel_btn.setVisible(processing)

        if processing:
            self.progress_bar.setRange(0, 0)  # Indeterminate progress
            self.status_label.setText(message)
            self.status_bar.showMessage(message)
        else:
            self.progress_bar.setRange(0, 100)
            self.status_label.setText(get_text("ready"))
            self.status_bar.showMessage(get_text("ready"))

    def _cancel_operation(self) -> None:
        """Cancel current operation."""
        self.worker_manager.cancel_all_workers()
        self._set_processing_state(False)

    def _on_discovery_completed(self, success: bool) -> None:
        """Handle file discovery completed.
        
        Args:
            success: Whether discovery was successful.
        """
        self._set_processing_state(False)
        if success:
            self._update_status()


    def _on_markdown_completed(self, success: bool) -> None:
        """Handle markdown generation completed.
        
        Args:
            success: Whether generation was successful.
        """
        self._set_processing_state(False)

    def _on_error_occurred(self, error_message: str) -> None:
        """Handle error occurred.
        
        Args:
            error_message: Error message.
        """
        self._set_processing_state(False)

        msg = QMessageBox(self)
        msg.setWindowTitle(get_text("error_occurred"))
        msg.setText(error_message)
        msg.setIcon(QMessageBox.Critical)
        msg.exec()

    def _show_about(self) -> None:
        """Show about dialog."""
        msg = QMessageBox(self)
        msg.setWindowTitle("О программе")
        msg.setText("""
        <h3>Code to Markdown</h3>
        <p>Версия 1.0.0</p>
        <p>Инструмент для конвертации исходного кода проекта в Markdown файл.</p>
        <p>Разработано с использованием PySide6 и Python.</p>
        """)
        msg.setIcon(QMessageBox.Information)
        msg.exec()

    def closeEvent(self, event) -> None:
        """Handle window close event.
        
        Args:
            event: Close event.
        """
        # Cancel any running operations
        self.worker_manager.cancel_all_workers()

        # Save settings
        self._save_settings()

        # Save config
        self.config.save_config()

        event.accept()
