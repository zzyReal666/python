#!/bin/bash

# Gradio 应用启动脚本

echo "🚀 启动 Gradio 演示应用..."

# 激活虚拟环境
source /Users/zhangzhongyuan/PycharmProjects/venv/bin/activate

# 检查是否在虚拟环境中
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ 虚拟环境已激活: $VIRTUAL_ENV"
else
    echo "❌ 虚拟环境激活失败"
    exit 1
fi

# 检查 Gradio 是否已安装
if python -c "import gradio" 2>/dev/null; then
    echo "✅ Gradio 已安装"
else
    echo "❌ Gradio 未安装，正在安装..."
    pip install gradio
fi

# 启动应用
echo "🌐 启动 Web 应用..."
echo "📱 应用将在浏览器中打开: http://localhost:7860"
echo "⏹️  按 Ctrl+C 停止应用"
echo ""

python gradio_demo.py 