[![CI](https://github.com/kirill-vasilev/code-to-markdown/workflows/CI/badge.svg)](https://github.com/kirill-vasilev/code-to-markdown/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PySide6](https://img.shields.io/badge/PySide6-6.9.2-green.svg)](https://pypi.org/project/PySide6/)

> **Transform your source code into beautiful, well-documented Markdown files with intelligent annotations and project structure visualization.**

<img width="316" height="326" alt="LOGO" src="https://github.com/user-attachments/assets/f498027a-bd04-4dcb-a57d-10f5815b0462" />


## Code to Markdown — ваш умный помощник для wibe-кодинга и общения с нейросетями 🚀

Преобразуйте свой исходный код в красивые, структурированные и понятные Markdown-файлы.
Code to Markdown превращает любой проект в наглядную документацию с аннотациями, статистикой и визуализацией — идеально для совместной работы и получения обратной связи от нейронных сетей.

✨ Почему это удобно именно для wibe-кодинга?
🧠 Готовьте код так, чтобы его было легко показывать нейросетям и коллегам.
🤖 Получайте качественный фидбек от AI-ассистентов: структурированные аннотации делают ваш проект прозрачным для анализа.
🔄 Экспериментируйте быстрее — смотрите, как разные нейросети «видят» ваш проект и что советуют.
📚 Используйте Markdown как универсальный формат для общения: легко делиться, редактировать и комментировать.

## 🌟 Функции

🗂️ Автоматическое сканирование структуры, фильтрация по .gitignore
🚫 Умная фильтрация — исключение лишних или бинарных файлов
⚡ Оптимизация для больших проектов — справляется даже с 1000+ файлов
🎨 Современный GUI — красивый, интуитивный интерфейс на PySide6

## 🏆 Итог

Code to Markdown — это не просто генератор документации.
Это инструмент для продуктивного wibe-кодинга, который превращает ваш проект в удобный, визуально понятный «разговорный формат» для любых нейросетей и коллег.

## Code to Markdown — your smart assistant for vibe-coding and interacting with neural networks 🚀

Transform your source code into beautiful, structured, and easy-to-read Markdown files.
Code to Markdown turns any project into clear documentation with annotations, statistics, and visualization — perfect for collaboration and getting feedback from neural networks.

✨ Why is this especially useful for vibe-coding?
🧠 Prepare your code so it’s easy to show to neural networks and colleagues.
🤖 Get quality feedback from AI assistants: structured annotations make your project transparent for analysis.
🔄 Experiment faster — see how different neural networks “perceive” your project and what they suggest.
📚 Use Markdown as a universal communication format: easy to share, edit, and comment on.

## 🌟 Features

🗂️ Automatic project structure scanning, with .gitignore support
🚫 Smart filtering — excluding unnecessary or binary files
⚡ Optimized for large projects — handles even 1000+ files
🎨 Modern GUI — sleek, intuitive interface built with PySide6

## 🏆 Bottom line

Code to Markdown is more than just a documentation generator.
It’s a tool for productive vibe-coding that turns your project into a convenient, visually clear “conversational format” for any neural networks and colleagues.

## 🚀 Quick Start

### Installation

#### Option 1: Download Executable (Recommended)
1. Download the latest release from [Releases](https://github.com/kirill-vasilev/code-to-markdown/releases)
2. Extract and run `CodeToMarkdown.exe`

#### Option 2: Install from Source
```bash
# Clone the repository
git clone https://github.com/kirill-vasilev/code-to-markdown.git
cd code-to-markdown

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Run the application
python -m src.main
```

### Basic Usage

1. **Launch the application**
2. **Select project folder** - Click "Select Project" and choose your source code directory
3. **Configure options** (optional):
   - Enable/disable .gitignore support
   - Set maximum file size limit
   - Choose to include config files
4. **Preview** - Click "Preview" to see the generated Markdown
5. **Generate** - Click "Generate" to create the final documentation

## 📸 Screenshots

<img width="2170" height="1460" alt="image" src="https://github.com/user-attachments/assets/a35c1374-70ec-4ed7-9a59-dc6699e6c81c" />


## 🛠️ Configuration

### Environment Variables

Copy `env.example` to `.env` and customize:

```bash
cp env.example .env
```

Key configuration options:
- `MAX_FILE_SIZE_MB` - Maximum file size to process (default: 5MB)
- `INCLUDE_GITIGNORE` - Respect .gitignore files (default: true)
- `INCLUDE_CONFIG_FILES` - Include configuration files (default: true)
- `LANGUAGE` - Interface language (ru/en, default: ru)

### Supported File Types

- **Programming Languages**: Python, JavaScript, TypeScript, HTML, CSS
- **Configuration**: JSON, YAML, TOML, INI, CFG
- **Documentation**: Markdown, Text files
- **Scripts**: Shell, Batch, PowerShell

## 🧪 Development

### Prerequisites

- Python 3.11 or higher
- Git
- Code editor (VS Code recommended)

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/kirill-vasilev/code-to-markdown.git
cd code-to-markdown

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_file_discovery.py -v
```

### Code Quality

```bash
# Format code
black src/ tests/
isort src/ tests/

# Lint code
ruff check src/ tests/
ruff check --fix src/ tests/

# Type checking
mypy src/
```

### Building Executable

```bash
# Build executable
python build.py

# Create release package
python build_release.py
```

## 📁 Project Structure

```
code-to-markdown/
├── src/                    # Source code
│   ├── main.py            # Application entry point
│   ├── ui.py              # Main UI implementation
│   ├── file_discovery.py  # File discovery and filtering
│   ├── md_builder.py      # Markdown generation
│   ├── annotations.py     # AST analysis and annotations
│   ├── worker.py          # Background processing
│   └── ...                # Other modules
├── tests/                 # Test suite
├── docs/                  # Documentation
├── .github/               # GitHub workflows and templates
├── CHANGELOG.md           # Version history
├── CONTRIBUTING.md        # Contribution guidelines
├── SECURITY.md            # Security policy
├── CODE_OF_CONDUCT.md     # Code of conduct
└── README.md              # This file
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Workflow

- Use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages
- Follow the existing code style and patterns
- Add tests for new features
- Update documentation as needed

## 🐛 Bug Reports & Feature Requests

- **Bug Reports**: Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md)
- **Feature Requests**: Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.md)
- **Questions**: Use the [Question template](.github/ISSUE_TEMPLATE/question.md)

## 🛡️ Security

If you discover a security vulnerability, please report it privately:
- Email: [security@example.com](mailto:security@example.com)
- GitHub: [Security Advisories](https://github.com/kirill-vasilev/code-to-markdown/security/advisories)

See our [Security Policy](SECURITY.md) for more details.

## 📈 Roadmap

- [ ] **Dark Theme** - Dark mode support for the UI
- [ ] **Plugin System** - Extensible architecture for custom processors
- [ ] **Export Formats** - Support for HTML, PDF, and other formats
- [ ] **Cloud Integration** - Direct publishing to GitHub Pages, GitBook, etc.
- [ ] **Advanced Filtering** - Custom file inclusion/exclusion rules
- [ ] **Collaborative Features** - Team documentation workflows

See our [Issues](https://github.com/kirill-vasilev/code-to-markdown/issues) for more planned features.

## 📊 Performance

Code to Markdown is optimized for performance:

- **Large Projects**: Handles 5000+ files efficiently
- **Memory Usage**: Streams processing to minimize memory footprint
- **Speed**: 6-10x faster than previous versions on large projects
- **Responsiveness**: Non-blocking UI with background processing

## 🏆 Acknowledgments

- Built with [PySide6](https://pypi.org/project/PySide6/) - Modern Qt bindings for Python
- Uses [pathspec](https://pypi.org/project/pathspec/) for .gitignore support
- Code quality maintained with [ruff](https://pypi.org/project/ruff/) and [black](https://pypi.org/project/black/)
- Testing powered by [pytest](https://pypi.org/project/pytest/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Documentation**: [Wiki](https://github.com/kirill-vasilev/code-to-markdown/wiki)
- **Issues**: [GitHub Issues](https://github.com/kirill-vasilev/code-to-markdown/issues)
- **Discussions**: [GitHub Discussions](https://github.com/kirill-vasilev/code-to-markdown/discussions)

---

**Code to Markdown** - Transform your code into beautiful documentation! 📚✨

Made with ❤️ by [Kirill Vasilev](https://github.com/kirill-vasilev)
