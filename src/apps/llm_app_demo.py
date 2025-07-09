#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM 应用开发学习 Demo
包含多种 LLM 应用场景的示例
"""

import gradio as gr
import json
import re
from datetime import datetime
import random

class LLMSimulator:
    """LLM 模拟器 - 用于演示 LLM 应用开发"""
    
    def __init__(self):
        self.conversation_history = []
        self.system_prompt = "你是一个有用的AI助手，请用中文回答用户的问题。"
    
    def chat_completion(self, messages, temperature=0.7, max_tokens=1000):
        """模拟 LLM 聊天完成"""
        # 模拟 LLM 响应
        user_message = messages[-1]["content"] if messages else ""
        
        # 简单的规则基础响应
        response = self._generate_response(user_message)
        
        return {
            "choices": [{
                "message": {
                    "content": response,
                    "role": "assistant"
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": len(user_message),
                "completion_tokens": len(response),
                "total_tokens": len(user_message) + len(response)
            }
        }
    
    def _generate_response(self, user_input):
        """生成模拟响应"""
        user_input_lower = user_input.lower()
        
        # 预设的响应模式
        if "你好" in user_input or "hello" in user_input_lower:
            return "你好！我是AI助手，很高兴为您服务。有什么我可以帮助您的吗？"
        
        elif "天气" in user_input:
            return "今天天气晴朗，温度25°C，适合外出活动。"
        
        elif "时间" in user_input:
            return f"现在是 {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}"
        
        elif "计算" in user_input or "数学" in user_input:
            return "我可以帮助您进行基本的数学计算。请告诉我您想计算什么？"
        
        elif "翻译" in user_input:
            return "我可以帮助您翻译文本。请提供需要翻译的内容和目标语言。"
        
        elif "总结" in user_input:
            return "我可以帮助您总结文本内容。请提供需要总结的文本。"
        
        elif "代码" in user_input or "编程" in user_input:
            return "我可以帮助您编写和解释代码。请告诉我您需要什么编程帮助？"
        
        else:
            responses = [
                "这是一个很有趣的问题。让我想想...",
                "我理解您的问题，让我为您详细解答。",
                "根据我的理解，这个问题的答案是...",
                "这是一个很好的问题，让我从几个角度来分析。",
                "我建议您可以这样考虑这个问题..."
            ]
            return random.choice(responses) + f"\n\n关于'{user_input}'，我认为..."

# 创建 LLM 模拟器实例
llm_simulator = LLMSimulator()

def chat_with_llm(message, history, temperature, max_tokens):
    """与 LLM 聊天"""
    if not message.strip():
        return "", history
    
    # 构建消息历史
    messages = [{"role": "system", "content": llm_simulator.system_prompt}]
    
    # 添加历史对话
    for human, assistant in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": assistant})
    
    # 添加当前消息
    messages.append({"role": "user", "content": message})
    
    # 调用 LLM
    try:
        response = llm_simulator.chat_completion(
            messages, 
            temperature=temperature, 
            max_tokens=max_tokens
        )
        
        assistant_response = response["choices"][0]["message"]["content"]
        
        # 显示使用统计
        usage_info = f"\n\n--- 使用统计 ---\n"
        usage_info += f"输入tokens: {response['usage']['prompt_tokens']}\n"
        usage_info += f"输出tokens: {response['usage']['completion_tokens']}\n"
        usage_info += f"总tokens: {response['usage']['total_tokens']}"
        
        return "", history + [[message, assistant_response + usage_info]]
    
    except Exception as e:
        return "", history + [[message, f"错误：{str(e)}"]]

def text_summarizer(text, max_length):
    """文本总结功能"""
    if not text.strip():
        return "请输入要总结的文本"
    
    # 简单的文本总结逻辑
    sentences = re.split(r'[。！？]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) <= 3:
        return "文本太短，无需总结。原文：\n" + text
    
    # 选择关键句子
    key_sentences = sentences[:max(2, len(sentences)//3)]
    summary = "。".join(key_sentences) + "。"
    
    return f"总结结果：\n{summary}\n\n原文长度：{len(text)} 字符\n总结长度：{len(summary)} 字符"

def code_explainer(code, language):
    """代码解释功能"""
    if not code.strip():
        return "请输入要解释的代码"
    
    # 简单的代码分析
    lines = code.split('\n')
    line_count = len(lines)
    char_count = len(code)
    
    # 检测代码特征
    features = []
    if 'def ' in code:
        features.append("包含函数定义")
    if 'class ' in code:
        features.append("包含类定义")
    if 'import ' in code or 'from ' in code:
        features.append("包含导入语句")
    if 'if ' in code:
        features.append("包含条件语句")
    if 'for ' in code or 'while ' in code:
        features.append("包含循环语句")
    
    explanation = f"""
代码分析结果：

📊 基本信息：
- 编程语言：{language}
- 代码行数：{line_count}
- 字符数量：{char_count}

