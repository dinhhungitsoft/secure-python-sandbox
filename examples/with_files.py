"""
Example: Execute code with input/output files
"""
import requests
import base64
import json

# Sandbox API URL
API_URL = "http://localhost:8000"


def read_and_process_file():
    """Execute code to read input file and create output file"""
    print("=" * 50)
    print("Example 1: Read Input File and Create Output")
    print("=" * 50)
    
    # Create input file content
    input_content = "Hello from input file!\nThis is line 2.\nThis is line 3."
    input_base64 = base64.b64encode(input_content.encode()).decode('utf-8')
    
    code = """
# Read input file
with open('input.txt', 'r') as f:
    content = f.read()
    print("Input file content:")
    print(content)
    print()

# Process and create output file
lines = content.split('\\n')
print(f"Number of lines: {len(lines)}")

# Write processed content to output file
with open('output.txt', 'w') as f:
    f.write("PROCESSED OUTPUT\\n")
    f.write("=" * 40 + "\\n")
    for i, line in enumerate(lines, 1):
        f.write(f"Line {i}: {line.upper()}\\n")

print("\\nOutput file created successfully!")
"""
    
    payload = {
        "code": code,
        "timeout": 10,
        "files": {
            "input.txt": input_base64
        }
    }
    
    response = requests.post(f"{API_URL}/execute", json=payload)
    result = response.json()
    
    print("STDOUT:")
    print(result["stdout"])
    
    if "output.txt" in result["output_files"]:
        output_content = base64.b64decode(result["output_files"]["output.txt"])
        print("\nOutput file content:")
        print(output_content.decode('utf-8'))
    print()


def work_with_csv():
    """Execute code to process CSV file"""
    print("=" * 50)
    print("Example 2: Process CSV File")
    print("=" * 50)
    
    # Create CSV content
    csv_content = """name,age,city
John,30,New York
Alice,25,London
Bob,35,Tokyo
Charlie,28,Paris"""
    
    csv_base64 = base64.b64encode(csv_content.encode()).decode('utf-8')
    
    code = """
import csv

# Read CSV file
with open('data.csv', 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)

print("CSV Data:")
print("-" * 40)
for row in data:
    print(f"{row['name']:10} | Age: {row['age']:3} | {row['city']}")

# Calculate and create report
total_age = sum(int(row['age']) for row in data)
avg_age = total_age / len(data)

report = f'''
CSV Processing Report
=====================
Total records: {len(data)}
Total age: {total_age}
Average age: {avg_age:.1f}

Cities: {', '.join(set(row['city'] for row in data))}
'''

print(report)

# Save report to file
with open('report.txt', 'w') as f:
    f.write(report)

print("Report saved to report.txt")
"""
    
    payload = {
        "code": code,
        "timeout": 10,
        "files": {
            "data.csv": csv_base64
        }
    }
    
    response = requests.post(f"{API_URL}/execute", json=payload)
    result = response.json()
    
    print("STDOUT:")
    print(result["stdout"])
    
    if "report.txt" in result["output_files"]:
        report_content = base64.b64decode(result["output_files"]["report.txt"])
        print("\nReport file content:")
        print(report_content.decode('utf-8'))
    print()


def work_with_json():
    """Execute code to process JSON file"""
    print("=" * 50)
    print("Example 3: Process JSON File")
    print("=" * 50)
    
    # Create JSON content
    json_data = {
        "users": [
            {"id": 1, "name": "John", "score": 85},
            {"id": 2, "name": "Alice", "score": 92},
            {"id": 3, "name": "Bob", "score": 78},
            {"id": 4, "name": "Charlie", "score": 95}
        ]
    }
    json_content = json.dumps(json_data, indent=2)
    json_base64 = base64.b64encode(json_content.encode()).decode('utf-8')
    
    code = """
import json

# Read JSON file
with open('data.json', 'r') as f:
    data = json.load(f)

print("User Scores:")
print("-" * 40)
for user in data['users']:
    print(f"ID: {user['id']} | {user['name']:10} | Score: {user['score']}")

# Calculate statistics
scores = [user['score'] for user in data['users']]
stats = {
    "count": len(scores),
    "min": min(scores),
    "max": max(scores),
    "average": sum(scores) / len(scores),
    "total": sum(scores)
}

print(f"\\nStatistics:")
print(f"  Count: {stats['count']}")
print(f"  Min: {stats['min']}")
print(f"  Max: {stats['max']}")
print(f"  Average: {stats['average']:.2f}")
print(f"  Total: {stats['total']}")

# Save statistics to JSON file
with open('stats.json', 'w') as f:
    json.dump(stats, f, indent=2)

print("\\nStatistics saved to stats.json")
"""
    
    payload = {
        "code": code,
        "timeout": 10,
        "files": {
            "data.json": json_base64
        }
    }
    
    response = requests.post(f"{API_URL}/execute", json=payload)
    result = response.json()
    
    print("STDOUT:")
    print(result["stdout"])
    
    if "stats.json" in result["output_files"]:
        stats_content = base64.b64decode(result["output_files"]["stats.json"])
        print("\nStats JSON content:")
        print(stats_content.decode('utf-8'))
    print()


def multiple_files():
    """Execute code with multiple input files"""
    print("=" * 50)
    print("Example 4: Multiple Input Files")
    print("=" * 50)
    
    # Create multiple files
    file1 = "Content of file 1"
    file2 = "Content of file 2"
    file3 = "Content of file 3"
    
    code = """
import os

# List all files
print("Files in directory:")
for filename in os.listdir('.'):
    if filename.endswith('.txt'):
        print(f"  - {filename}")

print()

# Read and merge all files
all_content = []
for i in range(1, 4):
    filename = f'file{i}.txt'
    with open(filename, 'r') as f:
        content = f.read()
        print(f"Reading {filename}: {content}")
        all_content.append(content)

# Create merged file
with open('merged.txt', 'w') as f:
    f.write("MERGED CONTENT\\n")
    f.write("=" * 40 + "\\n")
    for i, content in enumerate(all_content, 1):
        f.write(f"From file{i}.txt: {content}\\n")

print("\\nMerged file created!")
"""
    
    payload = {
        "code": code,
        "timeout": 10,
        "files": {
            "file1.txt": base64.b64encode(file1.encode()).decode('utf-8'),
            "file2.txt": base64.b64encode(file2.encode()).decode('utf-8'),
            "file3.txt": base64.b64encode(file3.encode()).decode('utf-8')
        }
    }
    
    response = requests.post(f"{API_URL}/execute", json=payload)
    result = response.json()
    
    print("STDOUT:")
    print(result["stdout"])
    
    if "merged.txt" in result["output_files"]:
        merged_content = base64.b64decode(result["output_files"]["merged.txt"])
        print("\nMerged file content:")
        print(merged_content.decode('utf-8'))
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
    read_and_process_file()
    work_with_csv()
    work_with_json()
    multiple_files()
    
    print("✅ All examples completed!")
