# Cursor 配置指南

## 🎯 配置目标

解决 Cursor 中找不到依赖包的问题，让 Cursor 正确使用虚拟环境。

## 📁 配置文件说明

### 1. `.vscode/settings.json`
- **Python 解释器路径**: 指向虚拟环境中的 Python
- **终端激活**: 自动激活虚拟环境
- **代码质量工具**: 配置 flake8, black, isort, mypy
- **测试配置**: 配置 pytest
- **路径配置**: 添加 src 目录到 Python 路径

### 2. `.vscode/launch.json`
- **调试配置**: 配置多个调试场景
- **环境变量**: 设置 PYTHONPATH
- **Python 解释器**: 使用虚拟环境中的 Python

### 3. `.vscode/tasks.json`
- **常用任务**: 安装依赖、运行应用、代码检查等
- **集成终端**: 在集成终端中执行命令
- **问题匹配**: 自动识别错误和警告

### 4. `.cursorrules`
- **AI 助手规则**: 指导 Cursor AI 理解项目结构
- **代码规范**: 定义代码风格和最佳实践
- **项目信息**: 提供项目上下文

## 🔧 手动配置步骤

如果自动配置不生效，请按以下步骤手动配置：

### 1. 选择 Python 解释器
1. 按 `Cmd+Shift+P` (Mac) 或 `Ctrl+Shift+P` (Windows/Linux)
2. 输入 "Python: Select Interpreter"
3. 选择 `./.venv/bin/python`

### 2. 重新加载窗口
1. 按 `Cmd+Shift+P` (Mac) 或 `Ctrl+Shift+P` (Windows/Linux)
2. 输入 "Developer: Reload Window"
3. 点击重新加载

### 3. 验证配置
1. 打开终端 (Terminal → New Terminal)
2. 检查是否显示 `(.venv)` 前缀
3. 运行 `python --version` 确认版本

## 🚀 使用方法

### 1. 运行应用
- **方法一**: 使用调试配置
  1. 按 `F5` 或点击调试按钮
  2. 选择 "Python: 主程序" 或 "Python: 日志演示"

- **方法二**: 使用任务
  1. 按 `Cmd+Shift+P` → "Tasks: Run Task"
  2. 选择 "运行日志演示"

- **方法三**: 使用终端
  ```bash
  python src/main.py run logging_demo
  ```

### 2. 代码质量检查
- **自动检查**: 保存时自动运行 flake8 和 mypy
- **手动检查**: 使用任务 "代码质量检查"
- **格式化**: 保存时自动格式化，或使用任务 "格式化代码"

### 3. 运行测试
- **方法一**: 使用调试配置 "Python: 测试"
- **方法二**: 使用任务 "运行测试"
- **方法三**: 在测试文件中点击 "Run Test"

## 🔍 故障排除

### 问题 1: 找不到模块
**症状**: `ModuleNotFoundError: No module named 'xxx'`

**解决方案**:
1. 确认 Python 解释器路径正确
2. 检查虚拟环境是否激活
3. 运行 `pip install -r requirements.txt`
4. 重启 Cursor

### 问题 2: 终端未激活虚拟环境
**症状**: 终端提示符没有 `(.venv)` 前缀

**解决方案**:
1. 检查 `.vscode/settings.json` 中的配置
2. 重新打开终端
3. 手动激活: `source .venv/bin/activate`

### 问题 3: 代码提示不工作
**症状**: 没有自动补全和类型提示

**解决方案**:
1. 确认 Python 扩展已安装
2. 检查 `python.analysis.extraPaths` 配置
3. 重新加载窗口

### 问题 4: 调试不工作
**症状**: 调试时找不到模块

**解决方案**:
1. 检查 `launch.json` 中的 `env` 配置
2. 确认 `PYTHONPATH` 设置正确
3. 使用绝对路径配置 Python 解释器

## 📋 常用快捷键

| 功能 | Mac | Windows/Linux |
|------|-----|---------------|
| 选择解释器 | `Cmd+Shift+P` | `Ctrl+Shift+P` |
| 运行调试 | `F5` | `F5` |
| 停止调试 | `Shift+F5` | `Shift+F5` |
| 运行任务 | `Cmd+Shift+P` | `Ctrl+Shift+P` |
| 格式化代码 | `Shift+Alt+F` | `Shift+Alt+F` |
| 打开终端 | `Ctrl+`` | `Ctrl+`` |

## 🎉 配置完成

配置完成后，你将获得：
- ✅ 正确的 Python 解释器
- ✅ 自动的代码质量检查
- ✅ 完整的调试支持
- ✅ 便捷的任务执行
- ✅ 智能的代码提示

现在你可以在 Cursor 中正常开发，不再需要切换到命令行运行代码！ 