# Python Code Sandbox - Testing Guide

## Test Suite Overview

Comprehensive unit tests covering all major components of the Python Code Sandbox.

## Test Structure

```
tests/
├── __init__.py                    # Test package initialization
├── run_tests.py                   # Test runner script
├── test_executor_factory.py       # ExecutorFactory tests
├── test_sandbox_executor.py       # SandboxExecutor tests
├── test_secure_executor.py        # SecureSandboxExecutor tests
├── test_api.py                    # FastAPI endpoint tests
└── test_integration.py            # Integration tests
```

## Test Coverage

### 1. ExecutorFactory Tests (`test_executor_factory.py`)
- ✅ Creating secure executor
- ✅ Creating simple executor
- ✅ Case-insensitive mode selection
- ✅ Invalid mode error handling
- ✅ Fallback mechanism
- ✅ Custom configuration parameters

### 2. SandboxExecutor Tests (`test_sandbox_executor.py`)
- ✅ Simple print statements
- ✅ Multiple print statements
- ✅ Basic calculations
- ✅ Error handling (division by zero)
- ✅ Syntax error handling
- ✅ Timeout enforcement
- ✅ Reading input files
- ✅ Writing output files
- ✅ Multiple file operations
- ✅ Standard library imports
- ✅ Configuration options

### 3. SecureSandboxExecutor Tests (`test_secure_executor.py`)
- ✅ Simple execution
- ✅ Safe module imports (math, json, random)
- ✅ Dangerous import blocking (os, sys, subprocess)
- ✅ File operations
- ✅ Timeout enforcement
- ✅ Error handling
- ✅ Memory limit configuration
- ✅ Network blocking
- ✅ AST validation
- ✅ Multiple output files

### 4. API Tests (`test_api.py`)
- ✅ Root endpoint health check
- ✅ Health check endpoint
- ✅ Simple code execution
- ✅ Code with calculations
- ✅ Error handling
- ✅ Custom timeout parameter
- ✅ File upload/download
- ✅ Invalid base64 handling
- ✅ Network flag parameter
- ✅ Timeout validation (range 1-300)
- ✅ Missing required parameters
- ✅ Multipart form data
- ✅ Input validation

### 5. Integration Tests (`test_integration.py`)
- ✅ End-to-end secure mode execution
- ✅ End-to-end simple mode execution
- ✅ File processing pipeline
- ✅ Error recovery
- ✅ Execution isolation
- ✅ Factory fallback mechanism
- ✅ Performance tests
- ✅ Output size handling

## Running Tests

### Option 1: Using unittest (default)

Run all tests:
```bash
python tests/run_tests.py
```

Run specific test module:
```bash
python tests/run_tests.py test_api.TestAPIEndpoints
```

Run individual test:
```bash
python -m unittest tests.test_api.TestAPIEndpoints.test_root_endpoint
```

### Option 2: Using pytest (recommended)

Install pytest dependencies:
```bash
pip install pytest pytest-cov pytest-asyncio httpx
```

Run all tests with coverage:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_api.py
```

Run specific test:
```bash
pytest tests/test_api.py::TestAPIEndpoints::test_root_endpoint
```

Run with verbose output:
```bash
pytest -v
```

Run with coverage report:
```bash
pytest --cov=src --cov-report=html
```

### Option 3: Individual test files

Each test file can be run independently:
```bash
python tests/test_executor_factory.py
python tests/test_sandbox_executor.py
python tests/test_secure_executor.py
python tests/test_api.py
python tests/test_integration.py
```

## Test Output

### Successful Test Run
```
test_create_secure_executor (test_executor_factory.TestExecutorFactory) ... ok
test_create_simple_executor (test_executor_factory.TestExecutorFactory) ... ok
test_execute_simple_code (test_api.TestAPIEndpoints) ... ok
...
----------------------------------------------------------------------
Ran 50 tests in 5.234s

OK
```

### Failed Test Example
```
FAIL: test_timeout_enforcement (test_sandbox_executor.TestSandboxExecutor)
----------------------------------------------------------------------
Traceback (most recent call last):
  ...
AssertionError: Expected timeout but got return_code 0
```

## Coverage Report

Generate HTML coverage report:
```bash
pytest --cov=src --cov-report=html
```

View report:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## Writing New Tests

### Test Naming Convention
- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`

### Example Test Template

```python
import unittest
from src.your_module import YourClass

class TestYourClass(unittest.TestCase):
    """Test cases for YourClass"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.instance = YourClass()
    
    def test_something(self):
        """Test description"""
        result = self.instance.method()
        self.assertEqual(result, expected_value)
    
    def tearDown(self):
        """Clean up after tests"""
        pass
```

## Best Practices

1. **Isolation**: Each test should be independent
2. **Descriptive names**: Use clear test method names
3. **Single assertion**: Test one thing at a time (when possible)
4. **Setup/Teardown**: Use setUp/tearDown for common initialization
5. **Mock external dependencies**: Use mocks for external services
6. **Fast tests**: Keep tests quick (< 1 second per test)
7. **Readable**: Write tests that serve as documentation

## Debugging Tests

### Run with debug output
```bash
pytest -vv -s
```

### Stop on first failure
```bash
pytest -x
```

### Run last failed tests only
```bash
pytest --lf
```

### Use pdb debugger
```bash
pytest --pdb
```

## Common Issues

### Import Errors
Make sure project root is in PYTHONPATH:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Timeout Tests Failing
Increase timeout values in tests if system is slow:
```python
executor = SandboxExecutor(timeout=10)  # Instead of 2
```

### File Permission Errors
Ensure temp directories have proper permissions:
```bash
chmod -R 755 /tmp
```

## Test Metrics

Target metrics:
- **Coverage**: > 80%
- **Test count**: > 50 tests
- **Pass rate**: 100%
- **Execution time**: < 30 seconds

## Contributing Tests

When contributing new features:
1. Write tests first (TDD approach)
2. Ensure all existing tests pass
3. Add integration tests for new features
4. Update this README with new test descriptions
5. Maintain coverage above 80%

## Resources

- [unittest documentation](https://docs.python.org/3/library/unittest.html)
- [pytest documentation](https://docs.pytest.org/)
- [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Coverage.py documentation](https://coverage.readthedocs.io/)
