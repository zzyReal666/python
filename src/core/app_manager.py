#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用管理器
管理所有学习模块的注册、发现和运行
"""

import importlib
import inspect
from typing import Dict, List, Type, Optional
from pathlib import Path
import logging

from .base_app import BaseApp


class AppManager:
    """应用管理器"""
    
    def __init__(self):
        self.apps: Dict[str, Type[BaseApp]] = {}
        self.logger = logging.getLogger("app_manager")
        self._discover_apps()
    
    def _discover_apps(self) -> None:
        """自动发现所有应用"""
        apps_dir = Path(__file__).parent.parent / "apps"
        
        for app_file in apps_dir.glob("*.py"):
            if app_file.name.startswith("__"):
                continue
                
            try:
                # 动态导入模块
                module_name = f"apps.{app_file.stem}"
                module = importlib.import_module(module_name)
                
                # 查找继承自 BaseApp 的类
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, BaseApp) and 
                        obj != BaseApp):
                        self.register_app(name, obj)
                        self.logger.info(f"发现应用: {name}")
                        
            except Exception as e:
                self.logger.warning(f"加载应用 {app_file.name} 失败: {e}")
    
    def register_app(self, name: str, app_class: Type[BaseApp]) -> None:
        """
        注册应用
        
        Args:
            name: 应用名称
            app_class: 应用类
        """
        self.apps[name] = app_class
        self.logger.info(f"注册应用: {name}")
    
    def get_app(self, name: str) -> Optional[Type[BaseApp]]:
        """
        获取应用类
        
        Args:
            name: 应用名称
            
        Returns:
            应用类或 None
        """
        return self.apps.get(name)
    
    def list_apps(self) -> List[Dict[str, str]]:
        """
        列出所有应用
        
        Returns:
            应用信息列表
        """
        app_list = []
        for name, app_class in self.apps.items():
            # 创建临时实例获取信息
            try:
                temp_app = app_class()
                info = temp_app.get_info()
                app_list.append({
                    "name": name,
                    "description": info.get("description", ""),
                    "version": info.get("version", "1.0.0")
                })
            except Exception as e:
                self.logger.warning(f"获取应用 {name} 信息失败: {e}")
                app_list.append({
                    "name": name,
                    "description": "获取信息失败",
                    "version": "unknown"
                })
        
        return app_list
    
    def run_app(self, name: str, **kwargs) -> None:
        """
        运行指定应用
        
        Args:
            name: 应用名称
            **kwargs: 运行参数
        """
        app_class = self.get_app(name)
        if not app_class:
            self.logger.error(f"应用 {name} 不存在")
            return
        
        try:
            # 直接实例化应用类
            app = app_class()
            app.setup()
            app.run(**kwargs)
        except KeyboardInterrupt:
            self.logger.info(f"应用 {name} 被用户中断")
        except Exception as e:
            self.logger.error(f"运行应用 {name} 失败: {e}")
        finally:
            try:
                app.cleanup()
            except:
                pass
    
    def create_app_template(self, name: str, app_type: str = "gradio") -> None:
        """
        创建新应用模板
        
        Args:
            name: 应用名称
            app_type: 应用类型 (gradio/console)
        """
        apps_dir = Path(__file__).parent.parent / "apps"
        template_file = apps_dir / f"{name.lower()}_app.py"
        
        if template_file.exists():
            self.logger.error(f"应用文件 {template_file} 已存在")
            return
        
        if app_type == "gradio":
            template = self._get_gradio_template(name)
        else:
            template = self._get_console_template(name)
        
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(template)
        
        self.logger.info(f"创建应用模板: {template_file}")
    
    def _get_gradio_template(self, name: str) -> str:
        """获取 Gradio 应用模板"""
        return f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{name} 学习模块
"""

import gradio as gr
from core.base_app import GradioApp


class {name}App(GradioApp):
    """{name} 应用"""
    
    def __init__(self):
        super().__init__(
            name="{name.lower()}",
            description="{name} 学习模块",
            port=7860
        )
    
    def create_interface(self):
        """创建 Gradio 界面"""
        with gr.Blocks(title="{name} 学习模块") as interface:
            gr.Markdown("# {name} 学习模块")
            
            with gr.Row():
                with gr.Column():
                    input_text = gr.Textbox(
                        label="输入",
                        placeholder="请输入内容..."
                    )
                    submit_btn = gr.Button("提交")
                
                with gr.Column():
                    output_text = gr.Textbox(
                        label="输出",
                        interactive=False
                    )
            
            def process_input(text):
                # 在这里实现您的业务逻辑
                return f"处理结果: {{text}}"
            
            submit_btn.click(
                fn=process_input,
                inputs=[input_text],
                outputs=[output_text]
            )
        
        return interface


# 应用实例
app = {name}App()

if __name__ == "__main__":
    app.run()
'''
    
    def _get_console_template(self, name: str) -> str:
        """获取控制台应用模板"""
        return f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{name} 学习模块
"""

from core.base_app import ConsoleApp


class {name}App(ConsoleApp):
    """{name} 应用"""
    
    def __init__(self):
        super().__init__(
            name="{name.lower()}",
            description="{name} 学习模块"
        )
    
    def run_console(self, **kwargs):
        """控制台应用的主要逻辑"""
        self.logger.info("开始运行 {name} 应用")
        
        # 在这里实现您的业务逻辑
        print(f"欢迎使用 {{name}} 学习模块!")
        
        # 示例：交互式输入
        user_input = input("请输入一些内容: ")
        print(f"您输入的内容是: {{user_input}}")
        
        self.logger.info("应用运行完成")


# 应用实例
app = {name}App()

if __name__ == "__main__":
    app.run()
'''


# 全局应用管理器实例
app_manager = AppManager() 