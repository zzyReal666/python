#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TestApp 学习模块
"""

import gradio as gr
from core.base_app import GradioApp
from typing import Dict, Any


class TestAppApp(GradioApp):
    """TestApp 应用"""
    
    # 这是 TestAppApp 类的构造函数（初始化方法），用于初始化父类 GradioApp，并设置应用的名称、描述和端口号
    def __init__(self):
        super().__init__(
            name="testapp",
            description="TestApp 学习模块",
            port=7860
        )
    def create_interface(self):
        """创建 Gradio 界面"""
        with gr.Blocks(title="TestApp 学习模块") as interface:
            gr.Markdown("# TestApp 学习模块")
            
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
                return f"处理结果: {text}"
            
            submit_btn.click(
                fn=process_input,
                inputs=[input_text],
                outputs=[output_text]
            )
        
        return interface
    
    def get_info(self) -> Dict[str, Any]:
        """获取应用信息"""
        return {
            "name": self.name,
            "description": self.description,
            "version": "1.0.0",
            "type": "gradio"
        }


# 应用实例
app = TestAppApp()

if __name__ == "__main__":
    app.run()
