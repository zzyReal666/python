"""
基础测试

测试项目的基本功能。
"""

import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_root_endpoint():
    """测试根端点"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_health_check():
    """测试健康检查端点"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_health_live():
    """测试存活检查端点"""
    response = client.get("/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"


def test_health_ready():
    """测试就绪检查端点"""
    response = client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"


def test_metrics_endpoint():
    """测试指标端点"""
    response = client.get("/metrics")
    # 在生产环境中可能返回404，在开发环境中返回指标
    assert response.status_code in [200, 404]


def test_docs_endpoint():
    """测试文档端点"""
    response = client.get("/docs")
    # 在开发环境中应该返回200，在生产环境中可能返回404
    assert response.status_code in [200, 404]


def test_openapi_endpoint():
    """测试OpenAPI端点"""
    response = client.get("/openapi.json")
    # 在开发环境中应该返回200，在生产环境中可能返回404
    assert response.status_code in [200, 404] 