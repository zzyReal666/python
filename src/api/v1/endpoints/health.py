"""
健康检查API端点

提供应用健康状态检查功能。
"""

from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ....core.database import get_db
from ....core.cache import cache
from ....core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """健康检查端点"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "llm-learn-api",
    }


@router.get("/health/detailed")
async def detailed_health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """详细健康检查端点"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "llm-learn-api",
        "components": {
            "database": "unknown",
            "cache": "unknown",
        }
    }
    
    # 检查数据库连接
    try:
        db.execute("SELECT 1")
        health_status["components"]["database"] = "healthy"
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        health_status["components"]["database"] = "unhealthy"
        health_status["status"] = "degraded"
    
    # 检查缓存连接
    try:
        await cache.set("health_check", "ok", expire=60)
        result = await cache.get("health_check")
        if result == "ok":
            health_status["components"]["cache"] = "healthy"
        else:
            health_status["components"]["cache"] = "unhealthy"
            health_status["status"] = "degraded"
    except Exception as e:
        logger.error("Cache health check failed", error=str(e))
        health_status["components"]["cache"] = "unhealthy"
        health_status["status"] = "degraded"
    
    return health_status


@router.get("/health/ready")
async def readiness_check() -> Dict[str, Any]:
    """就绪检查端点"""
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/health/live")
async def liveness_check() -> Dict[str, Any]:
    """存活检查端点"""
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat(),
    } 