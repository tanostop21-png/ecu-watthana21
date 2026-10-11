# Contributing to ECU-Watthana21

Thank you for your interest in contributing to ECU-Watthana21! Here are some guidelines to help you get started.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## How to Contribute

### Reporting Bugs

1. Check if the issue already exists
2. Create a clear bug report with:
   - Description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version, etc.)

### Suggesting Features

1. Check existing issues first
2. Clearly describe the feature
3. Explain the use case and benefits
4. Provide examples if possible

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes with clear commits
4. Add tests for new functionality
5. Update documentation as needed
6. Submit a pull request with a clear description

## Development Setup

1. Clone your fork: `git clone https://github.com/your-username/ecu-watthana21.git`
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Install dev dependencies: `pip install pytest pytest-cov`

## Testing

- Write tests for new features
- Run tests before submitting PR: `pytest tests/`
- Ensure code coverage remains good: `pytest --cov=. tests/`

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small

## Commit Messages

- Use clear, descriptive commit messages
- Start with a verb: "Add", "Fix", "Update", etc.
- Keep first line under 50 characters
- Add detailed description if needed

## Documentation

- Update README.md for major changes
- Add docstrings for new functions
- Update API.md for API changes
- Include examples for new features

## Review Process

- Be open to feedback and suggestions
- Respond to review comments promptly
- Make requested changes in separate commits
- Don't hesitate to ask questions

## Questions?

Feel free to open an issue or discussion for any questions about contributing.

Happy coding! 🚀
