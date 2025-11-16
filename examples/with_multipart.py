"""
Example: Upload files via multipart/form-data
"""
import requests
import tempfile
import os

# Sandbox API URL
API_URL = "http://localhost:8000"


def upload_single_file():
    """Upload a single file via multipart"""
    print("=" * 50)
    print("Example 1: Upload Single File (Multipart)")
    print("=" * 50)
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("Hello from uploaded file!\n")
        f.write("This is a test file.")
        temp_file = f.name
    
    code = """
import os

print("Files in directory:", os.listdir('.'))

# Read uploaded file
for filename in os.listdir('.'):
    if filename.endswith('.txt'):
        print(f"\\nReading {filename}:")
        with open(filename, 'r') as f:
            print(f.read())
"""
    
    try:
        with open(temp_file, 'rb') as f:
            files = {'files': ('test.txt', f, 'text/plain')}
            data = {'code': code, 'timeout': 10}
            
            response = requests.post(
                f"{API_URL}/execute-with-files",
                files=files,
                data=data
            )
            result = response.json()
            
            print("STDOUT:")
            print(result["stdout"])
            print()
    finally:
        # Cleanup
        os.unlink(temp_file)


def upload_multiple_files():
    """Upload multiple files via multipart"""
    print("=" * 50)
    print("Example 2: Upload Multiple Files (Multipart)")
    print("=" * 50)
    
    # Create multiple temporary files
    temp_files = []
    for i in range(1, 4):
        with tempfile.NamedTemporaryFile(
            mode='w', 
            delete=False, 
            suffix=f'_{i}.txt'
        ) as f:
            f.write(f"Content of file {i}\n")
            f.write(f"Line 2 of file {i}")
            temp_files.append(f.name)
    
    code = """
import os

# List all files
files = [f for f in os.listdir('.') if f.endswith('.txt')]
print(f"Found {len(files)} files:")
for filename in sorted(files):
    print(f"  - {filename}")

print("\\n" + "=" * 40)

# Read and display content
for filename in sorted(files):
    print(f"\\nContent of {filename}:")
    print("-" * 40)
    with open(filename, 'r') as f:
        print(f.read())

# Create summary file
with open('summary.txt', 'w') as f:
    f.write("FILE SUMMARY\\n")
    f.write("=" * 40 + "\\n\\n")
    for filename in sorted(files):
        with open(filename, 'r') as src:
            f.write(f"File: {filename}\\n")
            f.write(f"Content: {src.read()}\\n\\n")

print("\\nSummary file created!")
"""
    
    try:
        # Prepare multiple files for upload
        files = []
        for temp_file in temp_files:
            files.append(
                ('files', (os.path.basename(temp_file), open(temp_file, 'rb'), 'text/plain'))
            )
        
        data = {'code': code, 'timeout': 10}
        
        response = requests.post(
            f"{API_URL}/execute-with-files",
            files=files,
            data=data
        )
        result = response.json()
        
        print("STDOUT:")
        print(result["stdout"])
        
        # Show summary file if exists
        if "summary.txt" in result["output_files"]:
            import base64
            summary_content = base64.b64decode(result["output_files"]["summary.txt"])
            print("\nSummary file content:")
            print(summary_content.decode('utf-8'))
        print()
        
    finally:
        # Cleanup
        for temp_file in temp_files:
            os.unlink(temp_file)


def upload_csv_file():
    """Upload and process CSV file"""
    print("=" * 50)
    print("Example 3: Upload CSV File (Multipart)")
    print("=" * 50)
    
    # Create CSV file
    csv_content = """name,age,department,salary
John Doe,30,Engineering,75000
Jane Smith,28,Marketing,65000
Bob Johnson,35,Engineering,85000
Alice Brown,32,HR,60000
Charlie Wilson,29,Marketing,70000"""
    
    with tempfile.NamedTemporaryFile(
        mode='w', 
        delete=False, 
        suffix='.csv'
    ) as f:
        f.write(csv_content)
        temp_file = f.name
    
    code = """
import csv

# Read CSV file
with open('employees.csv', 'r') as f:
    reader = csv.DictReader(f)
    employees = list(reader)

print("Employee Data:")
print("=" * 60)
for emp in employees:
    print(f"{emp['name']:20} | Age: {emp['age']:2} | {emp['department']:12} | ${emp['salary']}")

# Analyze by department
from collections import defaultdict
dept_stats = defaultdict(lambda: {'count': 0, 'total_salary': 0})

for emp in employees:
    dept = emp['department']
    dept_stats[dept]['count'] += 1
    dept_stats[dept]['total_salary'] += int(emp['salary'])

print("\\nDepartment Statistics:")
print("=" * 60)
for dept, stats in dept_stats.items():
    avg_salary = stats['total_salary'] / stats['count']
    print(f"{dept:12} | Employees: {stats['count']} | Avg Salary: ${avg_salary:,.2f}")

# Save report
with open('analysis.txt', 'w') as f:
    f.write("EMPLOYEE ANALYSIS REPORT\\n")
    f.write("=" * 60 + "\\n\\n")
    f.write(f"Total Employees: {len(employees)}\\n\\n")
    
    for dept, stats in dept_stats.items():
        avg_salary = stats['total_salary'] / stats['count']
        f.write(f"\\nDepartment: {dept}\\n")
        f.write(f"  Employees: {stats['count']}\\n")
        f.write(f"  Total Salary: ${stats['total_salary']:,}\\n")
        f.write(f"  Average Salary: ${avg_salary:,.2f}\\n")

print("\\nAnalysis report saved!")
"""
    
    try:
        with open(temp_file, 'rb') as f:
            files = {'files': ('employees.csv', f, 'text/csv')}
            data = {'code': code, 'timeout': 10}
            
            response = requests.post(
                f"{API_URL}/execute-with-files",
                files=files,
                data=data
            )
            result = response.json()
            
            print("STDOUT:")
            print(result["stdout"])
            
            # Show analysis report
            if "analysis.txt" in result["output_files"]:
                import base64
                report_content = base64.b64decode(result["output_files"]["analysis.txt"])
                print("\nAnalysis Report:")
                print(report_content.decode('utf-8'))
            print()
    finally:
        # Cleanup
        os.unlink(temp_file)


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
    upload_single_file()
    upload_multiple_files()
    upload_csv_file()
    
    print("✅ All examples completed!")
