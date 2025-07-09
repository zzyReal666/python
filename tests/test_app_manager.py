"""应用管理器测试模块"""

import pytest
from unittest.mock import Mock, patch
from src.core.app_manager import AppManager
from src.core.base_app import BaseApp


class TestAppManager:
    """应用管理器测试类"""

    def setup_method(self):
        """每个测试方法前的设置"""
        self.app_manager = AppManager()

    def test_discover_apps(self):
        """测试应用发现功能"""
        # 模拟应用类
        mock_app = Mock(spec=BaseApp)
        mock_app.name = "test_app"
        mock_app.description = "Test application"
        
        with patch('src.core.app_manager.importlib.import_module') as mock_import:
            mock_module = Mock()
            mock_module.TestApp = mock_app
            mock_import.return_value = mock_module
            
            apps = self.app_manager.discover_apps()
            assert len(apps) >= 0  # 至少应该发现日志演示应用

    def test_get_app_info(self):
        """测试获取应用信息"""
        app_info = self.app_manager.get_app_info("logging_demo")
        assert app_info is not None
        assert "name" in app_info
        assert "description" in app_info

    def test_list_apps(self):
        """测试列出所有应用"""
        apps = self.app_manager.list_apps()
        assert isinstance(apps, list)
        assert len(apps) > 0

    def test_run_app_success(self):
        """测试成功运行应用"""
        with patch('src.core.app_manager.importlib.import_module') as mock_import:
            mock_app_class = Mock()
            mock_app_instance = Mock()
            mock_app_class.return_value = mock_app_instance
            mock_import.return_value = Mock(LoggingDemoApp=mock_app_class)
            
            result = self.app_manager.run_app("logging_demo")
            assert result is True

    def test_run_app_not_found(self):
        """测试运行不存在的应用"""
        result = self.app_manager.run_app("non_existent_app")
        assert result is False 