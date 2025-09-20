# Copyright (c) 2025 Kirill Vasilev
# Licensed under the MIT License. See LICENSE file for details.

"""Background worker for file processing and markdown generation."""

import logging
from pathlib import Path

from PySide6.QtCore import QMutex, QMutexLocker, QObject, QRunnable, QThreadPool, Signal

try:
    # Try relative imports first (for development)
    from .file_discovery import FileDiscovery
    from .i18n import get_text
    from .md_builder import MarkdownBuilder
except ImportError:
    # Fallback to absolute imports (for PyInstaller)
    from src.file_discovery import FileDiscovery
    from src.i18n import get_text
    from src.md_builder import MarkdownBuilder


class WorkerSignals(QObject):
    """Signals for worker communication."""

    # Progress signals
    progress = Signal(int, str)  # progress_percent, status_message
    file_processed = Signal(str)  # file_name
    error_occurred = Signal(str)  # error_message

    # Completion signals
    files_discovered = Signal(list)  # list of file paths
    markdown_generated = Signal(str)  # output_file_path
    preview_generated = Signal(str)  # preview_content
    task_completed = Signal(bool)  # success
    task_cancelled = Signal()


class FileDiscoveryWorker(QRunnable):
    """Worker for file discovery."""

    def __init__(
        self,
        project_path: Path,
        include_gitignore: bool = True,
        include_config_files: bool = True,
        max_file_size_mb: int = 5,
    ):
        """Initialize file discovery worker.
        
        Args:
            project_path: Path to project directory.
            include_gitignore: Whether to respect .gitignore.
            include_config_files: Whether to include config files.
            max_file_size_mb: Maximum file size in MB.
        """
        super().__init__()
        self.project_path = project_path
        self.include_gitignore = include_gitignore
        self.include_config_files = include_config_files
        self.max_file_size_mb = max_file_size_mb
        self.signals = WorkerSignals()
        self.logger = logging.getLogger(__name__)
        self._cancelled = False

    def run(self) -> None:
        """Run file discovery."""
        try:
            self.signals.progress.emit(0, get_text("scanning_files"))

            discovery = FileDiscovery(
                include_gitignore=self.include_gitignore,
                include_config=self.include_config_files,
            )

            files = discovery.discover_files(self.project_path, self.max_file_size_mb)

            if self._cancelled:
                self.signals.task_cancelled.emit()
                return

            self.signals.files_discovered.emit(files)
            self.signals.progress.emit(100, get_text("completed"))
            self.signals.task_completed.emit(True)

        except Exception as e:
            self.logger.error(f"Error in file discovery: {e}")
            self.signals.error_occurred.emit(str(e))
            self.signals.task_completed.emit(False)

    def cancel(self) -> None:
        """Cancel the task."""
        self._cancelled = True


class MarkdownGenerationWorker(QRunnable):
    """Worker for markdown generation."""

    def __init__(
        self,
        project_path: Path,
        files: list[Path],
        output_path: Path,
        include_gitignore: bool = True,
        include_large_files: bool = False,
        include_config_files: bool = True,
        max_file_size_mb: int = 5,
    ):
        """Initialize markdown generation worker.
        
        Args:
            project_path: Path to project directory.
            files: List of files to process.
            output_path: Path to output markdown file.
            include_gitignore: Whether to respect .gitignore.
            include_large_files: Whether to include large files.
            include_config_files: Whether to include config files.
            max_file_size_mb: Maximum file size in MB.
        """
        super().__init__()
        self.project_path = project_path
        self.files = files
        self.output_path = output_path
        self.include_gitignore = include_gitignore
        self.include_large_files = include_large_files
        self.include_config_files = include_config_files
        self.max_file_size_mb = max_file_size_mb
        self.signals = WorkerSignals()
        self.logger = logging.getLogger(__name__)
        self._cancelled = False

    def run(self) -> None:
        """Run markdown generation."""
        try:
            self.signals.progress.emit(0, get_text("generating_markdown"))

            builder = MarkdownBuilder()

            def progress_callback(percent: int, message: str) -> None:
                if self._cancelled:
                    return
                self.signals.progress.emit(percent, message)

            success = builder.build_markdown(
                project_path=self.project_path,
                output_path=self.output_path,
                include_gitignore=self.include_gitignore,
                include_large_files=self.include_large_files,
                include_config_files=self.include_config_files,
                max_file_size_mb=self.max_file_size_mb,
                progress_callback=progress_callback,
            )

            if self._cancelled:
                self.signals.task_cancelled.emit()
                return

            if success:
                self.signals.markdown_generated.emit(str(self.output_path))
                self.signals.task_completed.emit(True)
            else:
                self.signals.error_occurred.emit("Failed to generate markdown")
                self.signals.task_completed.emit(False)

        except Exception as e:
            self.logger.error(f"Error in markdown generation: {e}")
            self.signals.error_occurred.emit(str(e))
            self.signals.task_completed.emit(False)

    def cancel(self) -> None:
        """Cancel the task."""
        self._cancelled = True


