#!/bin/bash

# GitHub 仓库初始化脚本
# 用法: ./scripts/init-github.sh <repository-name>

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# 检查参数
if [ $# -eq 0 ]; then
    log_error "请提供仓库名称"
    echo "用法: $0 <repository-name>"
    echo "示例: $0 my-llm-learn-project"
    exit 1
fi

REPO_NAME=$1
GITHUB_USERNAME=$(git config user.name || echo "your-username")

log_info "开始初始化 GitHub 仓库: $REPO_NAME"

# 检查 Git 是否安装
if ! command -v git &> /dev/null; then
    log_error "Git 未安装或未在 PATH 中"
    exit 1
fi

# 检查是否在 Git 仓库中
if [ ! -d ".git" ]; then
    log_step "初始化 Git 仓库..."
    git init
fi

# 检查是否有未提交的更改
if [ -n "$(git status --porcelain)" ]; then
    log_warn "检测到未提交的更改，正在提交..."
    git add .
    git commit -m "Initial commit: 企业级 LLM 学习项目"
fi

# 创建 GitHub 仓库（使用 GitHub CLI）
log_step "创建 GitHub 仓库..."
if command -v gh &> /dev/null; then
    log_info "使用 GitHub CLI 创建仓库..."
    gh repo create "$REPO_NAME" --public --description "企业级 LLM 学习项目，包含完整的 CI/CD 流程" --source=. --remote=origin --push
else
    log_warn "GitHub CLI 未安装，请手动创建仓库"
    log_info "请访问 https://github.com/new 创建仓库: $REPO_NAME"
    log_info "然后运行以下命令："
    echo ""
    echo "git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    echo "git branch -M main"
    echo "git push -u origin main"
    echo ""
    read -p "按回车键继续..."
fi

# 创建 develop 分支
log_step "创建 develop 分支..."
git checkout -b develop
git push -u origin develop

# 切换回 main 分支
git checkout main

# 设置分支保护规则（如果使用 GitHub CLI）
if command -v gh &> /dev/null; then
    log_step "设置分支保护规则..."
    gh api repos/$GITHUB_USERNAME/$REPO_NAME/branches/main/protection \
        --method PUT \
        --field required_status_checks='{"strict":true,"contexts":["ci-cd"]}' \
        --field enforce_admins=true \
        --field required_pull_request_reviews='{"required_approving_review_count":1}' \
        --field restrictions=null || log_warn "无法设置分支保护规则，请手动设置"
fi

# 创建 GitHub 环境（如果使用 GitHub CLI）
if command -v gh &> /dev/null; then
    log_step "创建 GitHub 环境..."
    gh api repos/$GITHUB_USERNAME/$REPO_NAME/environments/staging \
        --method PUT \
        --field wait_timer=0 || log_warn "无法创建 staging 环境"
    
    gh api repos/$GITHUB_USERNAME/$REPO_NAME/environments/production \
        --method PUT \
        --field wait_timer=0 \
        --field required_reviewers='[{"type":"User","id":1}]' || log_warn "无法创建 production 环境"
fi

# 显示后续步骤
log_info "GitHub 仓库初始化完成！"
echo ""
log_step "后续步骤："
echo "1. 访问 https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo "2. 检查 GitHub Actions 是否正常运行"
echo "3. 配置环境变量（如果需要）"
echo "4. 设置分支保护规则"
echo "5. 邀请团队成员"
echo ""
log_info "项目已准备好进行企业级开发！" 