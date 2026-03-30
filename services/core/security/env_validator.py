import os
from typing import Dict, List
import logging

class EnvironmentValidator:
    """Validates and manages environment variables securely"""
    
    REQUIRED_VARS = [
        'GOOGLE_CLOUD_PROJECT',
        # Add other critical vars here as the system evolves
    ]
    
    SENSITIVE_VARS = [
        'POSTGRES_PASSWORD',
        'GOOGLE_API_KEY',
        'DATABASE_URL',
        'STRIPE_SECRET_KEY',
        'HUBSPOT_ACCESS_TOKEN'
    ]
    
    @classmethod
    def validate_environment(cls) -> Dict[str, any]:
        """Validate all required environment variables are present"""
        missing = []
        sensitive_exposed = []
        
        for var in cls.REQUIRED_VARS:
            if not os.getenv(var):
                missing.append(var)
        
        for var in cls.SENSITIVE_VARS:
            # Check if sensitive variables are suspiciously short (likely placeholders)
            val = os.getenv(var)
            if val and len(val) < 10:
                sensitive_exposed.append(var)
        
        return {
            'valid': len(missing) == 0,
            'missing_vars': missing,
            'sensitive_exposed': sensitive_exposed
        }
    
    @classmethod
    def sanitize_logs(cls, data: str) -> str:
        """Remove sensitive data from logs"""
        sanitized_data = data
        for var in cls.SENSITIVE_VARS:
            val = os.getenv(var)
            if val:
                sanitized_data = sanitized_data.replace(val, f"[REDACTED_{var}]")
        return sanitized_data
    
    @classmethod
    def get_secure_env(cls, key: str, default: str = None) -> str:
        """Get environment variable with security checks"""
        value = os.getenv(key, default)
        
        if key in cls.SENSITIVE_VARS and value:
            # Mask sensitive value in trace-level logging if needed, 
            # for now just acknowledge access
            logging.debug(f"Accessing sensitive environment variable: {key}")
        
        return value
