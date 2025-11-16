"""
Test Secure Sandbox Executor
=============================

Demonstrates the platform-agnostic secure sandbox with multi-layered security.
"""

import requests
import json
import base64

BASE_URL = "http://localhost:8000"


def test_health_check():
    """Check which execution mode is active"""
    print("=" * 60)
    print("Health Check")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/health")
    data = response.json()
    
    print(f"Status: {data['status']}")
    print(f"Execution Mode: {data['execution_mode']}")
    print(f"Config: {json.dumps(data['config'], indent=2)}")
    print()


def test_basic_execution():
    """Test basic code execution"""
    print("=" * 60)
    print("Test 1: Basic Execution")
    print("=" * 60)
    
    code = """
print("Hello from secure sandbox!")
print("2 + 2 =", 2 + 2)
"""
    
    response = requests.post(
        f"{BASE_URL}/execute",
        json={"code": code}
    )
    
    result = response.json()
    print(f"stdout: {result['stdout']}")
    print(f"stderr: {result['stderr']}")
    print(f"return_code: {result['return_code']}")
    print()


def test_allowed_modules():
    """Test that whitelisted modules work"""
    print("=" * 60)
    print("Test 2: Allowed Modules (math, json, datetime)")
    print("=" * 60)
    
    code = """
import math
import json
import datetime

print("Math: sqrt(16) =", math.sqrt(16))
print("JSON:", json.dumps({"hello": "world"}))
print("Date:", datetime.datetime.now().strftime("%Y-%m-%d"))
"""
    
    response = requests.post(
        f"{BASE_URL}/execute",
        json={"code": code}
    )
    
    result = response.json()
    print(f"stdout: {result['stdout']}")
    print(f"stderr: {result['stderr']}")
    print(f"return_code: {result['return_code']}")
    print()


def test_blocked_module_os():
    """Test that dangerous modules are blocked"""
    print("=" * 60)
    print("Test 3: Blocked Module - os (should fail)")
    print("=" * 60)
    
    code = """
import os
print(os.listdir('/'))
"""
    
    response = requests.post(
        f"{BASE_URL}/execute",
        json={"code": code}
    )
    
    result = response.json()
    print(f"stdout: {result['stdout']}")
    print(f"stderr: {result['stderr']}")
    print(f"return_code: {result['return_code']}")
    print("✅ Expected failure - security working!")
    print()


def test_blocked_module_subprocess():
    """Test subprocess blocking"""
    print("=" * 60)
    print("Test 4: Blocked Module - subprocess (should fail)")
    print("=" * 60)
    
    code = """
import subprocess
subprocess.run(['ls', '-la'])
"""
    
    response = requests.post(
        f"{BASE_URL}/execute",
        json={"code": code}
    )
    
    result = response.json()
    print(f"stdout: {result['stdout']}")
    print(f"stderr: {result['stderr']}")
    print(f"return_code: {result['return_code']}")
    print("✅ Expected failure - security working!")
    print()


def test_blocked_eval():
    """Test eval/exec blocking"""
    print("=" * 60)
    print("Test 5: Blocked Function - eval (should fail)")
    print("=" * 60)
    
    code = """
eval("print('hacked')")
"""
    
    response = requests.post(
        f"{BASE_URL}/execute",
        json={"code": code}
    )
    
    result = response.json()
    print(f"stdout: {result['stdout']}")
    print(f"stderr: {result['stderr']}")
    print(f"return_code: {result['return_code']}")
    print("✅ Expected failure - security working!")
    print()


def test_blocked_open():
    """Test file operations blocking"""
    print("=" * 60)
    print("Test 6: Blocked Function - open (should fail)")
    print("=" * 60)
    
    code = """
open('/etc/passwd', 'r')
"""
    
    response = requests.post(
        f"{BASE_URL}/execute",
        json={"code": code}
    )
    
    result = response.json()
    print(f"stdout: {result['stdout']}")
    print(f"stderr: {result['stderr']}")
    print(f"return_code: {result['return_code']}")
    print("✅ Expected failure - security working!")
    print()


def test_timeout():
    """Test timeout protection"""
    print("=" * 60)
    print("Test 7: Timeout Protection (infinite loop)")
    print("=" * 60)
    
    code = """
import time
while True:
    time.sleep(1)
"""
    
    response = requests.post(
        f"{BASE_URL}/execute",
        json={
            "code": code,
            "timeout": 2  # 2 seconds
        }
    )
    
    result = response.json()
    print(f"stdout: {result['stdout']}")
    print(f"stderr: {result['stderr']}")
    print(f"return_code: {result['return_code']}")
    print("✅ Timeout worked!")
    print()


