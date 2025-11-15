# py-applescript Roadmap

This document outlines potential improvements and feature additions for py-applescript. Items are organized by category and priority.

## Current Status (v1.0.3)

The library is production-stable and provides core functionality for Python-AppleScript interoperability. The following roadmap identifies opportunities for enhancement while maintaining backward compatibility and the library's lightweight philosophy.

---

## High Priority Improvements

### 1. Testing Infrastructure

**Status**: Missing
**Impact**: High
**Effort**: Medium

- Add comprehensive unit test suite
- Implement integration tests for common AppleScript scenarios
- Add CI/CD pipeline (GitHub Actions) for automated testing
- Test coverage across Python versions (2.7, 3.6+)
- Test on multiple macOS versions

**Benefits**:
- Catch regressions early
- Ensure compatibility across versions
- Enable confident refactoring
- Provide usage examples through tests

### 2. Enhanced Documentation

**Status**: Basic documentation exists
**Impact**: High
**Effort**: Low-Medium

- Add comprehensive API reference with all parameters
- Create tutorial series for common use cases
- Add cookbook with real-world examples
- Document common pitfalls and solutions
- Add type hints (Python 3.5+) with stub files for better IDE support
- Create interactive Jupyter notebooks demonstrating features

**Examples needed**:
- Controlling iTunes/Music.app
- File system operations
- UI automation
- Inter-application communication
- Working with Safari, Finder, etc.

### 3. Better Error Messages

**Status**: Basic error reporting
**Impact**: Medium-High
**Effort**: Low

- Enhance ScriptError with more context
- Add suggestions for common errors
- Improve error messages for type conversion failures
- Add debug mode with verbose logging
- Include script line numbers in all error messages

**Example**:
```python
# Current: "Can't pack data into an AEDesc (unsupported type)"
# Improved: "Cannot convert Python object of type 'MyClass' to AppleScript type.
#            Supported types: bool, int, float, str, list, dict, datetime.
#            Consider converting to a supported type first."
```

---

## Medium Priority Enhancements

### 4. Performance Optimizations

**Status**: Not optimized
**Impact**: Medium
**Effort**: Medium

- Profile and optimize type conversion (pack/unpack)
- Cache compiled scripts more efficiently
- Optimize repeated handler calls
- Benchmark against raw NSAppleScript usage
- Add lazy evaluation where possible

**Metrics to track**:
- Script compilation time
- Handler execution time
- Type conversion overhead
- Memory usage for long-running scripts

### 5. Extended Type Support

**Status**: Core types supported
**Impact**: Medium
**Effort**: Medium-High

**Additional type mappings**:
- Python pathlib.Path ↔ AppleScript file objects
- Python Decimal ↔ AppleScript currency/decimal
- Python sets ↔ AppleScript lists (with uniqueness)
- Python OrderedDict ↔ AppleScript record (preserving order)
- Better timezone support for datetime objects
- Support for AppleScript's 'duration' type

**Advanced features**:
- Object specifier creation from Python (e.g., "document 1 of application 'Safari'")
- Application-specific terminology dictionaries
- Automatic SDEF parsing for type-safe app scripting

### 6. Async/Concurrent Execution

**Status**: Synchronous only
**Impact**: Medium
**Effort**: High

- Add async/await support (Python 3.5+)
- Support for concurrent script execution
- Thread-safe script instances
- Non-blocking handler calls
- Event-driven script monitoring

**Use cases**:
- Long-running AppleScript operations
- Multiple parallel automation tasks
- Responsive GUI applications using AppleScript
- Background script execution

### 7. Script Management Features

**Status**: Basic script lifecycle
**Impact**: Low-Medium
**Effort**: Low-Medium

- Save compiled scripts to disk (.scpt format)
- Script templates and parameterization
- Script versioning and caching
- Hot-reload for script development
- Script dependency management

**Example**:
```python
# Template scripts with parameters
template = applescript.ScriptTemplate('''
on processFile(filePath, action)
    -- template logic
end processFile
''')
script = template.instantiate(timeout=30, debug=True)
```

---

## Low Priority / Future Enhancements

