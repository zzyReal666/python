# LLM-learn 项目

这是一个用于学习 LLM（大语言模型）相关技术的项目，包含各种示例和演示。

## 📁 项目结构

```
LLM-learn/
├── src/                   # 源代码目录
│   ├── __init__.py        # 主包初始化文件
│   ├── core/              # 核心模块
│   ├── utils/             # 工具模块
│   │   ├── __init__.py
│   │   └── logger_utils.py # 日志工具模块
│   ├── apps/              # 应用模块
│   │   ├── __init__.py
│   │   ├── gradio_demo.py # Gradio 多功能演示
│   │   ├── llm_app_demo.py # LLM 应用开发学习 Demo
│   │   └── logging_demo.py # Python 日志模块演示
│   └── demos/             # 演示模块
│       ├── __init__.py
│       ├── helloworld.py  # Hello World 示例
│       ├── import_examples.py # Python 包导入示例
│       └── example_with_logging.py # 日志使用示例
├── scripts/               # 脚本目录
│   ├── start_gradio.sh    # Gradio 应用启动脚本
│   ├── start_llm_demo.sh  # LLM Demo 启动脚本
│   └── start_logging_demo.sh # 日志演示启动脚本
├── config/                # 配置文件目录
├── docs/                  # 文档目录
│   └── pip_mirrors.md     # pip 镜像源配置指南
├── tests/                 # 测试目录
├── logs/                  # 日志文件目录
├── requirements.txt       # 项目依赖
├── setup.py              # 项目安装配置
├── pyproject.toml        # 现代 Python 项目配置
├── Makefile              # 项目管理命令
├── .gitignore            # Git 忽略文件
└── README.md             # 项目说明文档
```

## 🚀 快速开始

### 1. 环境准备

确保您已经设置了 Python 虚拟环境：

```bash
# 激活虚拟环境
source /Users/zhangzhongyuan/PycharmProjects/venv/bin/activate

# 验证环境
python --version
pip list
```

### 2. 运行 Hello World

```bash
python src/demos/helloworld.py
```

### 3. 运行 Gradio 演示应用

#### 方法一：使用启动脚本（推荐）
```bash
./start_gradio.sh
```

#### 方法二：手动启动
```bash
# 激活虚拟环境
source /Users/zhangzhongyuan/PycharmProjects/venv/bin/activate

# 启动应用
python src/apps/gradio_demo.py
```

应用启动后，在浏览器中访问：http://localhost:7860

### 4. 运行 LLM 应用开发学习 Demo

#### 方法一：使用启动脚本（推荐）
```bash
./start_llm_demo.sh
```

#### 方法二：手动启动
```bash
# 激活虚拟环境
source /Users/zhangzhongyuan/PycharmProjects/venv/bin/activate

# 启动应用
python src/apps/llm_app_demo.py
```

应用启动后，在浏览器中访问：http://localhost:7861

### 5. 运行日志模块演示

#### 方法一：使用启动脚本（推荐）
```bash
./start_logging_demo.sh
```

#### 方法二：手动启动
```bash
# 激活虚拟环境
source /Users/zhangzhongyuan/PycharmProjects/venv/bin/activate

# 启动应用
python src/apps/logging_demo.py
```

应用启动后，在浏览器中访问：http://localhost:7862

### 6. 运行日志使用示例
```bash
# 激活虚拟环境
source /Users/zhangzhongyuan/PycharmProjects/venv/bin/activate

# 运行示例
python src/demos/example_with_logging.py
```

### 7. 使用 Makefile（推荐）

项目提供了 Makefile 来简化常用操作：

```bash
# 查看所有可用命令
make help

# 安装项目依赖
make install

# 安装开发依赖
make install-dev

# 运行应用
make run-gradio    # 运行 Gradio 演示
make run-llm       # 运行 LLM 演示
make run-logging   # 运行日志演示
make run-example   # 运行日志示例

# 应用管理
make list-apps     # 列出所有应用
make create-app    # 创建新应用模板

# 代码质量
make format        # 代码格式化
make lint          # 代码检查
make test          # 运行测试
make clean         # 清理临时文件
```

### 8. 使用主程序管理工具

项目提供了统一的管理工具来管理所有学习模块：

```bash
# 列出所有可用的学习模块
python src/main.py list

# 运行指定应用
python src/main.py run LoggingDemoApp
python src/main.py run LoggingDemoApp --port 8080

# 创建新的学习模块
python src/main.py create MyApp gradio     # 创建 Gradio 应用
python src/main.py create MyApp console    # 创建控制台应用

# 查看应用信息
python src/main.py info LoggingDemoApp
```

## 🏢 企业级开发流程

### 代码质量检查
```bash
# 运行代码质量检查
make lint

# 格式化代码
make format

# 运行测试
make test

# 生成测试覆盖率报告
make test-cov
```

### Docker 开发
```bash
# 构建 Docker 镜像
make docker-build

# 启动开发环境
make dev

# 查看日志
make docker-logs

# 停止开发环境
make dev-stop
```

### CI/CD 流程
```bash
# 本地运行 CI 流程
make ci-local

# 部署到测试环境
make deploy-staging

# 部署到生产环境
make deploy-production
```

### GitHub Actions 自动化

项目配置了完整的 GitHub Actions CI/CD 流程：

- **代码质量检查**: flake8, black, isort, mypy
- **单元测试**: pytest 测试框架
- **Docker 构建**: 自动构建和推送 Docker 镜像
- **安全扫描**: Trivy 漏洞扫描
- **自动部署**: 支持测试和生产环境部署

