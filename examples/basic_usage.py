"""
Basic Usage Examples for Sandbox Executor
==========================================

This file demonstrates basic usage of the sandbox executor library.
"""

from sandbox_executor import SandboxExecutor, ExecutionMode, SandboxConfig


def example_1_simple_execution():
    """Example 1: Simple code execution"""
    print("=" * 60)
    print("Example 1: Simple Code Execution")
    print("=" * 60)
    
    executor = SandboxExecutor()
    
    code = """
def greet(name):
    return f"Hello, {name}!"

message = greet("Python Sandbox")
print(message)
"""
    
    result = executor.execute(code)
    
    print(f"Success: {result.success}")
    print(f"Output: {result.stdout}")
    print(f"Errors: {result.stderr}")
    print()


def example_2_with_config():
    """Example 2: Using configuration"""
    print("=" * 60)
    print("Example 2: Using Configuration")
    print("=" * 60)
    
    config = SandboxConfig(
        mode=ExecutionMode.SECURE,
        timeout=60,
        allow_network=False,
        max_memory_mb=256
    )
    
    executor = SandboxExecutor.from_config(config)
    
    code = """
import math

def calculate_circle_area(radius):
    return math.pi * radius ** 2

areas = [calculate_circle_area(r) for r in range(1, 6)]
for i, area in enumerate(areas, 1):
    print(f"Circle {i}: Area = {area:.2f}")
"""
    
    result = executor.execute(code)
    print(result.stdout)
    print()


def example_3_error_handling():
    """Example 3: Error handling"""
    print("=" * 60)
    print("Example 3: Error Handling")
    print("=" * 60)
    
    executor = SandboxExecutor(mode=ExecutionMode.SIMPLE)
    
    # Code with error
    code = """
def divide(a, b):
    return a / b

result = divide(10, 0)  # This will cause ZeroDivisionError
print(result)
"""
    
    result = executor.execute(code)
    
    print(f"Success: {result.success}")
    print(f"Return code: {result.return_code}")
    print(f"Error output:\n{result.stderr}")
    print()


def example_4_timeout():
    """Example 4: Handling timeout"""
    print("=" * 60)
    print("Example 4: Timeout Handling")
    print("=" * 60)
    
    executor = SandboxExecutor(timeout=2)
    
    # Code that takes too long
    code = """
import time
print("Starting long calculation...")
time.sleep(5)  # Will timeout after 2 seconds
print("Done!")
"""
    
    result = executor.execute(code)
    
    print(f"Success: {result.success}")
    print(f"Stderr: {result.stderr}")
    print()


def example_5_file_operations():
    """Example 5: Working with files"""
    print("=" * 60)
    print("Example 5: File Operations")
    print("=" * 60)
    
    executor = SandboxExecutor()
    
    # Provide input files
    input_files = {
        "data.txt": b"Line 1\nLine 2\nLine 3\n",
        "numbers.txt": b"1,2,3,4,5\n"
    }
    
    code = """
# Read from input file
with open('data.txt', 'r') as f:
    lines = f.readlines()
    print(f"Read {len(lines)} lines from data.txt")

# Read numbers and calculate sum
with open('numbers.txt', 'r') as f:
    numbers = list(map(int, f.read().strip().split(',')))
    total = sum(numbers)
    print(f"Sum of numbers: {total}")

# Write output file
with open('output.txt', 'w') as f:
    f.write(f"Processed {len(lines)} lines\\n")
    f.write(f"Total: {total}\\n")

print("Files processed successfully!")
"""
    
    result = executor.execute(code, input_files=input_files)
    
    print(result.stdout)
    
    # Get output file
    if 'output.txt' in result.output_files:
        output_content = result.get_file_content('output.txt')
        print(f"\nOutput file content:\n{output_content.decode()}")
    print()


def example_6_validation():
    """Example 6: Code validation"""
    print("=" * 60)
    print("Example 6: Code Validation")
    print("=" * 60)
    
    executor = SandboxExecutor()
    
    # Valid code
    valid_code = "print('Hello, World!')"
    is_valid, error = executor.validate_code(valid_code)
    print(f"Valid code: {is_valid}")
    
    # Invalid code
    invalid_code = "print('Hello, World!"  # Missing closing quote
    is_valid, error = executor.validate_code(invalid_code)
    print(f"Invalid code: {is_valid}")
    print(f"Error: {error}")
    print()


def example_7_from_env():
    """Example 7: Configuration from environment"""
    print("=" * 60)
    print("Example 7: Configuration from Environment")
    print("=" * 60)
    
    # This will read from environment variables like:
    # SANDBOX_MODE, SANDBOX_TIMEOUT, etc.
    executor = SandboxExecutor.from_env()
    
    code = "print('Configured from environment!')"
    result = executor.execute(code)
    print(result.stdout)
    print()


if __name__ == "__main__":
    print("\n🚀 Sandbox Executor - Basic Usage Examples\n")
    
    example_1_simple_execution()
    example_2_with_config()
    example_3_error_handling()
    example_4_timeout()
    example_5_file_operations()
    example_6_validation()
    example_7_from_env()
    
    print("✅ All examples completed!")
