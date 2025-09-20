# Contributing to Code to Markdown

Thank you for your interest in contributing to Code to Markdown! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Process](#contributing-process)
- [Coding Standards](#coding-standards)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature or bugfix
4. Make your changes
5. Test your changes
6. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Git
- A code editor (VS Code recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kirill-vasilev/code-to-markdown.git
   cd code-to-markdown
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   pip install -e ".[dev]"
   ```

4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_file_discovery.py

# Run tests with verbose output
pytest -v
```

### Running the Application

```bash
# Run from source
python -m src.main

# Or use the runner script
python run.py
```

## Contributing Process

### Branch Naming

Use descriptive branch names with prefixes:

- `feature/description` - New features
- `fix/description` - Bug fixes
- `chore/description` - Maintenance tasks
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

Examples:
- `feature/add-dark-theme`
- `fix/memory-leak-in-file-processing`
- `chore/update-dependencies`

### Commit Message Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### Types

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools

#### Examples

```
feat(ui): add dark theme support
fix(discovery): resolve memory leak in large projects
docs(readme): update installation instructions
test(annotations): add tests for Python AST analysis
chore(deps): update PySide6 to 6.9.2
```

### Pull Request Process

1. **Create a Pull Request**
   - Use a descriptive title
   - Reference any related issues
   - Provide a clear description of changes

2. **PR Template**
   - Fill out all sections in the PR template
   - Include screenshots for UI changes
   - Add test coverage information

3. **Review Process**
   - All PRs require review
   - Address feedback promptly
   - Keep PRs focused and reasonably sized

4. **Merge Requirements**
   - All tests must pass
   - Code must be reviewed and approved
   - No merge conflicts
   - Up-to-date with main branch

## Coding Standards

### Python Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for all public functions
- Keep functions small and focused
- Use meaningful variable names

### Code Formatting

We use automated formatting tools:

```bash
# Format code
black src/ tests/
isort src/ tests/

# Lint code
ruff check src/ tests/
ruff check --fix src/ tests/
```

### Testing

- Write tests for new features
- Maintain test coverage above 80%
- Use descriptive test names
- Test edge cases and error conditions

### Documentation

- Update README.md for user-facing changes
- Add docstrings for new functions
- Update CHANGELOG.md for significant changes
- Include examples in docstrings

## Issue Guidelines

### Bug Reports

When reporting bugs, please include:

1. **Clear description** of the bug
2. **Steps to reproduce** the issue
3. **Expected behavior** vs actual behavior
4. **Environment details** (OS, Python version, etc.)
5. **Screenshots** if applicable
6. **Log files** if available

### Feature Requests

When requesting features, please include:

1. **Clear description** of the feature
2. **Use case** and motivation
3. **Proposed solution** (if you have one)
4. **Alternatives** considered
5. **Additional context** or screenshots

### Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements or additions to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `question`: Further information is requested

## Getting Help

- Check existing issues and discussions
- Join our community discussions
- Create a new issue with the appropriate template
- Contact maintainers for urgent issues

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing to Code to Markdown! 🎉
