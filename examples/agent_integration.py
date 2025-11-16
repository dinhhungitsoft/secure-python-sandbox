"""
Agent Integration Examples
===========================

This file demonstrates how to integrate the sandbox executor with AI agents.
"""

from sandbox_executor import SandboxExecutor, ExecutionMode, SandboxConfig
from typing import Dict, Any, Optional


class PythonCodeExecutorTool:
    """
    A tool class that can be integrated with AI agents (LangChain, AutoGen, etc.)
    """
    
    name = "python_code_executor"
    description = (
        "Execute Python code in a secure sandbox environment. "
        "Useful for performing calculations, data processing, and testing code snippets. "
        "The code runs in an isolated environment with limited resources."
    )
    
    def __init__(
        self,
        timeout: int = 30,
        allow_network: bool = False,
        mode: ExecutionMode = ExecutionMode.SECURE
    ):
        """
        Initialize the tool
        
        Args:
            timeout: Maximum execution time in seconds
            allow_network: Whether to allow network access
            mode: Execution mode (simple or secure)
        """
        self.executor = SandboxExecutor(
            mode=mode,
            timeout=timeout,
            allow_network=allow_network
        )
    
    def __call__(self, code: str) -> Dict[str, Any]:
        """
        Execute code and return results
        
        Args:
            code: Python code to execute
            
        Returns:
            Dictionary with execution results
        """
        try:
            result = self.executor.execute(code)
            
            return {
                "success": result.success,
                "output": result.output,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.return_code,
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "stdout": "",
                "stderr": str(e),
                "return_code": -1,
            }
    
    def run(self, code: str) -> str:
        """
        Simple interface that returns just the output string
        Useful for simple agent integrations
        """
        result = self(code)
        if result["success"]:
            return result["output"]
        return f"Error: {result['stderr']}"


# Example 1: Basic agent tool usage
def example_agent_tool_basic():
    """Example: Using as an agent tool"""
    print("=" * 60)
    print("Example: Agent Tool - Basic Usage")
    print("=" * 60)
    
    tool = PythonCodeExecutorTool()
    
    # Simulate agent generating code
    agent_code = """
# Calculate fibonacci numbers
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Calculate first 10 fibonacci numbers
fib_numbers = [fibonacci(i) for i in range(10)]
print("Fibonacci sequence:", fib_numbers)
"""
    
    result = tool.run(agent_code)
    print(f"Tool output:\n{result}\n")


# Example 2: LangChain-style integration
def example_langchain_style():
    """Example: LangChain-style tool wrapper"""
    print("=" * 60)
    print("Example: LangChain-Style Integration")
    print("=" * 60)
    
    # This is a mock implementation showing how it would integrate with LangChain
    class LangChainPythonTool:
        """Mock LangChain Tool"""
        
        def __init__(self):
            self.executor = SandboxExecutor(
                mode=ExecutionMode.SECURE,
                timeout=30,
                allow_network=False
            )
        
        def _run(self, code: str) -> str:
            """Required by LangChain"""
            result = self.executor.execute(code)
            if result.success:
                return result.stdout
            return f"Execution Error:\n{result.stderr}"
        
        async def _arun(self, code: str) -> str:
            """Async version required by LangChain"""
            return self._run(code)
    
    tool = LangChainPythonTool()
    
    code = """
import json
data = {"name": "AI Agent", "task": "Data Analysis"}
print(json.dumps(data, indent=2))
"""
    
    output = tool._run(code)
    print(f"LangChain tool output:\n{output}\n")


