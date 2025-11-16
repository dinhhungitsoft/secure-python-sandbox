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

# Copy package files first (better caching)
COPY pyproject.toml setup.py ./
COPY src/ ./src/

# Install the package with API dependencies
# This installs: pydantic, python-dotenv, fastapi, uvicorn
RUN pip install --no-cache-dir -e ".[api]"

# Create directories for file uploads and executions
RUN mkdir -p /app/uploads /app/executions && \
    chown -R sandbox:sandbox /app && \
    chmod 755 /app/uploads /app/executions

# Switch to sandbox user
USER sandbox

# Expose port
EXPOSE 8000

# Environment variables (can be overridden)
ENV EXECUTION_MODE=secure
ENV SANDBOX_TIMEOUT=30
ENV SANDBOX_ALLOW_NETWORK=false

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
