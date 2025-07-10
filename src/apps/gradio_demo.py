#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gradio 演示应用
包含多种常用功能的示例
"""

import base64
import io
from datetime import datetime

import gradio as gr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def greet(name, is_morning, temperature):
    """简单的问候函数"""
    salutation = "早上好" if is_morning else "下午好"
    celsius_or_fahrenheit = "摄氏度" if temperature > 0 else "华氏度"
    return f"{salutation}，{name}！今天是 {temperature}°{celsius_or_fahrenheit}。"


def calculator(num1, num2, operation):
    """简单计算器"""
    if operation == "加法":
        return num1 + num2
    elif operation == "减法":
        return num1 - num2
    elif operation == "乘法":
        return num1 * num2
    elif operation == "除法":
        return num1 / num2 if num2 != 0 else "错误：除数不能为零"
    else:
        return "无效操作"


def text_analyzer(text):
    """文本分析器"""
    if not text:
        return "请输入文本"

    # 基本统计
    char_count = len(text)
    word_count = len(text.split())
    line_count = len(text.split("\n"))

    # 字符类型统计
    letters = sum(c.isalpha() for c in text)
    digits = sum(c.isdigit() for c in text)
    spaces = sum(c.isspace() for c in text)

    analysis = f"""
    📊 文本分析结果：
    
    📝 基本统计：
    - 字符数：{char_count}
    - 单词数：{word_count}
    - 行数：{line_count}
    
    🔤 字符类型：
    - 字母：{letters}
    - 数字：{digits}
    - 空格：{spaces}
    - 其他：{char_count - letters - digits - spaces}
    """

    return analysis


def generate_chart(chart_type, data_points):
    """生成图表"""
    try:
        n = int(data_points)
        if n <= 0 or n > 100:
            return "请输入1-100之间的数字"

        # 生成随机数据
        x = np.linspace(0, 10, n)
        y = np.sin(x) + np.random.normal(0, 0.1, n)

        # 创建图表
        plt.figure(figsize=(10, 6))

        if chart_type == "折线图":
            plt.plot(x, y, "b-", linewidth=2)
            plt.title("正弦波折线图")
        elif chart_type == "散点图":
            plt.scatter(x, y, alpha=0.6, color="red")
            plt.title("散点图")
        elif chart_type == "柱状图":
            plt.bar(x[:20], y[:20], alpha=0.7, color="green")
            plt.title("柱状图")

        plt.xlabel("X 轴")
        plt.ylabel("Y 轴")
        plt.grid(True, alpha=0.3)

        # 保存图表到内存
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format="png", dpi=100, bbox_inches="tight")
        img_buffer.seek(0)
        plt.close()

        # 转换为 base64
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"

    except ValueError:
        return "请输入有效的数字"


def sentiment_analyzer(text):
    """简单的情感分析（模拟）"""
    if not text:
        return "请输入文本"

    # 简单的情感词汇检测
    positive_words = ["好", "棒", "优秀", "喜欢", "爱", "开心", "快乐", "满意", "成功"]
    negative_words = ["坏", "差", "讨厌", "恨", "难过", "痛苦", "失望", "失败", "糟糕"]

    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)

    if positive_count > negative_count:
        sentiment = "😊 积极"
        score = positive_count / (positive_count + negative_count + 1) * 100
    elif negative_count > positive_count:
        sentiment = "😞 消极"
        score = negative_count / (positive_count + negative_count + 1) * 100
    else:
        sentiment = "😐 中性"
        score = 50

    return f"情感分析结果：{sentiment}\n置信度：{score:.1f}%"


# 创建 Gradio 界面
with gr.Blocks(title="Gradio 多功能演示", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎉 Gradio 多功能演示应用")
    gr.Markdown("这是一个包含多种功能的 Gradio 演示应用，展示了 Gradio 的基本用法。")

    with gr.Tab("👋 问候"):
        gr.Markdown("### 个性化问候")
        with gr.Row():
            with gr.Column():
                name_input = gr.Textbox(label="您的姓名", placeholder="请输入您的姓名")
                is_morning = gr.Checkbox(label="现在是早上吗？")
                temperature = gr.Slider(
                    minimum=-50, maximum=50, value=20, label="温度 (°C)"
                )
                greet_btn = gr.Button("生成问候", variant="primary")
            with gr.Column():
                greet_output = gr.Textbox(label="问候结果", lines=3)

        greet_btn.click(
            greet, inputs=[name_input, is_morning, temperature], outputs=greet_output
        )

    with gr.Tab("🧮 计算器"):
        gr.Markdown("### 简单计算器")
        with gr.Row():
            with gr.Column():
                num1 = gr.Number(label="第一个数字")
                num2 = gr.Number(label="第二个数字")
                operation = gr.Dropdown(
                    choices=["加法", "减法", "乘法", "除法"], label="运算", value="加法"
                )
                calc_btn = gr.Button("计算", variant="primary")
            with gr.Column():
                calc_output = gr.Textbox(label="计算结果")

        calc_btn.click(calculator, inputs=[num1, num2, operation], outputs=calc_output)

    with gr.Tab("📊 文本分析"):
        gr.Markdown("### 文本统计分析")
        with gr.Row():
            with gr.Column():
                text_input = gr.Textbox(
                    label="输入文本", placeholder="请输入要分析的文本...", lines=5
                )
                analyze_btn = gr.Button("分析文本", variant="primary")
            with gr.Column():
                analysis_output = gr.Textbox(label="分析结果", lines=10)

        analyze_btn.click(text_analyzer, inputs=text_input, outputs=analysis_output)

    with gr.Tab("📈 图表生成"):
        gr.Markdown("### 数据可视化")
        with gr.Row():
            with gr.Column():
                chart_type = gr.Dropdown(
                    choices=["折线图", "散点图", "柱状图"],
                    label="图表类型",
                    value="折线图",
                )
                data_points = gr.Slider(
                    minimum=5, maximum=100, value=50, step=5, label="数据点数量"
                )
                chart_btn = gr.Button("生成图表", variant="primary")
            with gr.Column():
                chart_output = gr.Image(label="生成的图表")

        chart_btn.click(
            generate_chart, inputs=[chart_type, data_points], outputs=chart_output
        )

    with gr.Tab("😊 情感分析"):
        gr.Markdown("### 简单情感分析")
        with gr.Row():
            with gr.Column():
                sentiment_text = gr.Textbox(
                    label="输入文本", placeholder="请输入要分析情感的文本...", lines=4
                )
                sentiment_btn = gr.Button("分析情感", variant="primary")
            with gr.Column():
                sentiment_output = gr.Textbox(label="情感分析结果", lines=3)

        sentiment_btn.click(
            sentiment_analyzer, inputs=sentiment_text, outputs=sentiment_output
        )

    with gr.Tab("ℹ️ 关于"):
        gr.Markdown(
            """
        ### 关于这个应用
        
        这是一个使用 **Gradio** 构建的多功能演示应用，展示了以下功能：
        
        - ✅ 文本输入和输出
        - ✅ 数字输入和计算
        - ✅ 下拉选择框
        - ✅ 滑块控件
        - ✅ 复选框
        - ✅ 按钮交互
        - ✅ 图像显示
        - ✅ 多标签页界面
        - ✅ 响应式布局
        
        **技术栈：**
        - Python 3.x
        - Gradio 5.x
        - NumPy
        - Matplotlib
        - Pandas
        
        **创建时间：** """
            + datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        )

if __name__ == "__main__":
    # 启动应用
    demo.launch(
        server_name="0.0.0.0",  # 允许外部访问
        server_port=7860,  # 端口号
        share=False,  # 是否生成公共链接
        debug=True,  # 调试模式
    )