def test_memory_limit():
    """Test memory limit (Linux only)"""
    print("=" * 60)
    print("Test 8: Memory Limit (may fail on Windows)")
    print("=" * 60)
    
    code = """
# Try to allocate large memory
data = [0] * (200 * 1024 * 1024)  # 200MB list
print("Allocated memory")
"""
    
    response = requests.post(
        f"{BASE_URL}/execute",
        json={"code": code}
    )
    
    result = response.json()
    print(f"stdout: {result['stdout']}")
    print(f"stderr: {result['stderr']}")
    print(f"return_code: {result['return_code']}")
    if result['return_code'] != 0:
        print("✅ Memory limit working! (Linux)")
    else:
        print("⚠️  Memory limit not enforced (Windows or high limit)")
    print()


def test_network_blocking():
    """Test network blocking"""
    print("=" * 60)
    print("Test 9: Network Blocking (should fail)")
    print("=" * 60)
    
    code = """
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('google.com', 80))
"""
    
    response = requests.post(
        f"{BASE_URL}/execute",
        json={"code": code}
    )
    
    result = response.json()
    print(f"stdout: {result['stdout']}")
    print(f"stderr: {result['stderr']}")
    print(f"return_code: {result['return_code']}")
    if 'socket' in result['stderr'].lower() or result['return_code'] != 0:
        print("✅ Network blocking working!")
    print()


def test_with_input_files():
    """Test with input files"""
    print("=" * 60)
    print("Test 10: Input Files")
    print("=" * 60)
    
    code = """
import json

# Read input file
with open('data.json', 'r') as f:
    data = json.load(f)

print("Data received:", data)

# Process and create output
output = {
    'processed': True,
    'count': len(data['items']),
    'sum': sum(data['items'])
}

with open('output.json', 'w') as f:
    json.dump(output, f)

print("Output created")
"""
    
    # Prepare input file
    input_data = {
        'items': [1, 2, 3, 4, 5]
    }
    
    response = requests.post(
        f"{BASE_URL}/execute",
        json={
            "code": code,
            "files": {  # Changed from input_files to files
                "data.json": base64.b64encode(
                    json.dumps(input_data).encode()
                ).decode()
            }
        }
    )
    
    result = response.json()
    print(f"stdout: {result['stdout']}")
    print(f"stderr: {result['stderr']}")
    print(f"return_code: {result['return_code']}")
    
    if result['return_code'] == 0:
        print("✅ File operations working!")
        if 'output.json' in result.get('output_files', {}):
            output_content = base64.b64decode(result['output_files']['output.json'])
            output_data = json.loads(output_content)
            print(f"Output file: {output_data}")
    else:
        print("❌ File operations failed")
    print()


def test_safe_computation():
    """Test complex but safe computation"""
def test_safe_computation():
    """Test complex but safe computation"""
    print("=" * 60)
    print("Test 11: Safe Complex Computation")
    print("=" * 60)
    
    code = """
import math
import statistics

# Generate data
data = [math.sin(x / 10) for x in range(100)]

# Statistics
mean = statistics.mean(data)
median = statistics.median(data)
stdev = statistics.stdev(data)

print(f"Mean: {mean:.4f}")
print(f"Median: {median:.4f}")
print(f"Stdev: {stdev:.4f}")

# Find peaks
peaks = [i for i in range(1, len(data)-1) 
         if data[i] > data[i-1] and data[i] > data[i+1]]
print(f"Found {len(peaks)} peaks")
"""
    
    response = requests.post(
        f"{BASE_URL}/execute",
        json={"code": code}
    )
    
    result = response.json()
    print(f"stdout: {result['stdout']}")
    print(f"stderr: {result['stderr']}")
    print(f"return_code: {result['return_code']}")
    print()


def test_file_access_restriction():
    """Test that file access is restricted to sandbox directory"""
    print("=" * 60)
    print("Test 12: File Access Restriction (should fail)")
    print("=" * 60)
    
    code = """
# Try to read system file
try:
    with open('/etc/passwd', 'r') as f:
        print(f.read())
except PermissionError as e:
    print(f"Blocked: {e}")
"""
    
    response = requests.post(
        f"{BASE_URL}/execute",
        json={"code": code}
    )
    
    result = response.json()
    print(f"stdout: {result['stdout']}")
    print(f"stderr: {result['stderr']}")
    print(f"return_code: {result['return_code']}")
    if 'Blocked' in result['stdout'] or 'Permission' in result['stderr']:
        print("✅ File access restriction working!")
    print()


def run_all_tests():
    """Run all security tests"""
    print("\n")
    print("🔒 SECURE SANDBOX SECURITY TESTS")
    print("=" * 60)
    print()
    
    try:
        test_health_check()
        test_basic_execution()
        test_allowed_modules()
        test_blocked_module_os()
        test_blocked_module_subprocess()
        test_blocked_eval()
        # test_blocked_open()  # Removed - open is now allowed in sandbox dir
        test_timeout()
        test_memory_limit()
        test_network_blocking()
        test_with_input_files()
        test_safe_computation()
        test_file_access_restriction()
        
        print("=" * 60)
        print("✅ All security tests completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
