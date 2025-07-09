"""项目配置文件"""

import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent.parent

# 环境配置
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
DEBUG = ENVIRONMENT == 'development'

# 日志配置
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'app.log'

# Gradio 配置
GRADIO_SERVER_NAME = os.getenv('GRADIO_SERVER_NAME', '127.0.0.1')
GRADIO_SERVER_PORT = int(os.getenv('GRADIO_SERVER_PORT', 7860))
GRADIO_SHARE = os.getenv('GRADIO_SHARE', 'False').lower() == 'true'

# 应用配置
DEFAULT_APP = 'logging_demo'
APPS_DIR = BASE_DIR / 'src' / 'apps'

# Docker 配置
DOCKER_IMAGE_NAME = 'llm-learn'
DOCKER_REGISTRY = os.getenv('DOCKER_REGISTRY', 'ghcr.io')

# 测试配置
TEST_DIR = BASE_DIR / 'tests'
COVERAGE_DIR = BASE_DIR / 'htmlcov'

# 开发工具配置
CODE_QUALITY = {
    'flake8': {
        'max_line_length': 88,
        'exclude': ['.git', '__pycache__', '.venv', 'venv', '.pytest_cache', 'build', 'dist'],
    },
    'black': {
        'line_length': 88,
        'target_version': ['py311'],
    },
    'isort': {
        'profile': 'black',
        'line_length': 88,
    },
    'mypy': {
        'python_version': '3.11',
        'warn_return_any': True,
        'disallow_untyped_defs': True,
    },
}

# 环境特定配置
if ENVIRONMENT == 'production':
    LOG_LEVEL = 'WARNING'
    GRADIO_SERVER_NAME = '0.0.0.0'
elif ENVIRONMENT == 'staging':
    LOG_LEVEL = 'DEBUG'
    GRADIO_SERVER_NAME = '0.0.0.0' 