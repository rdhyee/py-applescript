# Contributing to py-applescript

Thank you for your interest in contributing to py-applescript! This document provides guidelines and information for contributors.

## Project Overview

py-applescript is a Python wrapper for NSAppleScript that enables Python scripts to communicate with AppleScripts and AppleScriptable applications on macOS. The library provides a clean, Pythonic interface while avoiding dependencies on legacy frameworks.

## Development Setup

### Prerequisites

- macOS (required for AppleScript support)
- Python 2.7.x or Python 3.x
- PyObjC framework

### Installation for Development

1. Clone the repository:
```bash
git clone https://github.com/rdhyee/py-applescript.git
cd py-applescript
```

2. Install in development mode:
```bash
python setup.py develop
# or for Python 3
python3 setup.py develop
```

3. Install dependencies:
```bash
pip install pyobjc-core pyobjc-framework-AppleScriptKit pyobjc-framework-AppleScriptObjC
```

## Project Structure

```
py-applescript/
├── applescript/
│   ├── __init__.py      # Main AppleScript and ScriptError classes
│   ├── aecodecs.py      # Type conversion between Python and AppleScript
│   └── kae.py           # Auto-generated AE constants from OS X headers
├── setup.py             # Package configuration
├── README.md            # User documentation
└── LICENSE              # CC0 1.0 Universal (Public Domain)
```

## Code Architecture

### Core Components

1. **AppleScript class** (`applescript/__init__.py`)
   - Manages compiled AppleScript instances
   - Provides `run()` and `call()` methods for script execution
   - Maintains script state between calls

2. **Codecs system** (`applescript/aecodecs.py`)
   - Handles bidirectional type conversion
   - Extensible encoder/decoder architecture
   - Maps Python types to AppleScript equivalents

3. **AE Constants** (`applescript/kae.py`)
   - Four-character codes for AppleScript types and events
   - Auto-generated from macOS headers

### Type Conversion Flow

```
Python value → Codecs.pack() → NSAppleEventDescriptor → AppleScript
AppleScript → NSAppleEventDescriptor → Codecs.unpack() → Python value
```

## How to Contribute

### Reporting Issues

When reporting bugs, please include:
- Python version (2.7 or 3.x)
- macOS version
- PyObjC version
- Minimal code to reproduce the issue
- Expected vs. actual behavior
- Full error traceback

### Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit with clear messages
6. Push to your fork
7. Submit a pull request

### Coding Standards

- Follow PEP 8 style guidelines
- Maintain Python 2.7 and 3.x compatibility
- Add docstrings for all public methods and classes
- Keep code simple and readable
- Avoid external dependencies beyond PyObjC

### Testing Guidelines

Since this library interacts with macOS-specific frameworks:

1. **Manual Testing**: Test on actual macOS systems
2. **Version Testing**: Verify compatibility with Python 2.7 and 3.x
3. **Edge Cases**: Test with various AppleScript features
   - Multiple data types
   - Error conditions
   - State persistence
   - User-defined handlers

### Example Test Scenarios

```python
# Test basic execution
import applescript
scpt = applescript.AppleScript('return 42')
assert scpt.run() == 42

# Test type conversions
scpt = applescript.AppleScript('''
on run {lst}
    return lst
end run
''')
result = scpt.run([1, 2, 3])
assert result == [1, 2, 3]

# Test state persistence
scpt = applescript.AppleScript('''
property counter : 0
on increment()
    set counter to counter + 1
    return counter
end increment
''')
assert scpt.call('increment') == 1
assert scpt.call('increment') == 2

# Test error handling
try:
    applescript.AppleScript('invalid syntax')
except applescript.ScriptError as e:
    assert e.number is not None
```

## Areas for Contribution

See [ROADMAP.md](ROADMAP.md) for planned improvements and feature ideas.

Priority areas:
- Enhanced error messages and debugging support
- Additional type mappings
- Performance optimizations
- Documentation improvements
- Example scripts and tutorials

## Code Review Process

Pull requests will be reviewed for:
- Code quality and style
- Backward compatibility
- Documentation completeness
- Testing coverage
- Performance impact

## Questions?

- Open an issue for general questions
- Check existing issues and pull requests
- Review the README.md for usage documentation

## License

By contributing to py-applescript, you agree that your contributions will be licensed under the CC0 1.0 Universal (Public Domain) license, the same license as the project.
