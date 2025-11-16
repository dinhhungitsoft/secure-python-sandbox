# Python Code Sandbox

A secure, platform-agnostic Python code execution API with multi-layered security features. Execute untrusted Python code safely in an isolated environment with resource limits, network restrictions, and filesystem isolation.

## 🌟 Features

- **🔒 Multi-layered Security**: AST validation, restricted imports, sandboxed execution
- **🌐 Platform Agnostic**: Works on Linux, Windows, Mac, Docker, Kubernetes, and serverless platforms (AWS Fargate, Azure Container Apps, Google Cloud Run)
- **⚡ Fast & Lightweight**: Minimal overhead with efficient resource management
- **📁 File I/O Support**: Upload input files and retrieve output files (base64-encoded)
- **🎯 Resource Limits**: CPU, memory, and execution time constraints
- **🚫 Network Control**: Optional network access blocking
- **📊 RESTful API**: Simple HTTP API built with FastAPI
- **🐳 Docker Ready**: Pre-configured Docker and Docker Compose setup

## 🏗️ Architecture

The project uses a **Factory Pattern** with automatic fallback for executor selection:

### Execution Modes

1. **Secure Mode (Default)** - Platform-agnostic multi-layered security:
   - RestrictedPython AST filtering
   - Import whitelist/blacklist
   - Resource limits (CPU, memory, processes)
   - Filesystem isolation with temporary directories
   - Network blocking (optional)
   - Execution timeout enforcement

2. **Simple Mode** - Basic subprocess isolation:
   - Process-level isolation
   - Basic timeout and resource limits
   - Suitable for trusted environments

### Security Layers

```
┌─────────────────────────────────────┐
│   1. AST Validation                 │  Compile-time filtering
├─────────────────────────────────────┤
│   2. Import Restrictions            │  Module whitelist/blacklist
├─────────────────────────────────────┤
│   3. Resource Limits                │  CPU, Memory, Processes
├─────────────────────────────────────┤
│   4. Filesystem Isolation           │  Temporary directory sandbox
├─────────────────────────────────────┤
│   5. Network Blocking               │  Socket monkey-patching
├─────────────────────────────────────┤
│   6. Execution Timeout              │  Hard timeout enforcement
└─────────────────────────────────────┘
```

## 🚀 Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd python_sandbox
   ```

2. **Start the service**:
   ```bash
   docker-compose up -d
   ```

3. **Test the API**:
   ```bash
   curl http://localhost:8000/
   ```

The API will be available at `http://localhost:8000`.

### Manual Setup

1. **Install Python 3.11+**:
   ```bash
   python --version  # Should be 3.11 or higher
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server**:
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```

## 📖 API Documentation

### Endpoints

#### `GET /`
Health check endpoint.

**Response**:
```json
{
  "status": "ok",
  "message": "Python Code Sandbox API is running",
  "version": "1.0.0"
}
```

#### `POST /execute`
Execute Python code in a secure sandbox.

**Request Body**:
```json
{
  "code": "print('Hello, World!')",
  "timeout": 30,
  "allow_network": false,
  "files": {
    "input.txt": "SGVsbG8gV29ybGQ="
  }
}
```

**Parameters**:
- `code` (string, required): Python code to execute
- `timeout` (integer, optional): Execution timeout in seconds (1-300, default: 30)
- `allow_network` (boolean, optional): Allow network access (default: false)
- `files` (object, optional): Input files as base64-encoded strings

**Response**:
```json
{
  "stdout": "Hello, World!\n",
  "stderr": "",
  "return_code": 0,
  "output_files": {
    "output.txt": "SGVsbG8gV29ybGQ="
  }
}
```

**Response Fields**:
- `stdout` (string): Standard output from execution
- `stderr` (string): Standard error from execution
- `return_code` (integer): Process exit code (0 = success)
- `output_files` (object): Output files as base64-encoded strings

### Interactive API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 Usage Examples

### Basic Execution

```python
import requests

response = requests.post('http://localhost:8000/execute', json={
    'code': '''
import math
print(f"Pi = {math.pi}")
print(f"Square root of 16 = {math.sqrt(16)}")
'''
})

result = response.json()
print(result['stdout'])
# Output: 
# Pi = 3.141592653589793
# Square root of 16 = 4.0
```

### Working with Files

```python
import requests
import base64

# Prepare input file
input_data = "Line 1\nLine 2\nLine 3"
input_base64 = base64.b64encode(input_data.encode()).decode()

# Execute code that reads and writes files
response = requests.post('http://localhost:8000/execute', json={
    'code': '''
with open('input.txt', 'r') as f:
    lines = f.readlines()

with open('output.txt', 'w') as f:
    for i, line in enumerate(lines, 1):
        f.write(f"{i}. {line}")
''',
    'files': {
        'input.txt': input_base64
    }
})

# Decode output file
result = response.json()
output_base64 = result['output_files']['output.txt']
output_data = base64.b64decode(output_base64).decode()
print(output_data)
# Output:
# 1. Line 1
# 2. Line 2
# 3. Line 3
```

### Error Handling

```python
import requests

response = requests.post('http://localhost:8000/execute', json={
    'code': 'print(1/0)'  # Division by zero
})

result = response.json()
print(f"Return Code: {result['return_code']}")
print(f"Error: {result['stderr']}")
```

