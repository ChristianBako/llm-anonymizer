# Contributing to LLM Anonymizer

Thank you for your interest in contributing! This guide will help you get started.

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ChristianBako/LLM-Anonymizer-.git
   cd LLM-Anonymizer-
   ```

2. **Install UV** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   ```

4. **Install Ollama and a model**:
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Start Ollama
   ollama serve
   
   # Install a model (in another terminal)
   ollama pull llama3.2
   ```

## Running the Tool

During development, use:
```bash
uv run python -m llm_anon.cli --help
```

## Testing

Test with the provided examples:
```bash
# Basic test
uv run python -m llm_anon.cli examples/test_example.py

# Test validation system
uv run python -m llm_anon.cli examples/lamasoft_example.py --validation-config examples/banned_strings.txt -v
```

## Code Structure

```
llm_anon/
├── __init__.py          # Package initialization
├── cli.py              # Command-line interface
├── types.py            # Type definitions and data classes
├── file_processor.py   # File reading and language detection
├── anonymizer.py       # Core anonymization logic
└── validator.py        # Validation and banned string detection
```

## Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the existing code style

3. **Test thoroughly** with the examples

4. **Update documentation** if needed

5. **Commit with descriptive messages**:
   ```bash
   git commit -m "Add feature: brief description"
   ```

## Adding New Features

### Adding Language Support

1. Update `LANGUAGE_EXTENSIONS` in `file_processor.py`
2. Add test files to `examples/`
3. Update README language list

### Improving Anonymization

1. Modify prompts in `anonymizer.py`
2. Test with various code patterns
3. Ensure validation still works

### Enhancing Validation

1. Update `validator.py` for new detection patterns
2. Add test cases in `examples/`

## Code Style

- Use type hints consistently
- Follow existing naming conventions
- Add docstrings for new functions/classes
- Keep functions focused and small

## Submitting Changes

1. **Push your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** on GitHub

3. **Describe your changes** and why they're needed

4. **Link any related issues**

## Reporting Issues

When reporting bugs or requesting features:

1. **Use the GitHub issue tracker**
2. **Provide clear reproduction steps**
3. **Include your environment details** (OS, Python version, Ollama version)
4. **Share example code** that demonstrates the issue

## Questions?

Feel free to open an issue for questions or start a discussion on GitHub!