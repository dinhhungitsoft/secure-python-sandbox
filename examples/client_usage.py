"""
Unified Client Usage Examples
==============================

This file demonstrates how to use the SandboxClient for both local and remote execution.
"""

from sandbox_executor import SandboxClient, ClientConfig, ExecutionMode


def example_1_local_execution():
    """Example 1: Local execution (default)"""
    print("=" * 60)
    print("Example 1: Local Execution")
    print("=" * 60)
    
    # No server_url = local execution
    client = SandboxClient()
    
    print(f"Client mode: {client.get_mode_info()['execution_type']}")
    
    code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = [fibonacci(i) for i in range(10)]
print("Fibonacci:", result)
"""
    
    result = client.execute(code)
    print(f"Success: {result.success}")
    print(f"Output:\n{result.stdout}")
    print()


def example_2_remote_execution():
    """Example 2: Remote execution via API"""
    print("=" * 60)
    print("Example 2: Remote Execution")
    print("=" * 60)
    
    # With server_url = remote execution
    client = SandboxClient(
        server_url="http://localhost:8000",
        timeout=30
    )
    
    print(f"Client mode: {client.get_mode_info()['execution_type']}")
    print(f"Server: {client.server_url}")
    
    # Check if server is available
    if not client.health_check():
        print("⚠️  Server is not available. Start the server with:")
        print("   uvicorn src.main:app --reload")
        print()
        return
    
    code = """
import math

radius = 5
area = math.pi * radius ** 2
circumference = 2 * math.pi * radius

print(f"Circle with radius {radius}:")
print(f"  Area: {area:.2f}")
print(f"  Circumference: {circumference:.2f}")
"""
    
    result = client.execute(code)
    print(f"Success: {result.success}")
    print(f"Output:\n{result.stdout}")
    print()


def example_3_with_config():
    """Example 3: Using ClientConfig"""
    print("=" * 60)
    print("Example 3: Using ClientConfig")
    print("=" * 60)
    
    # Local configuration
    local_config = ClientConfig(
        server_url=None,  # Local
        timeout=60,
        allow_network=False,
        mode=ExecutionMode.SECURE,
        max_memory_mb=256
    )
    
    client = SandboxClient.from_config(local_config)
    
    code = """
data = [10, 20, 30, 40, 50]
average = sum(data) / len(data)
variance = sum((x - average) ** 2 for x in data) / len(data)
std_dev = variance ** 0.5

print(f"Data: {data}")
print(f"Average: {average}")
print(f"Std Dev: {std_dev:.2f}")
"""
    
    result = client.execute(code)
    print(result.stdout)
    print()


def example_4_remote_with_auth():
    """Example 4: Remote execution with API key"""
    print("=" * 60)
    print("Example 4: Remote with Authentication")
    print("=" * 60)
    
    # Remote with API key
    remote_config = ClientConfig(
        server_url="http://api.example.com",
        timeout=30,
        api_key="your-secret-api-key",
        api_timeout=60
    )
    
    client = SandboxClient.from_config(remote_config)
    
    print(f"Mode info: {client.get_mode_info()}")
    print("Note: This would connect to a real API server with authentication")
    print()


def example_5_file_operations():
    """Example 5: Working with files (local and remote)"""
    print("=" * 60)
    print("Example 5: File Operations")
    print("=" * 60)
    
    client = SandboxClient()  # Local
    
    # Provide input files
    input_files = {
        "data.csv": b"id,value\n1,100\n2,200\n3,300\n"
    }
    
    code = """
# Read CSV
lines = []
with open('data.csv', 'r') as f:
    lines = f.readlines()

print(f"Read {len(lines)} lines")

# Process and write output
total = 0
for line in lines[1:]:  # Skip header
    parts = line.strip().split(',')
    if len(parts) == 2:
        total += int(parts[1])

with open('result.txt', 'w') as f:
    f.write(f"Total: {total}\\n")