🔍 代码特征：
{chr(10).join(f"- {feature}" for feature in features) if features else "- 基础代码结构"}

💡 建议：
- 确保代码有适当的注释
- 遵循 {language} 的编码规范
- 考虑代码的可读性和维护性
"""
    
    return explanation

def prompt_engineering_demo(user_input, system_prompt, temperature):
    """提示工程演示"""
    if not user_input.strip():
        return "请输入用户输入"
    
    # 构建不同的系统提示
    prompts = {
        "默认": "你是一个有用的AI助手。",
        "专家": "你是一个领域专家，请用专业术语回答。",
        "教师": "你是一个耐心的教师，请用简单易懂的方式解释。",
        "创意": "你是一个创意助手，请提供创新的想法和解决方案。",
        "分析": "你是一个分析师，请提供详细的分析和推理过程。"
    }
    
    results = []
    for prompt_type, prompt in prompts.items():
        # 模拟不同提示的效果
        if prompt_type == "专家":
            response = f"作为{prompt_type}，我的专业分析是：{user_input}涉及复杂的专业概念..."
        elif prompt_type == "教师":
            response = f"让我用简单的方式解释：{user_input}就像..."
        elif prompt_type == "创意":
            response = f"从创意角度考虑：{user_input}可以这样创新地解决..."
        elif prompt_type == "分析":
            response = f"详细分析：首先，{user_input}需要考虑以下因素..."
        else:
            response = f"关于{user_input}，我的回答是..."
        
        results.append(f"**{prompt_type}模式：**\n{prompt}\n\n**回答：**\n{response}\n")
    
    return "\n---\n".join(results)

def rag_demo(query, documents):
    """RAG (检索增强生成) 演示"""
    if not query.strip():
        return "请输入查询问题"
    
    if not documents.strip():
        return "请输入文档内容"
    
    # 简单的文档检索
    doc_lines = documents.split('\n')
    relevant_docs = []
    
    # 简单的关键词匹配
    query_words = query.lower().split()
    for i, line in enumerate(doc_lines):
        if any(word in line.lower() for word in query_words):
            relevant_docs.append(f"文档第{i+1}行：{line}")
    
    if not relevant_docs:
        relevant_docs = ["未找到相关文档"]
    
    # 生成回答
    context = "\n".join(relevant_docs[:3])  # 取前3个相关文档
    
    response = f"""
RAG 检索结果：

🔍 查询：{query}

📄 相关文档：
{context}

