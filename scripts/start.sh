#!/bin/bash

# 企业级Python项目启动脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Python版本
check_python_version() {
    log_info "检查Python版本..."
    python_version=$(python3 --version 2>&1 | awk '{print $2}')
    required_version="3.8.0"
    
    if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
        log_success "Python版本 $python_version 满足要求"
    else
        log_error "Python版本 $python_version 不满足要求，需要 3.8+"
        exit 1
    fi
}

# 检查虚拟环境
check_venv() {
    log_info "检查虚拟环境..."
    if [ -z "$VIRTUAL_ENV" ]; then
        log_warning "未检测到虚拟环境，建议使用虚拟环境"
        read -p "是否继续？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        log_success "虚拟环境已激活: $VIRTUAL_ENV"
    fi
}

# 安装依赖
install_dependencies() {
    log_info "安装项目依赖..."
    if [ -f "pyproject.toml" ]; then
        pip install -e ".[dev]"
        log_success "依赖安装完成"
    else
        log_error "未找到 pyproject.toml 文件"
        exit 1
    fi
}

# 检查环境变量
check_env() {
    log_info "检查环境变量..."
    if [ ! -f ".env" ]; then
        log_warning "未找到 .env 文件，复制示例文件"
        if [ -f "env.example" ]; then
            cp env.example .env
            log_success "已复制 env.example 到 .env"
            log_warning "请编辑 .env 文件配置数据库等参数"
        else
            log_error "未找到 env.example 文件"
            exit 1
        fi
    else
        log_success "环境变量文件已存在"
    fi
}

# 数据库迁移
run_migrations() {
    log_info "运行数据库迁移..."
    if command -v alembic &> /dev/null; then
        alembic upgrade head
        log_success "数据库迁移完成"
    else
        log_warning "未找到 alembic，跳过数据库迁移"
    fi
}

# 运行测试
run_tests() {
    log_info "运行测试..."
    if command -v pytest &> /dev/null; then
        pytest --cov=src --cov-report=term-missing
        log_success "测试完成"
    else
        log_warning "未找到 pytest，跳过测试"
    fi
}

# 代码检查
run_linting() {
    log_info "运行代码检查..."
    
    if command -v black &> /dev/null; then
        black --check src tests
        log_success "代码格式化检查通过"
    fi
    
    if command -v isort &> /dev/null; then
        isort --check-only src tests
        log_success "导入排序检查通过"
    fi
    
    if command -v flake8 &> /dev/null; then
        flake8 src tests
        log_success "代码风格检查通过"
    fi
    
    if command -v mypy &> /dev/null; then
        mypy src
        log_success "类型检查通过"
    fi
}

# 启动应用
start_app() {
    log_info "启动应用..."
    
    # 检查端口是否被占用
    if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
        log_warning "端口 8000 已被占用"
        read -p "是否继续？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    # 启动应用
    uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
}

# 主函数
main() {
    log_info "启动企业级Python项目..."
    
    check_python_version
    check_venv
    install_dependencies
    check_env
    run_migrations
    run_tests
    run_linting
    start_app
}

# 处理命令行参数
case "${1:-}" in
    "install")
        check_python_version
        check_venv
        install_dependencies
        ;;
    "migrate")
        run_migrations
        ;;
    "test")
        run_tests
        ;;
    "lint")
        run_linting
        ;;
    "start")
        start_app
        ;;
    "help"|"-h"|"--help")
        echo "用法: $0 [命令]"
        echo ""
        echo "命令:"
        echo "  install   安装依赖"
        echo "  migrate   运行数据库迁移"
        echo "  test      运行测试"
        echo "  lint      运行代码检查"
        echo "  start     启动应用"
        echo "  help      显示帮助信息"
        ;;
    "")
        main
        ;;
    *)
        log_error "未知命令: $1"
        echo "使用 '$0 help' 查看可用命令"
        exit 1
        ;;
esac 