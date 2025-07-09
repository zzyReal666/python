#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志工具模块
提供可重用的日志配置和工具函数
"""

import logging
import logging.handlers
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional

class LoggerConfig:
    """日志配置类"""
    
    def __init__(self, 
                 name: str = "AppLogger",
                 log_dir: str = "logs",
                 level: str = "INFO",
                 max_bytes: int = 1024*1024,  # 1MB
                 backup_count: int = 5,
                 console_output: bool = True,
                 file_output: bool = True):
        """
        初始化日志配置
        
        Args:
            name: 日志记录器名称
            log_dir: 日志文件目录
            level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            max_bytes: 单个日志文件最大大小
            backup_count: 备份文件数量
            console_output: 是否输出到控制台
            file_output: 是否输出到文件
        """
        self.name = name
        self.log_dir = log_dir
        self.level = getattr(logging, level.upper())
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.console_output = console_output
        self.file_output = file_output
        
        # 创建日志目录
        if self.file_output and not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # 配置日志记录器
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        
        # 清除已有的处理器
        logger.handlers.clear()
        
        # 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 控制台处理器
        if self.console_output:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.level)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        # 文件处理器
        if self.file_output:
            # 普通日志文件
            file_handler = logging.handlers.RotatingFileHandler(
                os.path.join(self.log_dir, f'{self.name.lower()}.log'),
                maxBytes=self.max_bytes,
                backupCount=self.backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(self.level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
            # 错误日志文件
            error_handler = logging.handlers.RotatingFileHandler(
                os.path.join(self.log_dir, f'{self.name.lower()}_error.log'),
                maxBytes=self.max_bytes,
                backupCount=self.backup_count,
                encoding='utf-8'
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(formatter)
            logger.addHandler(error_handler)
        
        return logger
    
    def get_logger(self) -> logging.Logger:
        """获取日志记录器"""
        return self.logger

class StructuredLogger:
    """结构化日志记录器"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def log_event(self, 
                  event_type: str,
                  message: str,
                  data: Optional[Dict[str, Any]] = None,
                  level: str = "INFO"):
        """
        记录结构化事件日志
        
        Args:
            event_type: 事件类型
            message: 事件消息
            data: 附加数据
            level: 日志级别
        """
        log_entry = {
            "event_type": event_type,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "data": data or {}
        }
        
        log_message = f"{event_type}: {message} | {json.dumps(log_entry, ensure_ascii=False)}"
        
        log_method = getattr(self.logger, level.lower())
        log_method(log_message)
    
    def log_user_action(self, user_id: str, action: str, details: str = ""):
        """记录用户操作日志"""
        self.log_event(
            event_type="USER_ACTION",
            message=f"用户 {user_id} 执行了 {action}",
            data={"user_id": user_id, "action": action, "details": details}
        )
    
    def log_api_call(self, endpoint: str, method: str, status_code: int, duration: float):
        """记录API调用日志"""
        level = "ERROR" if status_code >= 400 else "INFO"
        self.log_event(
            event_type="API_CALL",
            message=f"{method} {endpoint} - {status_code}",
            data={
                "endpoint": endpoint,
                "method": method,
                "status_code": status_code,
                "duration": duration
            },
            level=level
        )
    
    def log_performance(self, operation: str, duration: float, threshold: float = 1.0):
        """记录性能日志"""
        level = "WARNING" if duration > threshold else "INFO"
        self.log_event(
            event_type="PERFORMANCE",
            message=f"操作 {operation} 耗时 {duration:.3f}秒",
            data={"operation": operation, "duration": duration, "threshold": threshold},
            level=level
        )
    
    def log_error(self, error: Exception, context: str = ""):
        """记录错误日志"""
        self.log_event(
            event_type="ERROR",
            message=f"{context}: {str(error)}",
            data={
                "error_type": type(error).__name__,
                "error_message": str(error),
                "context": context
            },
            level="ERROR"
        )

# 便捷函数
def get_logger(name: str = "AppLogger", **kwargs) -> logging.Logger:
    """获取配置好的日志记录器"""
    config = LoggerConfig(name=name, **kwargs)
    return config.get_logger()

def get_structured_logger(name: str = "AppLogger", **kwargs) -> StructuredLogger:
    """获取结构化日志记录器"""
    logger = get_logger(name, **kwargs)
    return StructuredLogger(logger)

# 使用示例
if __name__ == "__main__":
    # 基本使用
    logger = get_logger("TestApp")
    logger.info("应用启动")
    logger.warning("这是一个警告")
    logger.error("这是一个错误")
    
    # 结构化日志使用
    struct_logger = get_structured_logger("TestApp")
    struct_logger.log_user_action("user123", "login", "用户登录成功")
    struct_logger.log_api_call("/api/users", "GET", 200, 0.5)
    struct_logger.log_performance("database_query", 2.5)
    
    try:
        raise ValueError("测试错误")
    except Exception as e:
        struct_logger.log_error(e, "测试上下文") 