### 8. Advanced AppleScript Features

**Status**: Not implemented
**Impact**: Low-Medium
**Effort**: High

- Script debugger integration
- Breakpoint support
- Variable inspection
- Step-through execution
- Profiling AppleScript code from Python

### 9. Developer Tools

**Status**: Missing
**Impact**: Low
**Effort**: Low-Medium

- Interactive REPL for AppleScript experimentation
- Script linter and syntax checker
- Type checker for AppleScript code
- Code formatter
- Migration tool from osascript/appscript

**Example**:
```bash
$ python -m applescript repl
AppleScript REPL (Python 3.9.1)
>>> say "Hello"
None
>>> return 42
42
```

### 10. Enhanced PyObjC Integration

**Status**: Basic usage
**Impact**: Low
**Effort**: Medium

- Better integration with NSAppleEventDescriptor features
- Support for custom descriptor types
- Direct access to AE Manager when needed
- Coercion handlers for custom types

### 11. Cross-Platform Considerations

**Status**: macOS only (by design)
**Impact**: Low
**Effort**: Very High

While AppleScript is macOS-only, consider:
- Mock/stub implementation for testing on other platforms
- Documentation for cross-platform alternatives
- Abstract interface that could support JXA (JavaScript for Automation)
- Graceful degradation on non-macOS systems

### 12. Distribution Improvements

**Status**: Basic PyPI package
**Impact**: Low-Medium
**Effort**: Low

- Publish to PyPI with automated releases
- Add wheel distribution
- Conda package for conda-forge
- Pre-built binaries for common configurations
- Better dependency management (poetry/pipenv support)
- Add to Homebrew (brew install py-applescript)

---

## Python 2.7 Deprecation Strategy

**Timeline**: Consider for v2.0.0

Python 2.7 reached end-of-life in January 2020. Consider:

1. **Short term** (v1.x): Maintain compatibility
2. **Medium term** (v1.5+): Add deprecation warnings
3. **Long term** (v2.0+): Drop Python 2.7, embrace Python 3 features

**Benefits of dropping Python 2.7**:
- Native type hints
- Better string/bytes handling
- Async/await support
- f-strings and other syntax improvements
- Simplified codebase

---

## Migration Paths

### From osascript

Provide migration guide and conversion tools for users coming from `osascript` CLI tool.

### From appscript

Document migration path for legacy appscript users, highlighting improvements and changes.

### From Scripting Bridge

Compare and contrast with Apple's Scripting Bridge, showing when to use each.

---

## Community & Ecosystem

### Documentation Ecosystem

- Wiki with community examples
- Video tutorials
- Blog posts and articles
- Integration examples with popular libraries (requests, pandas, etc.)

### Related Tools

- Integration with automation frameworks
- Bridge to other scripting languages
- AppleScript library repository
- Shared script collection

---

## Non-Goals

To maintain focus and simplicity, the following are explicitly **not** planned:

1. **GUI builder for AppleScript** - Keep library focused on programmatic use
2. **AppleScript language redesign** - Work with AppleScript as-is
3. **Complete OSA API wrapper** - Stick to NSAppleScript subset for reliability
4. **Application-specific libraries** - Keep generic; let users build app-specific tools
5. **Visual scripting interface** - Command-line and programmatic only

---

## How to Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to help with any of these items.

### Quick Start Areas

Good first contributions:
- Add examples to documentation
- Write unit tests for existing features
- Improve error messages
- Add type hints
- Create tutorial notebooks

### Contact

- GitHub Issues: Feature requests and bug reports
- Pull Requests: Code contributions welcome
- Discussions: Architecture and design questions

---

## Version Planning

### v1.1.0 (Next Minor Release)
- Add test suite
- Improve error messages
- Add type hints
- Enhanced documentation

### v1.2.0
- Performance optimizations
- Additional type mappings
- Better script management

### v2.0.0 (Major Release)
- Drop Python 2.7 support
- Async/await support
- Breaking API improvements
- Modern Python 3 features

---

*Last Updated: 2025-11-15*

*This roadmap is a living document and will evolve based on community feedback and contributions.*