More examples available in the [`examples/`](./examples/) directory.

## ⚙️ Configuration

### Environment Variables

Configure the sandbox behavior using environment variables (in `.env` or `docker-compose.yml`):

| Variable | Default | Description |
|----------|---------|-------------|
| `EXECUTION_MODE` | `secure` | Execution mode: `secure` or `simple` |
| `SANDBOX_TIMEOUT` | `30` | Default execution timeout (seconds) |
| `SANDBOX_ALLOW_NETWORK` | `false` | Allow network access by default |

### Docker Compose Configuration

Edit `docker-compose.yml` to customize:

```yaml
environment:
  - EXECUTION_MODE=secure
  - SANDBOX_TIMEOUT=30
  - SANDBOX_ALLOW_NETWORK=false

deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 512M
```

### Security Configuration

The secure executor includes configurable whitelists and blacklists:

**Safe Modules** (allowed by default):
- `math`, `random`, `datetime`, `json`, `base64`, `hashlib`
- `collections`, `itertools`, `functools`, `re`, `string`
- `decimal`, `fractions`, `statistics`, `uuid`, `secrets`

**Blocked Modules** (always restricted):
- `os`, `sys`, `subprocess`, `multiprocessing`, `threading`
- `socket`, `urllib`, `requests`, `http`, `ftplib`, `smtplib`
- `importlib`, `eval`, `exec`, `compile`

## 🛡️ Security Considerations

### What's Protected

✅ **Import restrictions**: Dangerous modules are blocked  
✅ **Resource limits**: CPU, memory, and process limits enforced  
✅ **Filesystem isolation**: Code runs in temporary directories  
✅ **Network blocking**: Optional socket-level blocking  
✅ **Timeout enforcement**: Hard timeout prevents infinite loops  
✅ **AST validation**: Compile-time code analysis

### What's NOT Protected

⚠️ **DoS attacks**: Malicious code can still consume allowed resources  
⚠️ **Side-channel attacks**: Timing and cache attacks are possible  
⚠️ **Data exfiltration**: If network is enabled, data can be sent out  
⚠️ **Cryptographic operations**: CPU-intensive operations within limits  

### Best Practices

1. **Always use secure mode** in production
2. **Keep network access disabled** unless required
3. **Set appropriate resource limits** based on your use case
4. **Monitor resource usage** and adjust limits accordingly
5. **Run in containers** for additional isolation
6. **Keep dependencies updated** for security patches
7. **Validate user input** before sending to the sandbox
8. **Implement rate limiting** to prevent abuse

## 🧪 Testing

The project includes a comprehensive test suite with 58+ unit tests covering all components.

### Running Tests

```bash
# Run all tests
python tests/run_tests.py

# Run with pytest (recommended)
pip install pytest pytest-cov
pytest

# Run with coverage report
pytest --cov=src --cov-report=html
```

### Test Coverage

- ✅ ExecutorFactory (8 tests)
- ✅ SandboxExecutor (13 tests)
- ✅ SecureSandboxExecutor (12 tests)
- ✅ API Endpoints (17 tests)
- ✅ Integration Tests (8 tests)

See [`tests/README.md`](./tests/README.md) for detailed testing documentation.

## 🔧 Development

### Project Structure

```
python_sandbox/
├── src/
│   ├── main.py                    # FastAPI application
│   ├── executor_factory.py        # Executor factory with fallback
│   └── executors/
│       ├── sandbox_executor.py    # Base executor interface
│       └── secure_sandbox_executor.py  # Secure executor implementation
├── examples/                      # Usage examples
│   ├── simple_execute.py
│   ├── with_files.py
│   ├── with_multipart.py
│   ├── test_network.py
│   ├── test_secure_mode.py
│   └── security_tests.py
├── docker-compose.yml             # Docker Compose configuration
├── Dockerfile                     # Docker image definition
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

### Running Tests

```bash
# Run security tests
python examples/security_tests.py

# Test secure mode
python examples/test_secure_mode.py

# Test network blocking
python examples/test_network.py
```

### Adding New Features

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

## 🚢 Deployment

### Docker

```bash
# Build image
docker build -t python-sandbox .

# Run container
docker run -p 8000:8000 python-sandbox
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: python-sandbox
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: python-sandbox
        image: python-sandbox:latest
        ports:
        - containerPort: 8000
        env:
        - name: EXECUTION_MODE
          value: "secure"
        resources:
          limits:
            cpu: "1"
            memory: "512Mi"
```

### Cloud Platforms

The sandbox is compatible with:
- **AWS Fargate**: Deploy as ECS task
- **Azure Container Apps**: Deploy as container app
- **Google Cloud Run**: Deploy as Cloud Run service
- **Heroku**: Deploy as Docker container
- **DigitalOcean App Platform**: Deploy as Docker app

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📞 Support

- **Documentation**: Check the [examples](./examples/) directory
- **Issues**: Report bugs or request features via GitHub Issues
- **API Docs**: Visit http://localhost:8000/docs when running

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Security inspired by [RestrictedPython](https://github.com/zopefoundation/RestrictedPython)
- Docker containerization for additional isolation

---

**⚠️ Warning**: This sandbox provides multiple layers of security but is not foolproof. Always run in isolated environments and implement additional security measures for production use.