class PreviewGenerationWorker(QRunnable):
    """Worker for preview generation."""

    def __init__(
        self,
        project_path: Path,
        files: list[Path],
        max_lines: int = 200,
    ):
        """Initialize preview generation worker.
        
        Args:
            project_path: Path to project directory.
            files: List of files to process.
            max_lines: Maximum lines in preview.
        """
        super().__init__()
        self.project_path = project_path
        self.files = files
        self.max_lines = max_lines
        self.signals = WorkerSignals()
        self.logger = logging.getLogger(__name__)
        self._cancelled = False

    def run(self) -> None:
        """Run preview generation."""
        try:
            self.signals.progress.emit(0, "Generating preview...")

            builder = MarkdownBuilder()
            preview = builder.generate_preview(
                project_path=self.project_path,
                files=self.files,
                max_lines=self.max_lines,
            )

            if self._cancelled:
                self.signals.task_cancelled.emit()
                return

            self.signals.preview_generated.emit(preview)
            self.signals.progress.emit(100, get_text("completed"))
            self.signals.task_completed.emit(True)

        except Exception as e:
            self.logger.error(f"Error in preview generation: {e}")
            self.signals.error_occurred.emit(str(e))
            self.signals.task_completed.emit(False)

    def cancel(self) -> None:
        """Cancel the task."""
        self._cancelled = True


class WorkerManager:
    """Manager for background workers."""

    def __init__(self) -> None:
        """Initialize worker manager."""
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(2)  # Limit concurrent workers
        self.logger = logging.getLogger(__name__)
        self._active_workers = []
        self._mutex = QMutex()

    def start_file_discovery(
        self,
        project_path: Path,
        include_gitignore: bool = True,
        include_config_files: bool = True,
        max_file_size_mb: int = 5,
    ) -> WorkerSignals:
        """Start file discovery worker.
        
        Args:
            project_path: Path to project directory.
            include_gitignore: Whether to respect .gitignore.
            include_config_files: Whether to include config files.
            max_file_size_mb: Maximum file size in MB.
            
        Returns:
            Worker signals for communication.
        """
        worker = FileDiscoveryWorker(
            project_path=project_path,
            include_gitignore=include_gitignore,
            include_config_files=include_config_files,
            max_file_size_mb=max_file_size_mb,
        )

        with QMutexLocker(self._mutex):
            self._active_workers.append(worker)

        self.thread_pool.start(worker)
        return worker.signals

    def start_markdown_generation(
        self,
        project_path: Path,
        files: list[Path],
        output_path: Path,
        include_gitignore: bool = True,
        include_large_files: bool = False,
        include_config_files: bool = True,
        max_file_size_mb: int = 5,
    ) -> WorkerSignals:
        """Start markdown generation worker.
        
        Args:
            project_path: Path to project directory.
            files: List of files to process.
            output_path: Path to output markdown file.
            include_gitignore: Whether to respect .gitignore.
            include_large_files: Whether to include large files.
            include_config_files: Whether to include config files.
            max_file_size_mb: Maximum file size in MB.
            
        Returns:
            Worker signals for communication.
        """
        worker = MarkdownGenerationWorker(
            project_path=project_path,
            files=files,
            output_path=output_path,
            include_gitignore=include_gitignore,
            include_large_files=include_large_files,
            include_config_files=include_config_files,
            max_file_size_mb=max_file_size_mb,
        )

        with QMutexLocker(self._mutex):
            self._active_workers.append(worker)

        self.thread_pool.start(worker)
        return worker.signals

    def start_preview_generation(
        self,
        project_path: Path,
        files: list[Path],
        max_lines: int = 200,
    ) -> WorkerSignals:
        """Start preview generation worker.
        
        Args:
            project_path: Path to project directory.
            files: List of files to process.
            max_lines: Maximum lines in preview.
            
        Returns:
            Worker signals for communication.
        """
        worker = PreviewGenerationWorker(
            project_path=project_path,
            files=files,
            max_lines=max_lines,
        )

        with QMutexLocker(self._mutex):
            self._active_workers.append(worker)

        self.thread_pool.start(worker)
        return worker.signals

    def cancel_all_workers(self) -> None:
        """Cancel all active workers."""
        with QMutexLocker(self._mutex):
            for worker in self._active_workers:
                if hasattr(worker, "cancel"):
                    worker.cancel()
            self._active_workers.clear()

        self.thread_pool.clear()

    def wait_for_completion(self, timeout: int = 30000) -> bool:
        """Wait for all workers to complete.
        
        Args:
            timeout: Timeout in milliseconds.
            
        Returns:
            True if all workers completed, False if timeout.
        """
        return self.thread_pool.waitForDone(timeout)