### 分支策略

- `main`: 生产环境分支
- `develop`: 开发环境分支
- `feature/*`: 功能开发分支
- `hotfix/*`: 紧急修复分支

### 9. 添加新的学习模块

项目采用模块化设计，您可以轻松添加新的学习模块：

#### 方法一：使用命令行工具（推荐）
```bash
# 创建新的 Gradio 应用
python src/main.py create MyLearningApp gradio

# 创建新的控制台应用
python src/main.py create MyLearningApp console
```

#### 方法二：手动创建
1. 在 `src/apps/` 目录下创建新的应用文件
2. 继承 `GradioApp` 或 `ConsoleApp` 基类
3. 实现必要的方法（`create_interface()` 或 `run_console()`）
4. 应用会自动被系统发现和注册

#### 应用模板示例
```python
# Gradio 应用模板
from core.base_app import GradioApp
import gradio as gr

class MyApp(GradioApp):
    def __init__(self):
        super().__init__(
            name="my_app",
            description="我的学习模块",
            port=7863
        )
    
    def create_interface(self):
        # 实现您的 Gradio 界面
        pass

# 控制台应用模板
from core.base_app import ConsoleApp

class MyConsoleApp(ConsoleApp):
    def __init__(self):
        super().__init__(
            name="my_console_app",
            description="我的控制台应用"
        )
    
    def run_console(self, **kwargs):
        # 实现您的控制台逻辑
        pass
```

## 🎯 应用功能

### Gradio 演示应用功能

#### 👋 问候模块
- 个性化问候语生成
- 根据时间和温度调整问候内容

#### 🧮 计算器
- 基本四则运算
- 支持加法、减法、乘法、除法

#### 📊 文本分析
- 字符统计
- 单词计数
- 行数统计
- 字符类型分析

#### 📈 图表生成
- 折线图
- 散点图
- 柱状图
- 动态数据生成

#### 😊 情感分析
- 简单的情感词汇检测
- 积极/消极/中性情感判断
- 置信度评分

### LLM 应用开发学习 Demo 功能

#### 💬 聊天对话
- LLM 对话演示
- 对话历史管理
- Token 使用统计
- 参数调节（Temperature、Max Tokens）

#### 📝 文本总结
- 智能文本总结
- 可调节总结长度
- 原文与总结对比

#### 💻 代码解释
- 多语言代码分析
- 代码特征检测
- 编程建议提供

#### 🎯 提示工程
- 不同系统提示效果对比
- 专家、教师、创意、分析等角色
- Temperature 参数影响演示

#### 🔍 RAG 检索
- 检索增强生成演示
- 文档相关性匹配
- 基于检索内容的回答生成

#### 📞 函数调用
- 函数调用需求检测
- 参数结构展示
- 多种函数类型支持

#### 📚 学习资源
- LLM 开发核心概念
- 推荐学习路径
- 常用工具介绍
- 相关文档链接

### Python 日志模块功能

#### 🔧 基本日志
- 基础日志记录演示
- 不同日志级别测试
- 日志格式化配置

#### 🏗️ 结构化日志
- 结构化日志记录
- JSON 格式日志输出
- 事件类型分类

#### ❌ 错误日志
- 错误处理和日志记录
- 异常堆栈跟踪
- 错误类型分类

#### ⚡ 性能日志
- 性能监控日志
- 操作耗时记录
- 性能阈值警告

#### 📊 日志级别
- 不同日志级别测试
- 级别过滤演示
- 级别配置说明

#### 📁 日志管理
- 日志文件管理
- 文件轮转配置
- 日志清理功能

#### 📚 学习指南
- 日志系统学习资料
- 最佳实践指南
- 配置示例和文档

## 🔧 技术栈

- **Python 3.x**
- **Gradio 5.x** - Web 界面框架
- **NumPy** - 数值计算
- **Matplotlib** - 数据可视化
- **Pandas** - 数据处理

## 📦 包管理

### 安装新包
```bash
# 激活虚拟环境
source /Users/zhangzhongyuan/PycharmProjects/venv/bin/activate

# 安装包
pip install 包名
```

### 配置镜像源
项目已配置清华大学镜像源，如需修改请参考 `pip_mirrors.md`

## 🌐 访问应用

- **本地访问**：http://localhost:7860
- **网络访问**：http://你的IP地址:7860

## 🛠️ 开发说明

### 添加新功能
1. 在 `gradio_demo.py` 中添加新的函数
2. 在界面中添加对应的组件
3. 连接函数和组件

### 自定义主题
```python
# 使用内置主题
demo = gr.Blocks(theme=gr.themes.Soft())

# 或使用默认主题
demo = gr.Blocks()
```

## 📝 注意事项

1. **虚拟环境**：确保在正确的虚拟环境中运行
2. **端口占用**：如果 7860 端口被占用，可以修改 `gradio_demo.py` 中的端口号
3. **依赖管理**：新安装的包会自动安装到虚拟环境中
4. **调试模式**：应用默认开启调试模式，生产环境请关闭

## 🔗 相关链接

- [Gradio 官方文档](https://gradio.app/docs/)
- [Python 官方文档](https://docs.python.org/)
- [NumPy 文档](https://numpy.org/doc/)
- [Matplotlib 文档](https://matplotlib.org/)

## 📞 支持

如有问题，请检查：
1. 虚拟环境是否正确激活
2. 依赖包是否已安装
3. 端口是否被占用
4. 防火墙设置

---

**创建时间**：2025年7月9日  
**最后更新**：2025年7月9日 # 测试 CI/CD 触发
