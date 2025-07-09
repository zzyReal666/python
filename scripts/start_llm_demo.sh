#!/bin/bash

# LLM 应用开发学习 Demo 启动脚本

echo "🤖 启动 LLM 应用开发学习 Demo..."

# 激活虚拟环境
source /Users/zhangzhongyuan/PycharmProjects/venv/bin/activate

# 检查是否在虚拟环境中
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ 虚拟环境已激活: $VIRTUAL_ENV"
else
    echo "❌ 虚拟环境激活失败"
    exit 1
fi

# 检查依赖包
echo "📦 检查依赖包..."
python -c "import gradio, json, re, random" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ 所有依赖包已安装"
else
    echo "❌ 缺少依赖包，正在安装..."
    pip install gradio
fi

# 启动应用
echo "🌐 启动 LLM 学习 Demo..."
echo "📱 应用将在浏览器中打开: http://localhost:7861"
echo "⏹️  按 Ctrl+C 停止应用"
echo ""
echo "🎯 功能模块："
echo "  💬 聊天对话 - LLM 对话演示"
echo "  📝 文本总结 - 文本总结功能"
echo "  💻 代码解释 - 代码分析功能"
echo "  🎯 提示工程 - 提示工程演示"
echo "  🔍 RAG 检索 - 检索增强生成"
echo "  📞 函数调用 - 函数调用演示"
echo "  📚 学习资源 - 学习资料和链接"
echo ""

python src/apps/llm_app_demo.py 