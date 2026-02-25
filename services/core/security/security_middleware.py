import time
import logging
import os
from typing import Callable
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from services.core.security.input_sanitizer import InputSanitizer
from services.core.security.rate_limiter import rate_limiter
from services.core.security.secure_logger import secure_logger
from services.core.security.env_validator import EnvironmentValidator

class SecurityMiddleware(BaseHTTPMiddleware):
    """Comprehensive security middleware for the Executive Suite"""
    
    def __init__(self, app):
        super().__init__(app)
        self.logger = logging.getLogger(__name__)
        
        # Validate environment on startup
        env_check = EnvironmentValidator.validate_environment()
        if not env_check['valid']:
            self.logger.warning(f"Environment validation failed: {env_check}")
            # In development, we might want to be more strict
            if os.getenv('ENVIRONMENT') == 'development':
                # Optional: raise RuntimeError("Environment validation failed")
                pass
        
        if env_check['sensitive_exposed']:
            self.logger.warning(f"Sensitive variables may be exposed: {env_check['sensitive_exposed']}")
    
    async def dispatch(self, request: Request, call_next: Callable):
        """Process request through security middleware"""
        start_time = time.time()
        
        # Get client information
        client_ip = request.client.host if request.client else "unknown"
        
        # Rate limiting
        # Default limits: 1000 requests per hour
        if rate_limiter.is_rate_limited(client_ip, max_requests=1000, window_minutes=60):
            secure_logger.log_rate_limit_hit(
                client_ip, 
                str(request.url), 
                1000
            )
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "retry_after": rate_limiter.get_reset_time(client_ip).isoformat() if rate_limiter.get_reset_time(client_ip) else None
                }
            )
        
        # Input sanitization for mutation requests
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                # We need to be careful with reading the body as it consumes the stream
                # For FastAPI middleware, we can use the following pattern:
                body = await request.body()
                if body:
                    body_str = body.decode('utf-8')
                    
                    # Check for prompt injection
                    detection_result = InputSanitizer.detect_injection_attempt(body_str)
                    
                    if detection_result['is_suspicious']:
                        secure_logger.log_prompt_injection_attempt(
                            "anonymous",
                            client_ip,
                            body_str,
                            detection_result
                        )
                        
                        if detection_result['severity'] == 'HIGH':
                            return JSONResponse(
                                status_code=400,
                                content={
                                    "error": "Suspicious input detected",
                                    "message": "Your request contains potentially harmful content. Please rephrase your question."
                                }
                            )
                
                # Re-create the request with the body so subsequent handlers can read it
                # Note: This is an expensive operation in Starlette/FastAPI middleware.
                # A better approach for production would be a custom APIRoute class.
                # However, for this implementation, we follow the legacy pattern.
                async def receive():
                    return {"type": "http.request", "body": body}
                request._receive = receive

            except Exception as e:
                self.logger.error(f"Error in input sanitization: {e}")
        
        # Process request
        try:
            response = await call_next(request)
            
            # Log API access
            secure_logger.log_api_access(
                str(request.url),
                "anonymous", # Would be real user ID after auth
                client_ip,
                request.method,
                response.status_code
            )
            
            return response
            
        except HTTPException as e:
            secure_logger.log_api_access(
                str(request.url),
                "anonymous",
                client_ip,
                request.method,
                e.status_code
            )
            raise e
            
        except Exception as e:
            secure_logger.log_security_incident(
                "unexpected_error",
                "MEDIUM",
                {
                    "endpoint": str(request.url),
                    "method": request.method,
                    "error": str(e),
                    "client_ip": client_ip
                }
            )
            raise e
        
        finally:
            duration = time.time() - start_time
            if duration > 2.0: # Threshold for slow request logging
                self.logger.warning(f"Slow request: {request.url} took {duration:.2f}s")

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""
    
    async def dispatch(self, request: Request, call_next: Callable):
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Standard CSP for a React/FastAPI app
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "font-src 'self' data:; "
        )
        
        return response
