#!/bin/bash

# Python 日志模块演示启动脚本

echo "📝 启动 Python 日志模块演示..."

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
python -c "import logging, gradio" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ 所有依赖包已安装"
else
    echo "❌ 缺少依赖包，正在安装..."
    pip install gradio
fi

# 创建日志目录
echo "📁 创建日志目录..."
mkdir -p logs

# 启动应用
echo "🌐 启动日志演示应用..."
echo "📱 应用将在浏览器中打开: http://localhost:7862"
echo "⏹️  按 Ctrl+C 停止应用"
echo ""
echo "🎯 功能模块："
echo "  🔧 基本日志 - 基础日志记录演示"
echo "  🏗️ 结构化日志 - 结构化日志记录"
echo "  ❌ 错误日志 - 错误处理和日志记录"
echo "  ⚡ 性能日志 - 性能监控日志"
echo "  📊 日志级别 - 不同日志级别测试"
echo "  📁 日志管理 - 日志文件管理"
echo "  📚 学习指南 - 日志系统学习资料"
echo ""

python src/apps/logging_demo.py 