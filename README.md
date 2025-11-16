# 🔒 Python Sandbox Executor

[![Tests](https://github.com/dinhhungitsoft/secure-python-sandbox/actions/workflows/tests.yml/badge.svg)](https://github.com/dinhhungitsoft/secure-python-sandbox/actions/workflows/tests.yml)
[![Build](https://github.com/dinhhungitsoft/secure-python-sandbox/actions/workflows/build.yml/badge.svg)](https://github.com/dinhhungitsoft/secure-python-sandbox/actions/workflows/build.yml)
[![PyPI version](https://badge.fury.io/py/sandbox-executor.svg)](https://badge.fury.io/py/sandbox-executor)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A secure Python code execution library with **dual-mode architecture**: run code locally for fast development or connect to a remote API server for production workloads. Perfect for AI agents, code playgrounds, and educational platforms.

## ✨ Key Features

- 🏠 **Local Execution**: Direct subprocess execution for fast iteration and debugging
- 🌐 **Remote Execution**: HTTP client for connecting to sandbox API servers
- 🔄 **Unified Interface**: Same API works for both local and remote modes
- 🤖 **AI Agent Ready**: Easy integration with LangChain, AutoGen, and custom agents
- **Multi-layered Security**: AST validation, resource limits, network control
- 📁 **File I/O Support**: Upload input files and retrieve output files
- ⚡ **Platform Agnostic**: Works on Linux, Windows, macOS, Docker, Kubernetes, and serverless

## 🚀 Quick Start

### Mode 1: Local Execution (Development)

**Best for**: Development, debugging, fast iteration, local AI agents

**How it works**: Executes code directly on your machine using subprocess isolation

**Installation**:
```bash
pip install sandbox-executor
```

**Example**:
```python
from sandbox_executor import SandboxClient

# Create client without server_url = local execution
client = SandboxClient()

code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = [fibonacci(i) for i in range(10)]
print("Fibonacci:", result)
"""

result = client.execute(code)
print(result.stdout)
# Output: Fibonacci: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

**Advantages**:
- ⚡ **Fastest**: No network overhead
- 🐛 **Easy debugging**: Direct execution with full error messages
- 🔧 **Simple setup**: No server required
- 💻 **Offline capable**: Works without internet

**Use cases**:
- Local development and testing
- AI agent prototyping
- Educational tools
- Code snippets execution
- Quick scripts and automation

---

### Mode 2: Remote Execution (Production)

**Best for**: Production, scaling, untrusted code, multi-tenant systems

**How it works**: Sends code to a remote API server via HTTP requests

**Installation**:
**Step 1**: Run Sandbox server (on docker or K8s cluster)
```bash
git clone https://github.com/dinhhungitsoft/secure-python-sandbox
cd secure-python-sandbox
# Run API server on docker
docker-compose up # Serving at http://localhost:8000
```
**Step 2**: Install the client library in your main project
```bash
pip install sandbox-executor
```

**Step 3**: Initialize the sandbox client with the Sandbox server endpoint
```python
from sandbox_executor import SandboxClient

# Create client with server_url = remote execution
client = SandboxClient(
    server_url="http://localhost:8000",
    timeout=30
)

code = """
import math

radius = 5
area = math.pi * radius ** 2
print(f"Circle area: {area:.2f}")
"""

result = client.execute(code)
print(result.stdout)
# Output: Circle area: 78.54
```

**Advantages**:
- 🔒 **Enhanced security**: Code runs in isolated containers
- 📈 **Scalable**: Handle multiple concurrent executions
- 🌐 **Distributed**: Execute code on powerful remote machines
- 🛡️ **Better isolation**: Full container-level isolation

**Use cases**:
- Production AI agents
- Multi-tenant code execution platforms
- Online code playgrounds
- Serverless functions
- Educational platforms with many users

**🔐 Notes for Maximum Security Deployment**: For the highest level of isolation and security, deploy the sandbox API on a Kubernetes cluster with [Kata Containers](https://katacontainers.io/) runtime. Kata Containers provide lightweight VMs that offer hardware-level isolation while maintaining container compatibility, making them ideal for executing untrusted code in multi-tenant environments.

---

## Configuration

### Environment Variables

Create a `.env` file:
```bash
SANDBOX_MODE=secure
SANDBOX_TIMEOUT=30
SANDBOX_ALLOW_NETWORK=false
```

Load automatically:
```python
client = SandboxClient.from_env()
```

## Advanced Examples

### Working with attached files

```python
from sandbox_executor import SandboxClient

client = SandboxClient()

# Provide input files
input_files = {
    "data.csv": b"id,value\n1,100\n2,200\n3,300\n"
}

code = """
import csv

# Read CSV
with open('data.csv', 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Calculate total
total = sum(int(row['value']) for row in data)
print(f"Total: {total}")

# Write output
with open('result.txt', 'w') as f:
    f.write(f"Sum: {total}\\n")
"""

result = client.execute(code, input_files=input_files)
print(result.stdout)  # Total: 600

# Get output file
output = result.get_file_content('result.txt')
print(output.decode())  # Sum: 600
```

### API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs

### API Endpoints

#### `GET /` - Health Check
```bash
curl http://localhost:8000/
```

#### `POST /execute` - Execute Code
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "print(\"Hello, World!\")",
    "timeout": 30,
    "allow_network": false
  }'
```

## 🏗️ Architecture

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

### Execution Modes

**Secure Mode (Default)**:
- AST validation and restricted imports
- Resource limits (CPU, memory, processes)
- Filesystem isolation with temporary directories
- Network blocking (configurable)
- Execution timeout enforcement

**Simple Mode**:
- Basic subprocess isolation
- Timeout and output limits
- Suitable for trusted code

## 📚 Examples

See the [`examples/`](./examples/) directory for complete examples:

- **`basic_usage.py`** - Basic execution patterns
- **`client_usage.py`** - Local vs Remote client usage  
- **`agent_integration.py`** - AI agent integration examples
- **`with_files.py`** - Working with input/output files
- **`security_tests.py`** - Security feature demonstrations

Run examples:
```bash
python examples/basic_usage.py
python examples/client_usage.py
python examples/agent_integration.py
```

## ⚙️ Configuration

### Environment Variables

Configure the sandbox behavior using environment variables (in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `SANDBOX_MODE` | `secure` | Execution mode: `secure` or `simple` |
| `SANDBOX_TIMEOUT` | `30` | Default execution timeout (seconds) |
| `SANDBOX_ALLOW_NETWORK` | `false` | Allow network access by default |

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

## 🧪 Testing

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_sandbox_executor.py
```

See [`tests/README.md`](./tests/README.md) for detailed testing documentation.

## Cloud Platforms

The sandbox is compatible with:
- **AWS Fargate**: Deploy as ECS task
- **Azure Container Apps**: Deploy as container app
- **Azure Kubernetes Service with Kata runtime**: For more isolation, learn more at 
https://learn.microsoft.com/en-us/azure/aks/use-pod-sandboxing
- **Google Cloud Run**: Deploy as Cloud Run service
- **Heroku**: Deploy as Docker container
- **DigitalOcean App Platform**: Deploy as Docker app

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/dinhhungitsoft/secure-python-sandbox/issues)
- **Examples**: Check the [examples/](./examples/) directory

## ⭐ Star History

If you find this project useful, please give it a star! ⭐

---

**Made with ❤️ for the Python & AI community**

**⚠️ Security Note**: While this sandbox provides multiple layers of security, no sandbox is 100% foolproof. Always run in isolated environments and implement additional security measures for production use with untrusted code.