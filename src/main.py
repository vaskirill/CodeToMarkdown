# Copyright (c) 2025 Kirill Vasilev
# Licensed under the MIT License. See LICENSE file for details.

"""Main application entry point."""

import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMessageBox

try:
    # Try relative imports first (for development)
    from .logging_setup import setup_logging
    from .ui import MainWindow
except ImportError:
    # Fallback to absolute imports (for PyInstaller)
    from src.logging_setup import setup_logging
    from src.ui import MainWindow


def main() -> int:
    """Main application entry point.
    
    Returns:
        Exit code.
    """
    # Set up logging
    logger = setup_logging()
    logger.info("Starting Code to Markdown application v1.1.0")
    logger.debug("Python version: %s", sys.version)
    logger.debug("Platform: %s", sys.platform)

    try:
        # Create QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("Code to Markdown")
        app.setApplicationVersion("1.1.0")
        app.setOrganizationName("CodeToMarkdown")

        # Set application style
        app.setStyle("Fusion")

        # Set application icon (if available)
        try:
            icon_path = Path(__file__).parent / "icon.ico"
            if icon_path.exists():
                app.setWindowIcon(QIcon(str(icon_path)))
        except Exception:
            pass  # Icon not critical

        # Create and show main window
        logger.debug("Creating main window...")
        window = MainWindow()
        logger.debug("Main window created successfully")
        window.show()
        logger.info("Main window displayed")

        # Run application
        return app.exec()

    except Exception as e:
        logger.error(f"Fatal error: {e}")

        # Show error message if possible
        try:
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)

            msg = QMessageBox()
            msg.setWindowTitle("Fatal Error")
            msg.setText(f"Произошла критическая ошибка:\n{e!s}")
            msg.setIcon(QMessageBox.Critical)
            msg.exec()
        except Exception:
            print(f"Fatal error: {e}")

        return 1

    finally:
        logger.info("Application shutdown")


if __name__ == "__main__":
    sys.exit(main())
