FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create sandbox user
RUN groupadd -r sandbox && \
    useradd -r -g sandbox -m -d /home/sandbox -s /bin/bash sandbox

# Create working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Create directories for file uploads and executions
RUN mkdir -p /app/uploads /app/executions && \
    chown -R sandbox:sandbox /app && \
    chmod 755 /app/uploads /app/executions

# Switch to sandbox user
USER sandbox

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
