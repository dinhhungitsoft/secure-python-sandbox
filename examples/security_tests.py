"""
Script để test các security features của sandbox
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_security_feature(name: str, code: str, should_fail: bool = True):
    """Test một security feature"""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}")
    print(f"Code:\n{code}\n")
    
    try:
        response = requests.post(
            f"{BASE_URL}/execute",
            json={"code": code},
            timeout=35
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Status: SUCCESS (return_code={result['return_code']})")
            print(f"Stdout: {result['stdout']}")
            if result['stderr']:
                print(f"Stderr: {result['stderr']}")
            
            if should_fail:
                print(f"❌ SECURITY ISSUE: This attack should have been blocked!")
            else:
                print(f"✅ EXPECTED: Legitimate code executed successfully")
        else:
            print(f"✗ Status: HTTP {response.status_code}")
            print(f"Error: {response.text}")
    
    except requests.exceptions.Timeout:
        print("✗ Status: TIMEOUT")
        if should_fail:
            print("✅ GOOD: Attack was stopped by timeout")
    except Exception as e:
        print(f"✗ Exception: {str(e)}")


def main():
    print("="*60)
    print("SANDBOX SECURITY TESTS")
    print("="*60)
    
    # Test 1: Legitimate code (should succeed)
    test_security_feature(
        "Legitimate Code - Print Hello World",
        "print('Hello from secure sandbox!')",
        should_fail=False
    )
    
    # Test 2: Memory bomb
    test_security_feature(
        "Memory Bomb Attack",
        """
import sys
try:
    # Try to allocate 1GB of memory
    data = 'x' * (1024 * 1024 * 1024)
    print(f"Allocated {len(data)} bytes")
except MemoryError:
    print("Memory limit reached!")
    sys.exit(1)
"""
    )
    
    # Test 3: Fork bomb
    test_security_feature(
        "Fork Bomb Attack",
        """
import os
import sys
try:
    for i in range(100):
        pid = os.fork()
        if pid == 0:
            print(f"Child process {i}")
            sys.exit(0)
except Exception as e:
    print(f"Fork blocked: {e}")
    sys.exit(1)
"""
    )
    
    # Test 4: Network access (should fail if allow_network=False)
    test_security_feature(
        "Network Access Attack",
        """
import socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect(('google.com', 80))
    print("Network access allowed!")
    s.close()
except Exception as e:
    print(f"Network blocked: {e}")
"""
    )
    
    # Test 5: File system access outside working dir
    test_security_feature(
        "File System Access Attack",
        """
import os
try:
    # Try to read /etc/passwd
    with open('/etc/passwd', 'r') as f:
        content = f.read()
        print("Read /etc/passwd successfully!")
        print(content[:100])
except Exception as e:
    print(f"File access blocked: {e}")
"""
    )
    
    # Test 6: System command execution
    test_security_feature(
        "System Command Execution Attack",
        """
import subprocess
try:
    result = subprocess.run(['ls', '-la', '/'], capture_output=True, text=True, timeout=2)
    print("Command executed successfully!")
    print(result.stdout[:200])
except Exception as e:
    print(f"Command execution blocked: {e}")
"""
    )
    
    # Test 7: Infinite loop (should timeout)
    test_security_feature(
        "Infinite Loop Attack",
        """
import time
print("Starting infinite loop...")
i = 0
while True:
    i += 1
    if i % 1000000 == 0:
        print(f"Still running... {i}")
"""
    )
    
    # Test 8: CPU intensive task
    test_security_feature(
        "CPU Intensive Task",
        """
import time
start = time.time()
# Calculate primes (CPU intensive)
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

count = 0
for i in range(100000):
    if is_prime(i):
        count += 1

end = time.time()
print(f"Found {count} primes in {end-start:.2f} seconds")
"""
    )
    
    # Test 9: Large output
    test_security_feature(
        "Large Output Attack",
        """
# Try to generate huge output
for i in range(1000000):
    print(f"Line {i}: " + "x" * 100)
print("Done")
""",
        should_fail=False  # Should truncate, not fail
    )
    
    # Test 10: File creation (should work)
    test_security_feature(
        "File Creation Test",
        """
# This should work - creating files in working directory
with open('output.txt', 'w') as f:
    f.write('Hello from sandbox!')

with open('output.txt', 'r') as f:
    content = f.read()
    print(f"Created file with content: {content}")
""",
        should_fail=False
    )
    
    print("\n" + "="*60)
    print("TESTS COMPLETED")
    print("="*60)


if __name__ == "__main__":
    main()
