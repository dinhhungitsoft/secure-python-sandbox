# Examples - Python Code Sandbox

Thư mục này chứa các ví dụ sử dụng Python Code Sandbox API.

## Yêu cầu

Trước khi chạy các examples, đảm bảo:

1. **Sandbox đang chạy**:
   ```bash
   docker-compose up -d
   ```

2. **Cài đặt requests library** (cho examples):
   ```bash
   pip install requests
   ```

## Các file examples

### 1. simple_execute.py
Ví dụ cơ bản về thực thi Python code.

**Chạy:**
```bash
python examples/simple_execute.py
```

**Bao gồm:**
- Hello World đơn giản
- Tính toán với variables
- Xử lý errors
- Sử dụng standard library (json, math, datetime)

---

### 2. with_files.py
Ví dụ về thực thi code với input/output files (JSON API với base64).

**Chạy:**
```bash
python examples/with_files.py
```

**Bao gồm:**
- Đọc input file và tạo output file
- Xử lý CSV data
- Xử lý JSON data
- Multiple input files

---

### 3. with_multipart.py
Ví dụ upload files qua multipart/form-data.

**Chạy:**
```bash
python examples/with_multipart.py
```

**Bao gồm:**
- Upload single file
- Upload multiple files
- Upload và xử lý CSV file
- Tạo analysis report

---

### 4. test_network.py
Test và demo network access control.

**Chạy:**
```bash
python examples/test_network.py
```

**Bao gồm:**
- Test với network disabled (default)
- Test với network enabled
- Test với urllib library
- Test với requests library (nếu có)
- DNS lookup comparison

## Chạy tất cả examples

```bash
# Chạy lần lượt từng example
python examples/simple_execute.py
python examples/with_files.py
python examples/with_multipart.py
python examples/test_network.py
```

## Tạo example của riêng bạn

```python
import requests

# API URL
API_URL = "http://localhost:8000"

# Execute code
payload = {
    "code": "print('Hello from my custom example!')",
    "timeout": 10,
    "allow_network": False
}

response = requests.post(f"{API_URL}/execute", json=payload)
result = response.json()

print("STDOUT:", result["stdout"])
print("STDERR:", result["stderr"])
print("Return Code:", result["return_code"])
```

## Troubleshooting

### Error: Cannot connect to API

**Lỗi:**
```
❌ Error: Cannot connect to API. Make sure the sandbox is running.
```

**Giải pháp:**
```bash
# Start sandbox
docker-compose up -d

# Check if running
docker-compose ps

# Check logs
docker-compose logs -f
```

### Error: ModuleNotFoundError: No module named 'requests'

**Giải pháp:**
```bash
pip install requests
```

### Examples chạy chậm

- Timeout mặc định là 30 giây
- Network requests có thể mất thời gian
- Kiểm tra logs: `docker-compose logs -f`

## Tham khảo thêm

- [README.md](../README.md) - Documentation chính
- [CONFIGURATION.md](../CONFIGURATION.md) - Hướng dẫn cấu hình
- API Docs: http://localhost:8000/docs (khi sandbox đang chạy)
