from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import base64
import os
from .executor_factory import ExecutorFactory

app = FastAPI(
    title="Python Code Sandbox",
    description="API to execute Python code in a secure sandbox environment",
    version="1.0.0"
)

# Read configuration from environment variables
DEFAULT_TIMEOUT = int(os.getenv("SANDBOX_TIMEOUT", "30"))
DEFAULT_ALLOW_NETWORK = os.getenv("SANDBOX_ALLOW_NETWORK", "false").lower() in ("true", "1", "yes")
EXECUTION_MODE = os.getenv("EXECUTION_MODE", "secure").lower()  # secure, simple

# Initialize executor using Factory pattern with fallback mechanism
executor, EXECUTOR_MODE = ExecutorFactory.create_with_fallback(
    preferred_mode=EXECUTION_MODE,
    fallback_mode="secure",
    timeout=DEFAULT_TIMEOUT,
    max_output_size=1024 * 1024,
    allow_network=DEFAULT_ALLOW_NETWORK,
    memory_limit="128m",
    cpu_quota=50000,
    pids_limit=20,
    max_memory_mb=128,
    max_cpu_time=DEFAULT_TIMEOUT
)

# Print message about the executor mode being used
MODE_MESSAGES = {
    "secure": "✅ Using Secure Sandbox (Platform-agnostic, multi-layered security)",
    "simple": "✅ Using Simple Subprocess (Basic isolation)"
}
print(MODE_MESSAGES.get(EXECUTOR_MODE, f"✅ Using {EXECUTOR_MODE} mode"))


class ExecuteRequest(BaseModel):
    """Request model for execute endpoint"""
    code: str = Field(..., description="Python code to execute")
    timeout: Optional[int] = Field(None, description="Timeout (seconds)", ge=1, le=300)
    allow_network: Optional[bool] = Field(None, description="Allow internet access")
    files: Optional[Dict[str, str]] = Field(
        None, 
        description="Dictionary mapping filename -> file content (base64)"
    )


class ExecuteResponse(BaseModel):
    """Response model for execute endpoint"""
    stdout: str = Field(..., description="Standard output")
    stderr: str = Field(..., description="Standard error")
    return_code: int = Field(..., description="Process return code")
    output_files: Dict[str, str] = Field(
        ..., 
        description="Dictionary mapping filename -> file content (base64)"
    )


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Python Code Sandbox API is running",
        "version": "1.0.0"
    }


@app.post("/execute", response_model=ExecuteResponse)
async def execute_code(request: ExecuteRequest):
    """
    Execute Python code in sandbox
    
    Args:
        request: ExecuteRequest containing code and optional files
    
    Returns:
        ExecuteResponse containing stdout, stderr, return_code and output_files
    """
    try:
        # Decode input files from base64 if provided
        input_files = None
        if request.files:
            input_files = {}
            for filename, base64_content in request.files.items():
                try:
                    file_content = base64.b64decode(base64_content)
                    input_files[filename] = file_content
                except Exception as e:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid base64 encoding for file {filename}: {str(e)}"
                    )
        
        # Use value from request or default from env
        timeout = request.timeout if request.timeout is not None else DEFAULT_TIMEOUT
        allow_network = request.allow_network if request.allow_network is not None else DEFAULT_ALLOW_NETWORK
        
        # Create executor with custom config if different from default
        if timeout != DEFAULT_TIMEOUT or allow_network != DEFAULT_ALLOW_NETWORK:
            custom_executor = ExecutorFactory.create_executor(
                mode=EXECUTOR_MODE,
                timeout=timeout,
                max_output_size=1024 * 1024,
                allow_network=allow_network,
                memory_limit="128m",
                cpu_quota=50000,
                pids_limit=20,
                max_memory_mb=128,
                max_cpu_time=timeout
            )
            result = custom_executor.execute(request.code, input_files)
        else:
            result = executor.execute(request.code, input_files)
        
        return ExecuteResponse(**result)
    
    except HTTPException:
        # Re-raise HTTPException to preserve status code
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Execution error: {str(e)}"
        )


@app.post("/execute-with-files")
async def execute_code_with_files(
    code: str = Form(..., description="Python code to execute"),
    timeout: Optional[int] = Form(None, description="Timeout (seconds)"),
    allow_network: Optional[bool] = Form(None, description="Allow internet access"),
    files: List[UploadFile] = File(default=[], description="List of files to upload")
):
    """
    Execute Python code with files uploaded via multipart/form-data
    
    Args:
        code: Python code to execute
        timeout: Timeout (seconds)
        files: List of uploaded files
    
    Returns:
        JSON response containing stdout, stderr, return_code and output_files
    """
    try:
        # Read uploaded files
        input_files = {}
        for upload_file in files:
            file_content = await upload_file.read()
            input_files[upload_file.filename] = file_content
        
        # Use value from request or default from env
        final_timeout = timeout if timeout is not None else DEFAULT_TIMEOUT
        final_allow_network = allow_network if allow_network is not None else DEFAULT_ALLOW_NETWORK
        
        # Execute code
        if final_timeout != DEFAULT_TIMEOUT or final_allow_network != DEFAULT_ALLOW_NETWORK:
            custom_executor = ExecutorFactory.create_executor(
                mode=EXECUTOR_MODE,
                timeout=final_timeout,
                max_output_size=1024 * 1024,
                allow_network=final_allow_network,
                memory_limit="128m",
                cpu_quota=50000,
                pids_limit=20,
                max_memory_mb=128,
                max_cpu_time=final_timeout
            )
            result = custom_executor.execute(code, input_files if input_files else None)
        else:
            result = executor.execute(code, input_files if input_files else None)
        
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Execution error: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "execution_mode": EXECUTOR_MODE,
        "config": {
            "default_timeout": DEFAULT_TIMEOUT,
            "default_allow_network": DEFAULT_ALLOW_NETWORK,
            "max_output_size": executor.max_output_size
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
