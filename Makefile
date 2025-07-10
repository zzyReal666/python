# LLM-Learn 企业级项目框架 Makefile

.PHONY: help install install-dev test lint format clean start migrate docker-build docker-up docker-down

# 默认目标
help:
	@echo "LLM-Learn 企业级项目框架管理命令"
	@echo ""
	@echo "可用命令:"
	@echo "  install     安装项目依赖"
	@echo "  install-dev 安装开发依赖"
	@echo "  test        运行测试"
	@echo "  lint        代码检查"
	@echo "  format      代码格式化"
	@echo "  clean       清理临时文件"
	@echo "  start       启动应用"
	@echo "  migrate     数据库迁移"
	@echo "  docker-build 构建Docker镜像"
	@echo "  docker-up   启动Docker服务"
	@echo "  docker-down 停止Docker服务"
	@echo "  help        显示帮助信息"

# 安装项目依赖
install:
	pip install -e .

# 安装开发依赖
install-dev:
	pip install -e ".[dev]"

# 运行测试
test:
	pytest --cov=src --cov-report=term-missing --cov-report=html

# 代码检查
lint:
	flake8 src tests
	mypy src
	bandit -r src -f json -o bandit-report.json
	safety check --json --output safety-report.json

# 代码格式化
format:
	black src tests
	isort src tests

# 清理临时文件
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .coverage
	rm -f bandit-report.json
	rm -f safety-report.json

# 启动应用
start:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# 数据库迁移
migrate:
	alembic upgrade head

# 创建迁移
migrate-create:
	@read -p "请输入迁移描述: " description; \
	alembic revision --autogenerate -m "$$description"

# 构建Docker镜像
docker-build:
	docker build -t llm-learn .

# 启动Docker服务
docker-up:
	docker-compose up -d

# 停止Docker服务
docker-down:
	docker-compose down

# 查看Docker日志
docker-logs:
	docker-compose logs -f

# 预提交检查
pre-commit:
	pre-commit run --all-files

# 安装预提交钩子
pre-commit-install:
	pre-commit install

# 安全检查
security-check:
	bandit -r src -f json -o bandit-report.json
	safety check --json --output safety-report.json

# 生成依赖报告
deps-report:
	pip list --format=freeze > requirements-freeze.txt
	pipdeptree > deps-tree.txt

# 更新依赖
update-deps:
	pip install --upgrade pip
	pip install --upgrade -e ".[dev]"

# 检查代码覆盖率
coverage:
	pytest --cov=src --cov-report=html --cov-report=term-missing
	@echo "覆盖率报告已生成在 htmlcov/index.html"

# 性能测试
perf-test:
	pytest tests/test_performance.py -v

# 集成测试
integration-test:
	pytest tests/test_integration.py -v

# 单元测试
unit-test:
	pytest tests/test_unit.py -v

# 检查代码质量
quality:
	@echo "运行代码质量检查..."
	@make format
	@make lint
	@make test
	@make security-check
	@echo "代码质量检查完成"

# 开发环境设置
dev-setup:
	@echo "设置开发环境..."
	python -m venv .venv
	@echo "请激活虚拟环境: source .venv/bin/activate"
	@echo "然后运行: make install-dev"
	@echo "最后运行: make pre-commit-install"

# 生产环境检查
prod-check:
	@echo "生产环境检查..."
	@test -f .env || (echo "错误: 未找到 .env 文件" && exit 1)
	@echo "检查环境变量..."
	@grep -q "SECRET_KEY" .env || (echo "警告: 未设置 SECRET_KEY" && exit 1)
	@grep -q "DATABASE_URL" .env || (echo "警告: 未设置 DATABASE_URL" && exit 1)
	@echo "生产环境检查通过"

# 备份数据库
backup-db:
	@echo "备份数据库..."
	@test -n "$(DB_NAME)" || (echo "请设置 DB_NAME 环境变量" && exit 1)
	@test -n "$(DB_USER)" || (echo "请设置 DB_USER 环境变量" && exit 1)
	pg_dump -U $(DB_USER) $(DB_NAME) > backup_$(shell date +%Y%m%d_%H%M%S).sql

# 恢复数据库
restore-db:
	@echo "恢复数据库..."
	@test -n "$(DB_NAME)" || (echo "请设置 DB_NAME 环境变量" && exit 1)
	@test -n "$(DB_USER)" || (echo "请设置 DB_USER 环境变量" && exit 1)
	@test -n "$(BACKUP_FILE)" || (echo "请设置 BACKUP_FILE 环境变量" && exit 1)
	psql -U $(DB_USER) $(DB_NAME) < $(BACKUP_FILE) 