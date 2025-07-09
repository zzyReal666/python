#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 日志模块演示
展示日志系统的配置和使用方法
"""

import logging
import logging.handlers
import os
from datetime import datetime
from typing import Dict, Any
import gradio as gr

from core.base_app import GradioApp

# 创建日志目录
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


class LoggingDemoApp(GradioApp):
    """日志演示应用"""
    
    def __init__(self):
        super().__init__(
            name="logging_demo",
            description="Python 日志模块演示",
            port=7862
        )
        self.setup_logging()
    
    def setup_logging(self):
        """配置日志系统"""
        # 创建根日志记录器
        self.logger = logging.getLogger('LLMDemo')
        self.logger.setLevel(logging.DEBUG)
        
        # 清除已有的处理器
        self.logger.handlers.clear()
        
        # 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 1. 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # 2. 文件处理器 - 普通日志
        file_handler = logging.FileHandler(
            os.path.join(log_dir, 'app.log'),
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # 3. 文件处理器 - 错误日志
        error_handler = logging.FileHandler(
            os.path.join(log_dir, 'error.log'),
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        self.logger.addHandler(error_handler)
        
        # 4. 轮转文件处理器 - 按大小轮转
        rotating_handler = logging.handlers.RotatingFileHandler(
            os.path.join(log_dir, 'rotating.log'),
            maxBytes=1024*1024,  # 1MB
            backupCount=5,
            encoding='utf-8'
        )
        rotating_handler.setLevel(logging.INFO)
        rotating_handler.setFormatter(formatter)
        self.logger.addHandler(rotating_handler)
        
        # 5. 时间轮转处理器 - 按时间轮转
        timed_handler = logging.handlers.TimedRotatingFileHandler(
            os.path.join(log_dir, 'timed.log'),
            when='midnight',
            interval=1,
            backupCount=7,
            encoding='utf-8'
        )
        timed_handler.setLevel(logging.WARNING)
        timed_handler.setFormatter(formatter)
        self.logger.addHandler(timed_handler)
    
    def demo_basic_logging(self, message):
        """演示基本日志记录"""
        if not message.strip():
            return "请输入日志消息"
        
        try:
            # 不同级别的日志
            self.logger.debug(f"调试信息: {message}")
            self.logger.info(f"一般信息: {message}")
            self.logger.warning(f"警告信息: {message}")
            self.logger.error(f"错误信息: {message}")
            self.logger.critical(f"严重错误: {message}")
            
            return f"✅ 已记录日志消息: {message}\n\n日志级别: DEBUG, INFO, WARNING, ERROR, CRITICAL"
        
        except Exception as e:
            return f"❌ 记录日志时出错: {str(e)}"
    
    def demo_structured_logging(self, user_id, action, details):
        """演示结构化日志记录"""
        if not all([user_id, action, details]):
            return "请填写所有字段"
        
        try:
            # 结构化日志数据
            log_data = {
                "user_id": user_id,
                "action": action,
                "details": details,
                "timestamp": datetime.now().isoformat(),
                "session_id": f"session_{hash(user_id) % 10000}"
            }
            
            # 记录结构化日志
            self.logger.info(f"用户操作: {log_data}")
            
            return f"✅ 结构化日志已记录:\n{self._format_dict(log_data)}"
        
        except Exception as e:
            return f"❌ 记录结构化日志时出错: {str(e)}"
    
    def demo_error_logging(self, error_type, error_message):
        """演示错误日志记录"""
        if not error_message.strip():
            return "请输入错误信息"
        
        try:
            # 模拟不同类型的错误
            if error_type == "ValueError":
                raise ValueError(error_message)
            elif error_type == "TypeError":
                raise TypeError(error_message)
            elif error_type == "RuntimeError":
                raise RuntimeError(error_message)
            else:
                raise Exception(error_message)
        
        except Exception as e:
            # 记录错误日志
            self.logger.error(f"捕获到错误: {type(e).__name__}: {str(e)}", exc_info=True)
            return f"✅ 错误日志已记录:\n错误类型: {type(e).__name__}\n错误信息: {str(e)}"
    
    def demo_performance_logging(self, operation, duration):
        """演示性能日志记录"""
        if not operation.strip():
            return "请输入操作名称"
        
        try:
            duration = float(duration)
            
            # 性能日志
            if duration < 1.0:
                self.logger.info(f"操作 '{operation}' 完成，耗时: {duration:.3f}秒")
            elif duration < 5.0:
                self.logger.warning(f"操作 '{operation}' 较慢，耗时: {duration:.3f}秒")
            else:
                self.logger.error(f"操作 '{operation}' 超时，耗时: {duration:.3f}秒")
            
            return f"✅ 性能日志已记录:\n操作: {operation}\n耗时: {duration:.3f}秒"
        
        except ValueError:
            return "❌ 请输入有效的数字作为耗时"
        except Exception as e:
            return f"❌ 记录性能日志时出错: {str(e)}"
    
    def demo_log_levels(self):
        """演示不同日志级别"""
        try:
            messages = []
            
            # 测试所有日志级别
            self.logger.debug("这是一条调试信息")
            messages.append("DEBUG: 这是一条调试信息")
            
            self.logger.info("这是一条一般信息")
            messages.append("INFO: 这是一条一般信息")
            
            self.logger.warning("这是一条警告信息")
            messages.append("WARNING: 这是一条警告信息")
            
            self.logger.error("这是一条错误信息")
            messages.append("ERROR: 这是一条错误信息")
            
            self.logger.critical("这是一条严重错误信息")
            messages.append("CRITICAL: 这是一条严重错误信息")
            
            return "✅ 所有日志级别测试完成:\n" + "\n".join(messages)
        
        except Exception as e:
            return f"❌ 测试日志级别时出错: {str(e)}"
    
    def get_log_files(self):
        """获取日志文件列表"""
        try:
            log_files = []
            for file in os.listdir(log_dir):
                if file.endswith('.log'):
                    file_path = os.path.join(log_dir, file)
                    size = os.path.getsize(file_path)
                    modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                    log_files.append(f"📄 {file} ({size} bytes, 修改时间: {modified.strftime('%Y-%m-%d %H:%M:%S')})")
            
            if log_files:
                return "📁 日志文件列表:\n" + "\n".join(log_files)
            else:
                return "📁 暂无日志文件"
        
        except Exception as e:
            return f"❌ 获取日志文件列表时出错: {str(e)}"
    
    def clear_logs(self):
        """清空日志文件"""
        try:
            cleared_files = []
            for file in os.listdir(log_dir):
                if file.endswith('.log'):
                    file_path = os.path.join(log_dir, file)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write('')
                    cleared_files.append(file)
            
            if cleared_files:
                return f"✅ 已清空以下日志文件:\n" + "\n".join(cleared_files)
            else:
                return "📁 没有找到日志文件"
        
        except Exception as e:
            return f"❌ 清空日志文件时出错: {str(e)}"
    
    def _format_dict(self, data):
        """格式化字典输出"""
        return "\n".join([f"  {k}: {v}" for k, v in data.items()])
    
    def get_info(self) -> Dict[str, Any]:
        """获取应用信息"""
        return {
            "name": self.name,
            "description": self.description,
            "version": "1.0.0",
            "type": "gradio"
        }
    
    def create_interface(self):
        """创建 Gradio 界面"""
        with gr.Blocks(title="Python 日志模块演示") as interface:
            gr.Markdown("# 📝 Python 日志模块演示")
            gr.Markdown("这个演示展示了 Python 日志系统的各种功能和使用方法。")
            
            with gr.Tabs():
                # 基本日志记录
                with gr.TabItem("📋 基本日志记录"):
                    gr.Markdown("### 基本日志记录演示")
                    gr.Markdown("输入消息，系统会以不同级别记录日志。")
                    
                    with gr.Row():
                        with gr.Column():
                            basic_input = gr.Textbox(
                                label="日志消息",
                                placeholder="请输入要记录的日志消息...",
                                lines=3
                            )
                            basic_btn = gr.Button("记录日志", variant="primary")
                        
                        with gr.Column():
                            basic_output = gr.Textbox(
                                label="结果",
                                lines=8,
                                interactive=False
                            )
                    
                    basic_btn.click(
                        fn=self.demo_basic_logging,
                        inputs=[basic_input],
                        outputs=[basic_output]
                    )
                
                # 结构化日志
                with gr.TabItem("🏗️ 结构化日志"):
                    gr.Markdown("### 结构化日志记录演示")
                    gr.Markdown("记录包含结构化数据的日志信息。")
                    
                    with gr.Row():
                        with gr.Column():
                            user_id = gr.Textbox(label="用户ID", placeholder="user123")
                            action = gr.Textbox(label="操作", placeholder="login")
                            details = gr.Textbox(
                                label="详细信息",
                                placeholder="用户登录系统",
                                lines=2
                            )
                            structured_btn = gr.Button("记录结构化日志", variant="primary")
                        
                        with gr.Column():
                            structured_output = gr.Textbox(
                                label="结果",
                                lines=8,
                                interactive=False
                            )
                    
                    structured_btn.click(
                        fn=self.demo_structured_logging,
                        inputs=[user_id, action, details],
                        outputs=[structured_output]
                    )
                
                # 错误日志
                with gr.TabItem("❌ 错误日志"):
                    gr.Markdown("### 错误日志记录演示")
                    gr.Markdown("模拟不同类型的错误并记录错误日志。")
                    
                    with gr.Row():
                        with gr.Column():
                            error_type = gr.Dropdown(
                                choices=["ValueError", "TypeError", "RuntimeError", "Exception"],
                                label="错误类型",
                                value="ValueError"
                            )
                            error_message = gr.Textbox(
                                label="错误信息",
                                placeholder="这是一个错误信息",
                                lines=2
                            )
                            error_btn = gr.Button("模拟错误", variant="primary")
                        
                        with gr.Column():
                            error_output = gr.Textbox(
                                label="结果",
                                lines=8,
                                interactive=False
                            )
                    
                    error_btn.click(
                        fn=self.demo_error_logging,
                        inputs=[error_type, error_message],
                        outputs=[error_output]
                    )
                
                # 性能日志
                with gr.TabItem("⚡ 性能日志"):
                    gr.Markdown("### 性能日志记录演示")
                    gr.Markdown("记录操作耗时，根据耗时级别记录不同级别的日志。")
                    
                    with gr.Row():
                        with gr.Column():
                            operation = gr.Textbox(
                                label="操作名称",
                                placeholder="数据库查询"
                            )
                            duration = gr.Number(
                                label="耗时（秒）",
                                value=1.5,
                                minimum=0.1,
                                maximum=100.0
                            )
                            perf_btn = gr.Button("记录性能日志", variant="primary")
                        
                        with gr.Column():
                            perf_output = gr.Textbox(
                                label="结果",
                                lines=6,
                                interactive=False
                            )
                    
                    perf_btn.click(
                        fn=self.demo_performance_logging,
                        inputs=[operation, duration],
                        outputs=[perf_output]
                    )
                
                # 日志级别测试
                with gr.TabItem("🔍 日志级别测试"):
                    gr.Markdown("### 日志级别测试")
                    gr.Markdown("测试所有日志级别的记录。")
                    
                    with gr.Row():
                        level_btn = gr.Button("测试所有日志级别", variant="primary")
                        level_output = gr.Textbox(
                            label="结果",
                            lines=10,
                            interactive=False
                        )
                    
                    level_btn.click(
                        fn=self.demo_log_levels,
                        inputs=[],
                        outputs=[level_output]
                    )
                
                # 日志管理
                with gr.TabItem("📁 日志管理"):
                    gr.Markdown("### 日志文件管理")
                    gr.Markdown("查看和管理日志文件。")
                    
                    with gr.Row():
                        with gr.Column():
                            list_btn = gr.Button("查看日志文件", variant="primary")
                            clear_btn = gr.Button("清空日志文件", variant="secondary")
                        
                        with gr.Column():
                            manage_output = gr.Textbox(
                                label="结果",
                                lines=10,
                                interactive=False
                            )
                    
                    list_btn.click(
                        fn=self.get_log_files,
                        inputs=[],
                        outputs=[manage_output]
                    )
                    
                    clear_btn.click(
                        fn=self.clear_logs,
                        inputs=[],
                        outputs=[manage_output]
                    )
            
            gr.Markdown("---")
            gr.Markdown("### 📚 学习要点")
            gr.Markdown("""
            - **日志级别**: DEBUG < INFO < WARNING < ERROR < CRITICAL
            - **日志处理器**: 控制台、文件、轮转文件、时间轮转文件
            - **结构化日志**: 记录包含结构化数据的日志
            - **错误日志**: 记录异常信息和堆栈跟踪
            - **性能日志**: 根据操作耗时记录不同级别的日志
            - **日志管理**: 查看、清理日志文件
            """)
        
        return interface


# 应用实例
app = LoggingDemoApp()

if __name__ == "__main__":
    app.run() 