"""
Simple example: Execute Python code
"""
import requests
import json

# Sandbox API URL
API_URL = "http://localhost:8000"

def simple_hello_world():
    """Execute simple code to print Hello World"""
    print("=" * 50)
    print("Example 1: Simple Hello World")
    print("=" * 50)
    
    payload = {
        "code": "print('Hello from Python Sandbox!')",
        "timeout": 10
    }
    
    response = requests.post(f"{API_URL}/execute", json=payload)
    result = response.json()
    
    print("STDOUT:", result["stdout"])
    print("STDERR:", result["stderr"])
    print("Return Code:", result["return_code"])
    print()


def with_variables():
    """Execute code with variables and calculations"""
    print("=" * 50)
    print("Example 2: Variables and Calculations")
    print("=" * 50)
    
    code = """
# Calculations
a = 10
b = 20
c = a + b

print(f"a = {a}")
print(f"b = {b}")
print(f"a + b = {c}")

# List operations
numbers = [1, 2, 3, 4, 5]
total = sum(numbers)
print(f"Sum of {numbers} = {total}")
"""
    
    payload = {
        "code": code,
        "timeout": 10
    }
    
    response = requests.post(f"{API_URL}/execute", json=payload)
    result = response.json()
    
    print("STDOUT:")
    print(result["stdout"])
    print()


def with_error():
    """Execute code with error to test error handling"""
    print("=" * 50)
    print("Example 3: Code with Error")
    print("=" * 50)
    
    code = """
# This will cause an error
print("Before error")
x = 1 / 0  # Division by zero
print("After error")  # This won't execute
"""
    
    payload = {
        "code": code,
        "timeout": 10
    }
    
    response = requests.post(f"{API_URL}/execute", json=payload)
    result = response.json()
    
    print("STDOUT:", result["stdout"])
    print("STDERR:", result["stderr"])
    print("Return Code:", result["return_code"])
    print()


def with_imports():
    """Execute code using standard library"""
    print("=" * 50)
    print("Example 4: Using Standard Library")
    print("=" * 50)
    
    code = """
import json
import math
from datetime import datetime

# JSON operations
data = {"name": "Python Sandbox", "version": "1.0"}
print("JSON:", json.dumps(data, indent=2))

# Math operations
print(f"\\nPi = {math.pi:.4f}")
print(f"Square root of 16 = {math.sqrt(16)}")

# DateTime
now = datetime.now()
print(f"\\nCurrent time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
"""
    
    payload = {
        "code": code,
        "timeout": 10
    }
    
    response = requests.post(f"{API_URL}/execute", json=payload)
    result = response.json()
    
    print("STDOUT:")
    print(result["stdout"])
    print()


if __name__ == "__main__":
    # Check if API is running
    try:
        response = requests.get(f"{API_URL}/")
        print(f"✅ API is running: {response.json()}\n")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to API. Make sure the sandbox is running.")
        print("Run: docker-compose up -d")
        exit(1)
    
    # Run examples
    simple_hello_world()
    with_variables()
    with_error()
    with_imports()
    
    print("✅ All examples completed!")
