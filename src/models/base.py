"""
基础数据模型

包含所有模型的基础类和通用字段。
"""

from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declared_attr
from pydantic import BaseModel, Field

from ..core.database import Base


class BaseModelMixin:
    """基础模型混入类"""
    
    @declared_attr
    def __tablename__(cls) -> str:
        """自动生成表名"""
        return cls.__name__.lower()
    
    # 通用字段
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def update(self, **kwargs) -> None:
        """更新字段"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class TimestampMixin:
    """时间戳混入类"""
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class SoftDeleteMixin:
    """软删除混入类"""
    
    deleted_at = Column(DateTime, nullable=True)
    is_deleted = Column(String(1), default="N", nullable=False)  # Y/N
    
    def soft_delete(self) -> None:
        """软删除"""
        self.deleted_at = datetime.utcnow()
        self.is_deleted = "Y"
    
    def restore(self) -> None:
        """恢复"""
        self.deleted_at = None
        self.is_deleted = "N"


# Pydantic基础模型
class BaseSchema(BaseModel):
    """Pydantic基础模型"""
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TimestampSchema(BaseSchema):
    """时间戳Pydantic模型"""
    
    created_at: Optional[datetime] = Field(None, description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class PaginationSchema(BaseSchema):
    """分页Pydantic模型"""
    
    page: int = Field(1, ge=1, description="页码")
    size: int = Field(10, ge=1, le=100, description="每页大小")
    total: Optional[int] = Field(None, description="总记录数")
    pages: Optional[int] = Field(None, description="总页数")


class ResponseSchema(BaseSchema):
    """响应Pydantic模型"""
    
    code: int = Field(200, description="状态码")
    message: str = Field("success", description="消息")
    data: Optional[Any] = Field(None, description="数据") 