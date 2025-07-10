"""
结构化日志配置

使用structlog提供结构化日志记录，支持JSON格式和性能监控。
"""

import logging
import sys
import time
from typing import Any, Dict, Optional

import structlog
from structlog.stdlib import LoggerFactory

from .config import settings


def configure_logging() -> None:
    """配置结构化日志"""
    
    # 配置标准库日志
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.logging.level.upper()),
    )
    
    # 配置structlog
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
            structlog.processors.JSONRenderer() if settings.logging.format == "json" else structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """获取结构化日志记录器"""
    return structlog.get_logger(name)


class LoggerMixin:
    """日志记录器混入类"""
    
    @property
    def logger(self) -> structlog.stdlib.BoundLogger:
        """获取日志记录器"""
        return get_logger(self.__class__.__name__)


# 性能监控装饰器
def log_performance(logger_name: Optional[str] = None):
    """记录函数执行性能的装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            import time
            logger = get_logger(logger_name or func.__module__)
            
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                logger.info(
                    "function_executed",
                    function=func.__name__,
                    execution_time=execution_time,
                    status="success"
                )
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(
                    "function_failed",
                    function=func.__name__,
                    execution_time=execution_time,
                    error=str(e),
                    status="error"
                )
                raise
        
        return wrapper
    return decorator


# 异步性能监控装饰器
def log_async_performance(logger_name: Optional[str] = None):
    """记录异步函数执行性能的装饰器"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            import time
            logger = get_logger(logger_name or func.__module__)
            
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                execution_time = time.time() - start_time
                logger.info(
                    "async_function_executed",
                    function=func.__name__,
                    execution_time=execution_time,
                    status="success"
                )
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(
                    "async_function_failed",
                    function=func.__name__,
                    execution_time=execution_time,
                    error=str(e),
                    status="error"
                )
                raise
        
        return wrapper
    return decorator


# 请求日志中间件
class RequestLoggingMiddleware:
    """请求日志中间件"""
    
    def __init__(self, app):
        self.app = app
        self.logger = get_logger("request")
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            start_time = time.time()
            
            # 记录请求开始
            self.logger.info(
                "request_started",
                method=scope.get("method"),
                path=scope.get("path"),
                query_string=scope.get("query_string", b"").decode(),
                client=scope.get("client"),
            )
            
            # 处理请求
            await self.app(scope, receive, send)
            
            # 记录请求结束
            execution_time = time.time() - start_time
            self.logger.info(
                "request_finished",
                method=scope.get("method"),
                path=scope.get("path"),
                execution_time=execution_time,
            )
        else:
            await self.app(scope, receive, send)


# 初始化日志配置
configure_logging() 