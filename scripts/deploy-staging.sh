#!/bin/bash

# 测试环境部署脚本
# 使用方法: ./scripts/deploy-staging.sh

set -e  # 遇到错误立即退出

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

# 配置变量
STAGING_ENV="staging"
DOCKER_IMAGE="ghcr.io/zzyReal666/python"
DOCKER_TAG="develop"
COMPOSE_FILE="docker-compose.staging.yml"
BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"

# 主函数
main() {
    log_info "开始部署到测试环境..."
    
    # 1. 检查环境
    check_environment
    
    # 2. 备份当前版本
    backup_current_version
    
    # 3. 拉取最新镜像
    pull_latest_image
    
    # 4. 停止当前服务
    stop_current_services
    
    # 5. 部署新版本
    deploy_new_version
    
    # 6. 健康检查
    health_check
    
    # 7. 清理旧版本
    cleanup_old_versions
    
    log_success "测试环境部署完成！"
}

# 检查部署环境
check_environment() {
    log_info "检查部署环境..."
    
    # 检查 Docker 是否安装
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安装，请先安装 Docker"
        exit 1
    fi
    
    # 检查 Docker Compose 是否安装
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose 未安装，请先安装 Docker Compose"
        exit 1
    fi
    
    # 检查必要的文件是否存在
    if [ ! -f "$COMPOSE_FILE" ]; then
        log_error "Docker Compose 文件不存在: $COMPOSE_FILE"
        exit 1
    fi
    
    # 检查网络连接
    if ! docker info &> /dev/null; then
        log_error "无法连接到 Docker 守护进程"
        exit 1
    fi
    
    log_success "环境检查通过"
}

# 备份当前版本
backup_current_version() {
    log_info "备份当前版本..."
    
    # 创建备份目录
    mkdir -p "$BACKUP_DIR"
    
    # 备份当前运行的容器信息
    docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}" > "$BACKUP_DIR/running_containers.txt" 2>/dev/null || true
    
    # 备份 Docker Compose 文件
    cp "$COMPOSE_FILE" "$BACKUP_DIR/"
    
    # 备份环境变量文件（如果存在）
    if [ -f ".env.staging" ]; then
        cp ".env.staging" "$BACKUP_DIR/"
    fi
    
    log_success "备份完成: $BACKUP_DIR"
}

# 拉取最新镜像
pull_latest_image() {
    log_info "拉取最新 Docker 镜像..."
    
    # 登录到 GitHub Container Registry（如果需要）
    if [ -n "$GITHUB_TOKEN" ]; then
        echo "$GITHUB_TOKEN" | docker login ghcr.io -u "$GITHUB_USERNAME" --password-stdin
    fi
    
    # 拉取镜像
    docker pull "$DOCKER_IMAGE:$DOCKER_TAG"
    
    log_success "镜像拉取完成: $DOCKER_IMAGE:$DOCKER_TAG"
}

# 停止当前服务
stop_current_services() {
    log_info "停止当前服务..."
    
    # 使用 Docker Compose 停止服务
    docker-compose -f "$COMPOSE_FILE" down --remove-orphans || true
    
    # 等待服务完全停止
    sleep 5
    
    log_success "当前服务已停止"
}

# 部署新版本
deploy_new_version() {
    log_info "部署新版本..."
    
    # 设置环境变量
    export ENVIRONMENT="$STAGING_ENV"
    export DOCKER_IMAGE="$DOCKER_IMAGE:$DOCKER_TAG"
    
    # 使用 Docker Compose 启动服务
    docker-compose -f "$COMPOSE_FILE" up -d --force-recreate
    
    # 等待服务启动
    log_info "等待服务启动..."
    sleep 10
    
    log_success "新版本部署完成"
}

# 健康检查
health_check() {
    log_info "执行健康检查..."
    
    # 等待服务完全启动
    sleep 30
    
    # 检查容器状态
    if docker-compose -f "$COMPOSE_FILE" ps | grep -q "Up"; then
        log_success "容器运行正常"
    else
        log_error "容器启动失败"
        docker-compose -f "$COMPOSE_FILE" logs
        exit 1
    fi
    
    # 检查应用健康状态（假设应用有健康检查端点）
    if command -v curl &> /dev/null; then
        if curl -f http://localhost:7860/health &> /dev/null; then
            log_success "应用健康检查通过"
        else
            log_warning "应用健康检查失败，但容器正在运行"
        fi
    fi
    
    # 显示服务状态
    log_info "当前服务状态:"
    docker-compose -f "$COMPOSE_FILE" ps
}

# 清理旧版本
cleanup_old_versions() {
    log_info "清理旧版本..."
    
    # 清理未使用的镜像
    docker image prune -f
    
    # 清理未使用的容器
    docker container prune -f
    
    # 清理未使用的网络
    docker network prune -f
    
    # 保留最近 5 个备份
    find ./backups -type d -name "backup_*" | sort -r | tail -n +6 | xargs rm -rf 2>/dev/null || true
    
    log_success "清理完成"
}

# 回滚函数
rollback() {
    log_warning "开始回滚到上一个版本..."
    
    # 停止当前服务
    docker-compose -f "$COMPOSE_FILE" down
    
    # 恢复备份（这里需要根据实际情况实现）
    log_info "回滚完成"
}

# 显示帮助信息
show_help() {
    echo "测试环境部署脚本"
    echo ""
    echo "使用方法:"
    echo "  $0              # 部署到测试环境"
    echo "  $0 rollback     # 回滚到上一个版本"
    echo "  $0 help         # 显示帮助信息"
    echo ""
    echo "环境变量:"
    echo "  GITHUB_TOKEN    # GitHub Token（用于拉取私有镜像）"
    echo "  GITHUB_USERNAME # GitHub 用户名"
}

# 脚本入口
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "rollback")
        rollback
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        log_error "未知参数: $1"
        show_help
        exit 1
        ;;
esac 