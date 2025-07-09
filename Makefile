.PHONY: help install install-dev test lint format clean run-gradio run-llm run-logging run-example

# 默认目标
help:
	@echo "LLM-learn 项目管理命令："
	@echo ""
	@echo "安装相关："
	@echo "  install      - 安装项目依赖"
	@echo "  install-dev  - 安装开发依赖"
	@echo ""
	@echo "代码质量："
	@echo "  test         - 运行测试"
	@echo "  lint         - 代码检查"
	@echo "  format       - 代码格式化"
	@echo ""
	@echo "运行应用："
	@echo "  run-gradio   - 运行 Gradio 演示"
	@echo "  run-llm      - 运行 LLM 演示"
	@echo "  run-logging  - 运行日志演示"
	@echo "  run-example  - 运行日志示例"
	@echo ""
	@echo "维护："
	@echo "  clean        - 清理临时文件"

# 安装项目依赖
install:
	pip install -r requirements.txt

# 安装开发依赖
install-dev:
	pip install -r requirements.txt
	pip install flake8 black isort mypy pytest pytest-cov pytest-mock

# 运行测试
test:
	pytest tests/ -v

# 代码检查
lint:
	flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
	black --check src/ tests/
	isort --check-only src/ tests/
	mypy src/

# 代码格式化
format:
	black src/ tests/
	isort src/ tests/

# Docker 相关
docker-build: ## 构建 Docker 镜像
	@echo "构建 Docker 镜像..."
	docker build -t llm-learn:latest .

docker-run: ## 运行 Docker 容器
	@echo "运行 Docker 容器..."
	docker-compose up -d

docker-stop: ## 停止 Docker 容器
	@echo "停止 Docker 容器..."
	docker-compose down

docker-logs: ## 查看 Docker 日志
	@echo "查看 Docker 日志..."
	docker-compose logs -f

# CI/CD 相关
ci-local: ## 本地运行 CI 流程
	@echo "本地运行 CI 流程..."
	$(MAKE) lint
	$(MAKE) test
	$(MAKE) docker-build

deploy-staging: ## 部署到测试环境
	@echo "部署到测试环境..."
	./scripts/deploy.sh staging

deploy-production: ## 部署到生产环境
	@echo "部署到生产环境..."
	./scripts/deploy.sh production

# 开发环境
dev: ## 启动开发环境
	@echo "启动开发环境..."
	docker-compose --profile dev up -d

dev-stop: ## 停止开发环境
	@echo "停止开发环境..."
	docker-compose --profile dev down

# GitHub 相关
init-github: ## 初始化 GitHub 仓库
	@echo "初始化 GitHub 仓库..."
	@read -p "请输入仓库名称: " repo_name; \
	./scripts/init-github.sh $$repo_name

github-setup: ## 设置 GitHub 环境
	@echo "设置 GitHub 环境..."
	@echo "请确保已安装 GitHub CLI: https://cli.github.com/"
	@echo "然后运行: gh auth login"

# 项目状态检查
status: ## 检查项目状态
	@echo "检查项目状态..."
	./scripts/check-status.sh

# 清理临时文件
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/ .mypy_cache/

# 运行 Gradio 演示
run-gradio:
	@echo "启动 Gradio 演示应用..."
	@echo "访问地址: http://localhost:7860"
	python src/apps/gradio_demo.py

# 运行 LLM 演示
run-llm:
	@echo "启动 LLM 演示应用..."
	@echo "访问地址: http://localhost:7861"
	python src/apps/llm_app_demo.py

# 运行日志演示
run-logging:
	@echo "启动日志演示应用..."
	@echo "访问地址: http://localhost:7862"
	python src/main.py run LoggingDemoApp

# 运行 TestApp 模块
run-testapp:
	@echo "启动 TestApp 模块..."
	@echo "访问地址: http://localhost:7860"
	python src/main.py run testapp

# 运行日志示例
run-example:
	@echo "运行日志使用示例..."
	python src/demos/example_with_logging.py

# 列出所有应用
list-apps:
	@echo "列出所有可用的学习模块..."
	python src/main.py list

# 创建新应用
create-app:
	@echo "创建新应用模板..."
	@read -p "请输入应用名称: " app_name; \
	read -p "请选择应用类型 (gradio/console): " app_type; \
	python src/main.py create $$app_name $$app_type 