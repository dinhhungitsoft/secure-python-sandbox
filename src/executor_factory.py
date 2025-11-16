"""
Executor Factory - Strategy Pattern Implementation
===================================================

Factory class to initialize executor strategies based on execution mode.
"""

from typing import Optional, Union, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from sandbox_executor.executors.sandbox_executor import SandboxExecutor
    from sandbox_executor.executors.secure_sandbox_executor import SecureSandboxExecutor


class ExecutorFactory:
    """Factory class to create executor instances using Strategy pattern"""
    
    @staticmethod
    def create_executor(
        mode: str,
        timeout: int = 30,
        max_output_size: int = 1024 * 1024,
        allow_network: bool = False,
        **kwargs
    ) -> Any:  # Changed from Union[DockerSandboxExecutor, SecureSandboxExecutor, SandboxExecutor]
        """
        Create executor instance based on mode
        
        Args:
            mode: Execution mode ('secure', 'simple')
            timeout: Timeout (seconds)
            max_output_size: Maximum output size (bytes)
            allow_network: Allow internet access
            **kwargs: Additional parameters for specific executor
        
        Returns:
            Executor instance
            
        Raises:
            ValueError: If mode is invalid
        """
        mode = mode.lower()
        
        if mode == "secure":
            return ExecutorFactory._create_secure_executor(
                timeout, max_output_size, allow_network, **kwargs
            )
        elif mode == "simple":
            return ExecutorFactory._create_simple_executor(
                timeout, max_output_size, allow_network
            )
        else:
            raise ValueError(f"Unknown execution mode: {mode}")
    
    
    @staticmethod
    def _create_secure_executor(
        timeout: int,
        max_output_size: int,
        allow_network: bool,
        **kwargs
    ) -> Any:  # Changed from SecureSandboxExecutor
        """Create Secure executor"""
        from sandbox_executor.executors.secure_sandbox_executor import SecureSandboxExecutor
        return SecureSandboxExecutor(
            timeout=timeout,
            max_output_size=max_output_size,
            allow_network=allow_network,
            max_memory_mb=kwargs.get("max_memory_mb", 128),
            max_cpu_time=kwargs.get("max_cpu_time", timeout)
        )
    
    @staticmethod
    def _create_simple_executor(
        timeout: int,
        max_output_size: int,
        allow_network: bool
    ) -> Any:  # Changed from SandboxExecutor
        """Create Simple executor"""
        from sandbox_executor.executors.sandbox_executor import SandboxExecutor
        return SandboxExecutor(
            timeout=timeout,
            max_output_size=max_output_size,
            allow_network=allow_network
        )
    
    @staticmethod
    def create_with_fallback(
        preferred_mode: str,
        fallback_mode: str = "secure",
        timeout: int = 30,
        max_output_size: int = 1024 * 1024,
        allow_network: bool = False,
        **kwargs
    ) -> tuple[Any, str]:  # Changed from tuple[Union[...], str]
        """
        Create executor with fallback mechanism
        
        Args:
            preferred_mode: Preferred mode
            fallback_mode: Fallback mode if preferred_mode fails
            timeout: Timeout (seconds)
            max_output_size: Maximum output size (bytes)
            allow_network: Allow internet access
            **kwargs: Additional parameters
        
        Returns:
            Tuple (executor instance, actual mode used)
        """
        try:
            executor = ExecutorFactory.create_executor(
                preferred_mode, timeout, max_output_size, allow_network, **kwargs
            )
            return executor, preferred_mode
        except Exception as e:
            print(f"⚠️  {preferred_mode.capitalize()} mode not available: {e}")
            print(f"   Falling back to {fallback_mode} mode")
            
            try:
                executor = ExecutorFactory.create_executor(
                    fallback_mode, timeout, max_output_size, allow_network, **kwargs
                )
                return executor, fallback_mode
            except Exception as fallback_error:
                # Final fallback to secure mode
                print(f"⚠️  {fallback_mode.capitalize()} mode also failed: {fallback_error}")
                print("   Using secure mode as final fallback")
                executor = ExecutorFactory.create_executor(
                    "secure", timeout, max_output_size, allow_network, **kwargs
                )
                return executor, "secure"