print(f"Total value: {total}")
"""
    
    result = client.execute(code, input_files=input_files)
    print(result.stdout)
    
    # Get output file
    if 'result.txt' in result.output_files:
        content = result.get_file_content('result.txt')
        print(f"\nOutput file content: {content.decode()}")
    print()


def example_6_error_handling():
    """Example 6: Error handling"""
    print("=" * 60)
    print("Example 6: Error Handling")
    print("=" * 60)
    
    client = SandboxClient()
    
    # Code with error
    bad_code = """
def divide(a, b):
    return a / b

result = divide(10, 0)  # ZeroDivisionError
print(result)
"""
    
    result = client.execute(bad_code)
    
    print(f"Success: {result.success}")
    if not result.success:
        print(f"Error:\n{result.stderr}")
    print()


def example_7_timeout_override():
    """Example 7: Override timeout per execution"""
    print("=" * 60)
    print("Example 7: Override Timeout")
    print("=" * 60)
    
    # Default timeout is 30 seconds
    client = SandboxClient(timeout=30)
    
    # But we can override for specific execution
    code = """
import time
print("Starting...")
time.sleep(2)
print("Done!")
"""
    
    # Override timeout to 5 seconds for this execution
    result = client.execute(code, timeout=5)
    print(result.stdout)
    print()


def example_8_validation():
    """Example 8: Code validation"""
    print("=" * 60)
    print("Example 8: Code Validation")
    print("=" * 60)
    
    client = SandboxClient()
    
    # Valid code
    valid_code = "print('Hello, World!')"
    is_valid, error = client.validate_code(valid_code)
    print(f"Valid code: {is_valid}")
    
    # Invalid code
    invalid_code = "print('Hello, World!"  # Missing quote
    is_valid, error = client.validate_code(invalid_code)
    print(f"Invalid code: {is_valid}")
    print(f"Error: {error}")
    print()


def example_9_switch_modes():
    """Example 9: Switching between local and remote"""
    print("=" * 60)
    print("Example 9: Switching Execution Modes")
    print("=" * 60)
    
    code = "print('Testing execution mode')"
    
    # Local execution
    local_client = SandboxClient()
    print(f"Local client: {local_client}")
    result = local_client.execute(code)
    print(f"Local result: {result.stdout.strip()}")
    
    # Remote execution (if server is available)
    remote_client = SandboxClient(server_url="http://localhost:8000")
    print(f"\nRemote client: {remote_client}")
    
    if remote_client.health_check():
        result = remote_client.execute(code)
        print(f"Remote result: {result.stdout.strip()}")
    else:
        print("Remote server not available (this is OK for demo)")
    
    print()


def example_10_agent_integration():
    """Example 10: Integration with AI Agent"""
    print("=" * 60)
    print("Example 10: AI Agent Integration")
    print("=" * 60)
    
    class AgentPythonTool:
        """Simple tool wrapper for AI agents"""
        
        def __init__(self, server_url: Optional[str] = None):
            self.client = SandboxClient(
                server_url=server_url,
                timeout=30,
                allow_network=False
            )
        
        def execute_python(self, code: str) -> str:
            """Execute Python code and return output"""
            result = self.client.execute(code)
            if result.success:
                return result.stdout
            return f"Error: {result.stderr}"
    
    # Use local execution
    tool = AgentPythonTool()
    
    # Agent generates this code
    agent_code = """
def calculate_statistics(numbers):
    mean = sum(numbers) / len(numbers)
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    median = sorted_nums[n//2] if n % 2 else (sorted_nums[n//2-1] + sorted_nums[n//2]) / 2
    return mean, median

numbers = [10, 20, 15, 30, 25]
mean, median = calculate_statistics(numbers)
print(f"Mean: {mean}, Median: {median}")
"""
    
    output = tool.execute_python(agent_code)
    print(f"Agent tool output:\n{output}")
    print()


if __name__ == "__main__":
    from typing import Optional
    
    print("\n🚀 Sandbox Client - Usage Examples\n")
    
    example_1_local_execution()
    example_2_remote_execution()
    example_3_with_config()
    example_4_remote_with_auth()
    example_5_file_operations()
    example_6_error_handling()
    example_7_timeout_override()
    example_8_validation()
    example_9_switch_modes()
    example_10_agent_integration()
    
    print("✅ All examples completed!")
