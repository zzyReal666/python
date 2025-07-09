#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用基类
为所有学习模块提供统一的接口和基础功能
"""

import abc
import logging
from typing import Dict, Any, Optional
from pathlib import Path


class BaseApp(abc.ABC):
    """应用基类，所有学习模块都应该继承此类"""
    
    def __init__(self, name: str, description: str = ""):
        """
        初始化应用
        
        Args:
            name: 应用名称
            description: 应用描述
        """
        self.name = name
        self.description = description
        self.logger = self._setup_logger()
        self.config = self._load_config()
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger(f"app.{self.name}")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        config_path = Path("config") / f"{self.name}.json"
        if config_path.exists():
            import json
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    @abc.abstractmethod
    def run(self, **kwargs) -> None:
        """
        运行应用的主方法
        
        Args:
            **kwargs: 运行参数
        """
        pass
    
    @abc.abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """
        获取应用信息
        
        Returns:
            包含应用信息的字典
        """
        return {
            "name": self.name,
            "description": self.description,
            "version": "1.0.0"
        }
    
    def setup(self) -> None:
        """应用初始化设置"""
        self.logger.info(f"初始化应用: {self.name}")
    
    def cleanup(self) -> None:
        """应用清理"""
        self.logger.info(f"清理应用: {self.name}")


class GradioApp(BaseApp):
    """Gradio 应用基类"""
    
    def __init__(self, name: str, description: str = "", port: int = 7860):
        super().__init__(name, description)
        self.port = port
        self.app = None
    
    def create_interface(self):
        """创建 Gradio 界面，子类需要实现此方法"""
        raise NotImplementedError("子类必须实现 create_interface 方法")
    
    def run(self, **kwargs) -> None:
        """运行 Gradio 应用"""
        try:
            import gradio as gr
            self.app = self.create_interface()
            self.logger.info(f"启动 {self.name} 应用，端口: {self.port}")
            self.app.launch(
                server_port=self.port,
                share=False,
                **kwargs
            )
        except ImportError:
            self.logger.error("Gradio 未安装，请运行: pip install gradio")
        except Exception as e:
            self.logger.error(f"启动应用失败: {e}")


class ConsoleApp(BaseApp):
    """控制台应用基类"""
    
    def run(self, **kwargs) -> None:
        """运行控制台应用"""
        self.logger.info(f"启动控制台应用: {self.name}")
        self.run_console(**kwargs)
    
    @abc.abstractmethod
    def run_console(self, **kwargs) -> None:
        """控制台应用的主要逻辑，子类需要实现"""
        pass 