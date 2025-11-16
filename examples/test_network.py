"""
Example: Test network access in sandbox
"""
import requests

# Sandbox API URL
API_URL = "http://localhost:8000"


def test_without_network():
    """Test code with network disabled (default)"""
    print("=" * 60)
    print("Test 1: Network DISABLED (default)")
    print("=" * 60)
    
    code = """
import urllib.request

try:
    print("Attempting to access google.com...")
    response = urllib.request.urlopen('http://google.com', timeout=5)
    print(f"Success! Status: {response.status}")
    print(f"Content length: {len(response.read())}")
except Exception as e:
    print(f"Failed: {type(e).__name__}: {str(e)}")
"""
    
    payload = {
        "code": code,
        "timeout": 10,
        "allow_network": False  # Explicitly disable
    }
    
    response = requests.post(f"{API_URL}/execute", json=payload)
    result = response.json()
    
    print("STDOUT:")
    print(result["stdout"])
    if result["stderr"]:
        print("\nSTDERR:")
        print(result["stderr"])
    print()


def test_with_network():
    """Test code with network enabled"""
    print("=" * 60)
    print("Test 2: Network ENABLED")
    print("=" * 60)
    
    code = """
import urllib.request

try:
    print("Attempting to access google.com...")
    response = urllib.request.urlopen('http://google.com', timeout=5)
    print(f"Success! Status: {response.status}")
    content = response.read()
    print(f"Content length: {len(content)} bytes")
    print("First 100 chars:", content[:100].decode('utf-8', errors='ignore'))
except Exception as e:
    print(f"Failed: {type(e).__name__}: {str(e)}")
"""
    
    payload = {
        "code": code,
        "timeout": 10,
        "allow_network": True  # Enable network
    }
    
    response = requests.post(f"{API_URL}/execute", json=payload)
    result = response.json()
    
    print("STDOUT:")
    print(result["stdout"])
    if result["stderr"]:
        print("\nSTDERR:")
        print(result["stderr"])
    print()


def test_requests_library_disabled():
    """Test with requests library when network is disabled"""
    print("=" * 60)
    print("Test 3: Using requests library (Network DISABLED)")
    print("=" * 60)
    
    code = """
try:
    import requests
    print("Attempting to GET http://httpbin.org/get...")
    response = requests.get('http://httpbin.org/get', timeout=5)
    print(f"Success! Status code: {response.status_code}")
    print(f"Response: {response.json()}")
except ImportError:
    print("requests library not installed")
except Exception as e:
    print(f"Failed: {type(e).__name__}: {str(e)}")
"""
    
    payload = {
        "code": code,
        "timeout": 10,
        "allow_network": False
    }
    
    response = requests.post(f"{API_URL}/execute", json=payload)
    result = response.json()
    
    print("STDOUT:")
    print(result["stdout"])
    if result["stderr"]:
        print("\nSTDERR:")
        print(result["stderr"])
    print()


def test_requests_library_enabled():
    """Test with requests library when network is enabled"""
    print("=" * 60)
    print("Test 4: Using requests library (Network ENABLED)")
    print("=" * 60)
    
    code = """
try:
    import requests
    print("Attempting to GET http://httpbin.org/get...")
    response = requests.get('http://httpbin.org/get', timeout=5)
    print(f"Success! Status code: {response.status_code}")
    data = response.json()
    print(f"Origin IP: {data.get('origin', 'N/A')}")
    print(f"Headers: {list(data.get('headers', {}).keys())}")
except ImportError:
    print("requests library not installed")
except Exception as e:
    print(f"Failed: {type(e).__name__}: {str(e)}")
"""
    
    payload = {
        "code": code,
        "timeout": 10,
        "allow_network": True
    }
    
    response = requests.post(f"{API_URL}/execute", json=payload)
    result = response.json()
    
    print("STDOUT:")
    print(result["stdout"])
    if result["stderr"]:
        print("\nSTDERR:")
        print(result["stderr"])
    print()


def test_dns_lookup():
    """Test DNS lookup"""
    print("=" * 60)
    print("Test 5: DNS Lookup Comparison")
    print("=" * 60)
    
    code = """
import socket

print("Testing DNS resolution...")
try:
    ip = socket.gethostbyname('google.com')
    print(f"google.com resolves to: {ip}")
except Exception as e:
    print(f"DNS lookup failed: {type(e).__name__}: {str(e)}")
"""
    
    # Test without network
    print("\n--- With Network DISABLED ---")
    payload = {
        "code": code,
        "timeout": 10,
        "allow_network": False
    }
    response = requests.post(f"{API_URL}/execute", json=payload)
    result = response.json()
    print(result["stdout"])
    
    # Test with network
    print("\n--- With Network ENABLED ---")
    payload["allow_network"] = True
    response = requests.post(f"{API_URL}/execute", json=payload)
    result = response.json()
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
    
    # Run tests
    test_without_network()
    test_with_network()
    test_requests_library_disabled()
    test_requests_library_enabled()
    test_dns_lookup()
    
    print("=" * 60)
    print("✅ All network tests completed!")
    print("=" * 60)
    print("\nSummary:")
    print("- allow_network=False: Network access is BLOCKED (default)")
    print("- allow_network=True: Network access is ALLOWED")
