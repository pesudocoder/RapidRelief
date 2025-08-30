import structlog
import sys
import logging
from datetime import datetime
from typing import Any, Dict


def setup_logging(log_level: str = "INFO") -> None:
    """Setup structured JSON logging for the application"""
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper()),
    )


def get_logger(name: str = None) -> structlog.BoundLogger:
    """Get a structured logger instance"""
    return structlog.get_logger(name)


class LogContext:
    """Context manager for adding context to log entries"""
    
    def __init__(self, logger: structlog.BoundLogger, **context):
        self.logger = logger
        self.context = context
    
    def __enter__(self):
        return self.logger.bind(**self.context)
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def log_api_request(logger: structlog.BoundLogger, method: str, path: str, 
                   request_id: str, user_id: str = None, **kwargs) -> None:
    """Log API request details"""
    logger.info(
        "API request",
        method=method,
        path=path,
        request_id=request_id,
        user_id=user_id,
        **kwargs
    )


def log_api_response(logger: structlog.BoundLogger, method: str, path: str,
                    request_id: str, status_code: int, response_time_ms: float,
                    user_id: str = None, **kwargs) -> None:
    """Log API response details"""
    logger.info(
        "API response",
        method=method,
        path=path,
        request_id=request_id,
        status_code=status_code,
        response_time_ms=response_time_ms,
        user_id=user_id,
        **kwargs
    )


def log_workflow_step(logger: structlog.BoundLogger, workflow_id: str, 
                     step_name: str, status: str, **kwargs) -> None:
    """Log workflow step execution"""
    logger.info(
        "Workflow step",
        workflow_id=workflow_id,
        step_name=step_name,
        status=status,
        **kwargs
    )


def log_granite_request(logger: structlog.BoundLogger, operation: str, 
                       model: str, tokens_used: int = None, **kwargs) -> None:
    """Log Granite API requests"""
    logger.info(
        "Granite API request",
        operation=operation,
        model=model,
        tokens_used=tokens_used,
        **kwargs
    )


def log_database_operation(logger: structlog.BoundLogger, operation: str,
                          table: str, record_id: str = None, **kwargs) -> None:
    """Log database operations"""
    logger.info(
        "Database operation",
        operation=operation,
        table=table,
        record_id=record_id,
        **kwargs
    )


def log_error(logger: structlog.BoundLogger, error: Exception, 
              context: Dict[str, Any] = None, **kwargs) -> None:
    """Log error with context"""
    logger.error(
        "Application error",
        error_type=type(error).__name__,
        error_message=str(error),
        context=context or {},
        **kwargs
    )
