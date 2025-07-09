#!/bin/bash

# 部署脚本
# 用法: ./scripts/deploy.sh [staging|production]

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查参数
if [ $# -eq 0 ]; then
    log_error "请指定部署环境: staging 或 production"
    echo "用法: $0 [staging|production]"
    exit 1
fi

ENVIRONMENT=$1

# 验证环境参数
if [ "$ENVIRONMENT" != "staging" ] && [ "$ENVIRONMENT" != "production" ]; then
    log_error "无效的环境参数: $ENVIRONMENT"
    echo "支持的环境: staging, production"
    exit 1
fi

log_info "开始部署到 $ENVIRONMENT 环境..."

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    log_error "Docker 未安装或未在 PATH 中"
    exit 1
fi

# 检查 Docker Compose 是否安装
if ! command -v docker-compose &> /dev/null; then
    log_error "Docker Compose 未安装或未在 PATH 中"
    exit 1
fi

# 构建 Docker 镜像
log_info "构建 Docker 镜像..."
docker build -t llm-learn:$ENVIRONMENT .

# 停止现有容器
log_info "停止现有容器..."
docker-compose down || true

# 启动新容器
log_info "启动新容器..."
if [ "$ENVIRONMENT" = "staging" ]; then
    docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d
else
    docker-compose -f docker-compose.yml -f docker-compose.production.yml up -d
fi

# 等待服务启动
log_info "等待服务启动..."
sleep 10

# 检查服务状态
log_info "检查服务状态..."
if docker-compose ps | grep -q "Up"; then
    log_info "部署成功！"
    log_info "应用地址: http://localhost:7860"
else
    log_error "部署失败，请检查日志"
    docker-compose logs
    exit 1
fi

log_info "部署完成！" 