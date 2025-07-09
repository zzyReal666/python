#!/bin/bash

# 项目状态检查脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[!]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[→]${NC} $1"
}

echo "🔍 检查项目状态..."
echo "=================="

# 检查 Python 版本
log_step "检查 Python 版本..."
if command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1)
    log_info "Python: $PYTHON_VERSION"
else
    log_error "Python 未安装"
fi

# 检查虚拟环境
log_step "检查虚拟环境..."
if [ -n "$VIRTUAL_ENV" ]; then
    log_info "虚拟环境已激活: $VIRTUAL_ENV"
else
    log_warn "虚拟环境未激活"
fi

# 检查依赖
log_step "检查项目依赖..."
if [ -f "requirements.txt" ]; then
    log_info "requirements.txt 存在"
    if pip list | grep -q "gradio"; then
        log_info "Gradio 已安装"
    else
        log_warn "Gradio 未安装"
    fi
else
    log_error "requirements.txt 不存在"
fi

# 检查 Docker
log_step "检查 Docker..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    log_info "Docker: $DOCKER_VERSION"
    
    if docker info &> /dev/null; then
        log_info "Docker 守护进程运行正常"
    else
        log_warn "Docker 守护进程未运行"
    fi
else
    log_warn "Docker 未安装"
fi

# 检查 Docker Compose
log_step "检查 Docker Compose..."
if command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version)
    log_info "Docker Compose: $COMPOSE_VERSION"
else
    log_warn "Docker Compose 未安装"
fi

# 检查 Git
log_step "检查 Git..."
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    log_info "Git: $GIT_VERSION"
    
    if [ -d ".git" ]; then
        log_info "Git 仓库已初始化"
        
        # 检查远程仓库
        if git remote -v | grep -q "origin"; then
            log_info "远程仓库已配置"
        else
            log_warn "远程仓库未配置"
        fi
    else
        log_warn "Git 仓库未初始化"
    fi
else
    log_error "Git 未安装"
fi

# 检查 GitHub CLI
log_step "检查 GitHub CLI..."
if command -v gh &> /dev/null; then
    GH_VERSION=$(gh --version | head -n 1)
    log_info "GitHub CLI: $GH_VERSION"
    
    if gh auth status &> /dev/null; then
        log_info "GitHub CLI 已认证"
    else
        log_warn "GitHub CLI 未认证，请运行: gh auth login"
    fi
else
    log_warn "GitHub CLI 未安装"
fi

# 检查项目文件
log_step "检查项目文件..."
if [ -f "src/main.py" ]; then
    log_info "主程序文件存在"
else
    log_error "主程序文件不存在"
fi

if [ -f "Makefile" ]; then
    log_info "Makefile 存在"
else
    log_error "Makefile 不存在"
fi

if [ -f ".github/workflows/ci-cd.yml" ]; then
    log_info "GitHub Actions 配置存在"
else
    log_error "GitHub Actions 配置不存在"
fi

if [ -f "Dockerfile" ]; then
    log_info "Dockerfile 存在"
else
    log_error "Dockerfile 不存在"
fi

# 检查应用
log_step "检查应用..."
if [ -f "src/apps/logging_demo.py" ]; then
    log_info "日志演示应用存在"
else
    log_error "日志演示应用不存在"
fi

# 检查测试
log_step "检查测试..."
if [ -d "tests" ]; then
    TEST_COUNT=$(find tests -name "test_*.py" | wc -l)
    log_info "测试文件数量: $TEST_COUNT"
else
    log_warn "测试目录不存在"
fi

# 检查日志目录
log_step "检查日志目录..."
if [ -d "logs" ]; then
    log_info "日志目录存在"
else
    log_warn "日志目录不存在，将自动创建"
    mkdir -p logs
fi

echo ""
echo "📊 项目状态总结:"
echo "=================="

# 统计检查结果
TOTAL_CHECKS=0
PASSED_CHECKS=0

# 这里可以添加更详细的统计逻辑

echo ""
echo "🚀 下一步建议:"
echo "=============="

if [ ! -d ".git" ]; then
    echo "1. 初始化 Git 仓库: git init"
fi

if [ -z "$VIRTUAL_ENV" ]; then
    echo "2. 激活虚拟环境: source venv/bin/activate"
fi

if ! pip list | grep -q "gradio"; then
    echo "3. 安装依赖: pip install -r requirements.txt"
fi

if [ ! -d ".git" ] || ! git remote -v | grep -q "origin"; then
    echo "4. 设置 GitHub 仓库: make init-github"
fi

echo "5. 运行应用: make run-logging"
echo "6. 运行测试: make test"
echo "7. 代码质量检查: make lint"

echo ""
log_info "项目状态检查完成！" 