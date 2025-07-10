"""
应用配置管理

使用Pydantic Settings管理应用配置，支持环境变量和配置文件。
"""

import os
from functools import lru_cache
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """数据库配置"""
    
    url: str = Field(default="", env="DATABASE_URL")
    pool_size: int = Field(default=20, env="DATABASE_POOL_SIZE")
    max_overflow: int = Field(default=30, env="DATABASE_MAX_OVERFLOW")
    echo: bool = Field(default=False, env="DATABASE_ECHO")
    
    class Config:
        env_prefix = "DATABASE_"


class RedisSettings(BaseSettings):
    """Redis配置"""
    
    url: str = Field(..., env="REDIS_URL")
    pool_size: int = Field(10, env="REDIS_POOL_SIZE")
    decode_responses: bool = Field(True, env="REDIS_DECODE_RESPONSES")
    
    class Config:
        env_prefix = "REDIS_"


class SecuritySettings(BaseSettings):
    """安全配置"""
    
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field("HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    
    class Config:
        env_prefix = "SECURITY_"


class JWTSettings(BaseSettings):
    """JWT配置"""
    
    secret_key: str = Field(..., env="JWT_SECRET_KEY")
    algorithm: str = Field("HS256", env="JWT_ALGORITHM")
    
    class Config:
        env_prefix = "JWT_"


class LoggingSettings(BaseSettings):
    """日志配置"""
    
    level: str = Field("INFO", env="LOG_LEVEL")
    format: str = Field("json", env="LOG_FORMAT")
    
    class Config:
        env_prefix = "LOG_"


class MonitoringSettings(BaseSettings):
    """监控配置"""
    
    sentry_dsn: Optional[str] = Field(None, env="SENTRY_DSN")
    prometheus_enabled: bool = Field(True, env="PROMETHEUS_ENABLED")
    
    class Config:
        env_prefix = "MONITORING_"


class CelerySettings(BaseSettings):
    """Celery配置"""
    
    broker_url: str = Field(..., env="CELERY_BROKER_URL")
    result_backend: str = Field(..., env="CELERY_RESULT_BACKEND")
    task_serializer: str = Field("json", env="CELERY_TASK_SERIALIZER")
    result_serializer: str = Field("json", env="CELERY_RESULT_SERIALIZER")
    accept_content: List[str] = Field(["json"], env="CELERY_ACCEPT_CONTENT")
    timezone: str = Field("UTC", env="CELERY_TIMEZONE")
    enable_utc: bool = Field(True, env="CELERY_ENABLE_UTC")
    
    class Config:
        env_prefix = "CELERY_"


class CORSettings(BaseSettings):
    """CORS配置"""
    
    origins: List[str] = Field(["http://localhost:3000"], env="CORS_ORIGINS")
    allow_credentials: bool = Field(True, env="CORS_ALLOW_CREDENTIALS")
    allow_methods: List[str] = Field(["*"], env="CORS_ALLOW_METHODS")
    allow_headers: List[str] = Field(["*"], env="CORS_ALLOW_HEADERS")
    
    @validator("origins", pre=True)
    def parse_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    class Config:
        env_prefix = "CORS_"


class RateLimitSettings(BaseSettings):
    """限流配置"""
    
    enabled: bool = Field(True, env="RATE_LIMIT_ENABLED")
    requests: int = Field(100, env="RATE_LIMIT_REQUESTS")
    window: int = Field(60, env="RATE_LIMIT_WINDOW")
    
    class Config:
        env_prefix = "RATE_LIMIT_"


class Settings(BaseSettings):
    """应用主配置"""
    
    # 基础配置
    app_name: str = Field("LLM-Learn", env="APP_NAME")
    app_version: str = Field("0.1.0", env="APP_VERSION")
    debug: bool = Field(False, env="DEBUG")
    environment: str = Field("production", env="ENVIRONMENT")
    
    # 服务器配置
    host: str = Field("0.0.0.0", env="HOST")
    port: int = Field(8000, env="PORT")
    workers: int = Field(4, env="WORKERS")
    
    # 子配置
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    security: SecuritySettings = SecuritySettings()
    jwt: JWTSettings = JWTSettings()
    logging: LoggingSettings = LoggingSettings()
    monitoring: MonitoringSettings = MonitoringSettings()
    celery: CelerySettings = CelerySettings()
    cors: CORSettings = CORSettings()
    rate_limit: RateLimitSettings = RateLimitSettings()
    
    # 外部API配置
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(None, env="ANTHROPIC_API_KEY")
    
    # 文件存储配置
    storage_type: str = Field("local", env="STORAGE_TYPE")
    storage_path: str = Field("./storage", env="STORAGE_PATH")
    
    # AWS配置
    aws_access_key_id: Optional[str] = Field(None, env="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: Optional[str] = Field(None, env="AWS_SECRET_ACCESS_KEY")
    aws_region: str = Field("us-east-1", env="AWS_REGION")
    aws_s3_bucket: Optional[str] = Field(None, env="AWS_S3_BUCKET")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @property
    def is_development(self) -> bool:
        """是否为开发环境"""
        return self.environment.lower() in ["development", "dev", "local"]
    
    @property
    def is_production(self) -> bool:
        """是否为生产环境"""
        return self.environment.lower() in ["production", "prod"]
    
    @property
    def is_testing(self) -> bool:
        """是否为测试环境"""
        return self.environment.lower() in ["testing", "test"]


@lru_cache()
def get_settings() -> Settings:
    """获取应用配置单例"""
    return Settings()


# 全局配置实例
settings = get_settings() 