# Example 3: Multi-step agent workflow
def example_multi_step_workflow():
    """Example: Multi-step agent workflow"""
    print("=" * 60)
    print("Example: Multi-Step Agent Workflow")
    print("=" * 60)
    
    executor = SandboxExecutor()
    
    # Step 1: Agent generates data processing code
    step1_code = """
data = [10, 20, 30, 40, 50]
average = sum(data) / len(data)
print(f"Average: {average}")

# Save intermediate result
with open('step1_result.txt', 'w') as f:
    f.write(str(average))
"""
    
    print("Step 1: Calculate average")
    result1 = executor.execute(step1_code)
    print(result1.stdout)
    
    # Get intermediate result
    step1_output = result1.get_file_content('step1_result.txt')
    if step1_output:
        average = float(step1_output.decode().strip())
        
        # Step 2: Agent uses previous result
        step2_code = f"""
previous_average = {average}
variance_data = [10, 20, 30, 40, 50]

# Calculate variance
variance = sum((x - previous_average) ** 2 for x in variance_data) / len(variance_data)
std_dev = variance ** 0.5

print(f"Variance: {{variance}}")
print(f"Standard Deviation: {{std_dev:.2f}}")
"""
        
        print("\nStep 2: Calculate variance and std dev")
        result2 = executor.execute(step2_code)
        print(result2.stdout)
    
    print()


# Example 4: Error handling in agent context
def example_agent_error_handling():
    """Example: Error handling for agent"""
    print("=" * 60)
    print("Example: Agent Error Handling")
    print("=" * 60)
    
    tool = PythonCodeExecutorTool()
    
    # Simulate agent generating problematic code
    problematic_codes = [
        ("Division by zero", "result = 10 / 0"),
        ("Import error", "import nonexistent_module"),
        ("Syntax error", "print('hello'"),
        ("Infinite loop", "while True: pass"),
    ]
    
    for name, code in problematic_codes:
        print(f"\nTesting: {name}")
        result = tool(code)
        if result["success"]:
            print(f"✅ Success: {result['output']}")
        else:
            print(f"❌ Error: {result['stderr'][:100]}")  # Truncate error
    
    print()


# Example 5: Agent with file operations
def example_agent_with_files():
    """Example: Agent working with files"""
    print("=" * 60)
    print("Example: Agent with File Operations")
    print("=" * 60)
    
    executor = SandboxExecutor()
    
    # Agent creates data file
    input_files = {
        "dataset.csv": b"id,value\n1,100\n2,200\n3,300\n"
    }
    
    # Agent generates data analysis code
    code = """
import csv

# Read CSV data
with open('dataset.csv', 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Analyze
total = sum(int(row['value']) for row in data)
count = len(data)
avg = total / count

# Generate report
report = f'''
Data Analysis Report
====================
Total records: {count}
Sum of values: {total}
Average value: {avg}
'''

print(report)

# Save detailed report
with open('report.txt', 'w') as f:
    f.write(report)
    f.write('\\nDetailed data:\\n')
    for row in data:
        f.write(f"  ID {row['id']}: {row['value']}\\n")
"""
    
    result = executor.execute(code, input_files=input_files)
    print(result.stdout)
    
    # Agent retrieves the report
    if 'report.txt' in result.output_files:
        report_content = result.get_file_content('report.txt')
        print("\n📄 Generated report file:")
        print(report_content.decode())
    
    print()


# Example 6: Sandbox for code explanation/debugging
def example_code_debugging():
    """Example: Using sandbox for code debugging"""
    print("=" * 60)
    print("Example: Code Debugging with Sandbox")
    print("=" * 60)
    
    executor = SandboxExecutor(mode=ExecutionMode.SIMPLE)
    
    # Agent tests user's code
    user_code = """
def factorial(n):
    # Add debug prints
    print(f"Calculating factorial of {n}")
    if n <= 1:
        return 1
    result = n * factorial(n - 1)
    print(f"factorial({n}) = {result}")
    return result

# Test the function
result = factorial(5)
print(f"\\nFinal result: {result}")
"""
    
    print("Running user's code with debug output:")
    result = executor.execute(user_code)
    print(result.stdout)
    print()


if __name__ == "__main__":
    print("\n🤖 Sandbox Executor - Agent Integration Examples\n")
    
    example_agent_tool_basic()
    example_langchain_style()
    example_multi_step_workflow()
    example_agent_error_handling()
    example_agent_with_files()
    example_code_debugging()
    
    print("✅ All agent integration examples completed!")