💡 基于检索内容的回答：
根据检索到的文档，关于"{query}"的答案是...
"""
    
    return response

def function_calling_demo(user_input):
    """函数调用演示"""
    if not user_input.strip():
        return "请输入用户输入"
    
    # 模拟函数调用检测
    functions = {
        "天气": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "city": {"type": "string", "description": "城市名称"}
            }
        },
        "计算": {
            "name": "calculate",
            "description": "执行数学计算",
            "parameters": {
                "expression": {"type": "string", "description": "数学表达式"}
            }
        },
        "翻译": {
            "name": "translate",
            "description": "翻译文本",
            "parameters": {
                "text": {"type": "string", "description": "要翻译的文本"},
                "target_language": {"type": "string", "description": "目标语言"}
            }
        }
    }
    
    detected_functions = []
    for keyword, func in functions.items():
        if keyword in user_input:
            detected_functions.append(func)
    
    if detected_functions:
        result = "检测到函数调用需求：\n\n"
        for func in detected_functions:
            result += f"📞 函数：{func['name']}\n"
            result += f"📝 描述：{func['description']}\n"
            result += f"🔧 参数：{json.dumps(func['parameters'], ensure_ascii=False, indent=2)}\n\n"
    else:
        result = "未检测到特定的函数调用需求。"
    
    return result

# 创建 Gradio 界面
with gr.Blocks(title="LLM 应用开发学习 Demo", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 LLM 应用开发学习 Demo")
    gr.Markdown("这个演示应用展示了 LLM 应用开发中的常见场景和技术。")
    
    with gr.Tab("💬 聊天对话"):
        gr.Markdown("### LLM 聊天对话演示")
        with gr.Row():
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(height=400, label="对话历史")
                msg = gr.Textbox(label="输入消息", placeholder="请输入您的问题...")
                with gr.Row():
                    clear = gr.Button("清空对话")
                    submit = gr.Button("发送", variant="primary")
            with gr.Column(scale=1):
                temperature = gr.Slider(0.1, 2.0, value=0.7, label="Temperature")
                max_tokens = gr.Slider(100, 2000, value=1000, step=100, label="Max Tokens")
        
        submit.click(chat_with_llm, [msg, chatbot, temperature, max_tokens], [msg, chatbot])
        msg.submit(chat_with_llm, [msg, chatbot, temperature, max_tokens], [msg, chatbot])
        clear.click(lambda: ([], ""), outputs=[chatbot, msg])
    
    with gr.Tab("📝 文本总结"):
        gr.Markdown("### 文本总结功能演示")
        with gr.Row():
            with gr.Column():
                text_input = gr.Textbox(
                    label="输入文本",
                    placeholder="请输入要总结的文本...",
                    lines=8
                )
                max_length = gr.Slider(50, 500, value=200, label="总结最大长度")
                summarize_btn = gr.Button("生成总结", variant="primary")
            with gr.Column():
                summary_output = gr.Textbox(label="总结结果", lines=10)
        
        summarize_btn.click(text_summarizer, [text_input, max_length], summary_output)
    
    with gr.Tab("💻 代码解释"):
        gr.Markdown("### 代码解释功能演示")
        with gr.Row():
            with gr.Column():
                code_input = gr.Textbox(
                    label="输入代码",
                    placeholder="请输入要解释的代码...",
                    lines=10
                )
                language = gr.Dropdown(
                    choices=["Python", "JavaScript", "Java", "C++", "Go"],
                    label="编程语言",
                    value="Python"
                )
                explain_btn = gr.Button("解释代码", variant="primary")
            with gr.Column():
                explanation_output = gr.Textbox(label="代码解释", lines=12)
        
        explain_btn.click(code_explainer, [code_input, language], explanation_output)
    
    with gr.Tab("🎯 提示工程"):
        gr.Markdown("### 提示工程演示")
        with gr.Row():
            with gr.Column():
                prompt_input = gr.Textbox(
                    label="用户输入",
                    placeholder="请输入您的问题...",
                    lines=3
                )
                system_prompt = gr.Textbox(
                    label="系统提示",
                    value="你是一个有用的AI助手。",
                    lines=2
                )
                prompt_temperature = gr.Slider(0.1, 2.0, value=0.7, label="Temperature")
                prompt_btn = gr.Button("生成回答", variant="primary")
            with gr.Column():
                prompt_output = gr.Textbox(label="不同提示的效果对比", lines=15)
        
        prompt_btn.click(prompt_engineering_demo, [prompt_input, system_prompt, prompt_temperature], prompt_output)
    
    with gr.Tab("🔍 RAG 检索"):
        gr.Markdown("### RAG (检索增强生成) 演示")
        with gr.Row():
            with gr.Column():
                query_input = gr.Textbox(
                    label="查询问题",
                    placeholder="请输入您的问题...",
                    lines=2
                )
                documents_input = gr.Textbox(
                    label="文档内容",
                    placeholder="请输入文档内容，每行一个文档片段...",
                    lines=8
                )
                rag_btn = gr.Button("RAG 检索", variant="primary")
            with gr.Column():
                rag_output = gr.Textbox(label="RAG 结果", lines=12)
        
        rag_btn.click(rag_demo, [query_input, documents_input], rag_output)
    
    with gr.Tab("📞 函数调用"):
        gr.Markdown("### 函数调用演示")
        with gr.Row():
            with gr.Column():
                func_input = gr.Textbox(
                    label="用户输入",
                    placeholder="例如：查询北京的天气、计算 2+3*4、翻译 hello world",
                    lines=3
                )
                func_btn = gr.Button("检测函数调用", variant="primary")
            with gr.Column():
                func_output = gr.Textbox(label="函数调用检测结果", lines=10)
        
        func_btn.click(function_calling_demo, func_input, func_output)
    
    with gr.Tab("📚 学习资源"):
        gr.Markdown("""
        ### LLM 应用开发学习资源
        
        #### 🎯 核心概念
        - **提示工程 (Prompt Engineering)**: 设计有效的提示来获得更好的 LLM 响应
        - **RAG (Retrieval-Augmented Generation)**: 结合检索和生成的混合方法
        - **函数调用 (Function Calling)**: 让 LLM 能够调用外部函数
        - **微调 (Fine-tuning)**: 针对特定任务优化模型
        
        #### 🛠️ 常用工具
        - **OpenAI API**: 最流行的 LLM API
        - **LangChain**: LLM 应用开发框架
        - **Gradio**: 快速构建 Web 界面
        - **Streamlit**: 数据科学应用框架
        
        #### 📖 推荐学习路径
        1. 掌握基础 API 调用
        2. 学习提示工程技巧
        3. 实践 RAG 应用开发
        4. 探索函数调用功能
        5. 构建完整的应用
        
        #### 🔗 有用链接
        - [OpenAI API 文档](https://platform.openai.com/docs)
        - [LangChain 文档](https://python.langchain.com/)
        - [Gradio 文档](https://gradio.app/docs/)
        - [提示工程指南](https://www.promptingguide.ai/)
        
        **创建时间：** """ + datetime.now().strftime("%Y年%m月%d日 %H:%M:%S"))

if __name__ == "__main__":
    # 启动应用
    demo.launch(
        server_name="0.0.0.0",
        server_port=7861,  # 使用不同端口避免冲突
        share=False,
        debug=True
    ) 