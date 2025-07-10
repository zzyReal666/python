"""日志演示应用测试模块"""

from unittest.mock import Mock, patch

import pytest

from src.apps.logging_demo import LoggingDemoApp


class TestLoggingDemoApp:
    """日志演示应用测试类"""

    def setup_method(self):
        """每个测试方法前的设置"""
        self.app = LoggingDemoApp()

    def test_app_initialization(self):
        """测试应用初始化"""
        assert self.app.name == "日志演示应用"
        assert "日志" in self.app.description
        assert self.app.app_type == "gradio"

    def test_create_interface(self):
        """测试创建 Gradio 界面"""
        interface = self.app.create_interface()
        assert interface is not None

    @pytest.mark.integration
    def test_greeting_function(self):
        """测试问候功能"""
        result = self.app.greeting("张三")
        assert "张三" in result
        assert "欢迎" in result

    @pytest.mark.integration
    def test_calculator_function(self):
        """测试计算器功能"""
        result = self.app.calculator("2 + 3")
        assert result == "2 + 3 = 5"

        result = self.app.calculator("10 * 5")
        assert result == "10 * 5 = 50"

    @pytest.mark.integration
    def test_text_analysis_function(self):
        """测试文本分析功能"""
        result = self.app.text_analysis("这是一个测试文本")
        assert "字符数" in result
        assert "词数" in result

    @pytest.mark.integration
    def test_sentiment_analysis_function(self):
        """测试情感分析功能"""
        result = self.app.sentiment_analysis("我很开心")
        assert "情感" in result

        result = self.app.sentiment_analysis("我很伤心")
        assert "情感" in result

    def test_log_level_test(self):
        """测试日志级别测试功能"""
        result = self.app.log_level_test("DEBUG", "测试调试信息")
        assert "DEBUG" in result

    def test_log_management(self):
        """测试日志管理功能"""
        result = self.app.log_management("查看日志")
        assert "日志" in result
