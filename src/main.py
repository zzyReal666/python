#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM-learn 项目主程序
提供命令行界面来管理所有学习模块
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

# 添加 src 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from core.app_manager import app_manager


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="LLM-learn 学习项目管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python src/main.py list                    # 列出所有应用
  python src/main.py run logging_demo        # 运行日志演示应用
  python src/main.py create MyApp gradio     # 创建新的 Gradio 应用
  python src/main.py create MyApp console    # 创建新的控制台应用
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # list 命令
    list_parser = subparsers.add_parser("list", help="列出所有应用")

    # run 命令
    run_parser = subparsers.add_parser("run", help="运行指定应用")
    run_parser.add_argument("app_name", help="应用名称")
    run_parser.add_argument("--port", type=int, help="端口号（仅适用于 Gradio 应用）")

    # create 命令
    create_parser = subparsers.add_parser("create", help="创建新应用")
    create_parser.add_argument("app_name", help="应用名称")
    create_parser.add_argument(
        "app_type", choices=["gradio", "console"], help="应用类型"
    )

    # info 命令
    info_parser = subparsers.add_parser("info", help="显示应用信息")
    info_parser.add_argument("app_name", help="应用名称")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "list":
        list_apps()
    elif args.command == "run":
        run_app(args.app_name, args.port)
    elif args.command == "create":
        create_app(args.app_name, args.app_type)
    elif args.command == "info":
        show_app_info(args.app_name)


def list_apps():
    """列出所有应用"""
    apps = app_manager.list_apps()

    if not apps:
        print("没有找到任何应用")
        return

    print("可用的学习模块:")
    print("-" * 60)

    for i, app in enumerate(apps, 1):
        print(f"{i}. {app['name']}")
        print(f"   描述: {app['description']}")
        print(f"   版本: {app['version']}")
        print()

    print(f"总共 {len(apps)} 个应用")
    print("\n使用 'python src/main.py run <应用名称>' 来运行应用")


def run_app(app_name: str, port: Optional[int] = None):
    """运行指定应用"""
    app_class = app_manager.get_app(app_name)
    if not app_class:
        print(f"错误: 应用 '{app_name}' 不存在")
        print("使用 'python src/main.py list' 查看可用应用")
        return

    print(f"启动应用: {app_name}")

    kwargs = {}
    if port:
        kwargs["port"] = port

    try:
        app_manager.run_app(app_name, **kwargs)
    except KeyboardInterrupt:
        print(f"\n应用 {app_name} 已停止")


def create_app(app_name: str, app_type: str):
    """创建新应用"""
    print(f"创建 {app_type} 应用: {app_name}")

    try:
        app_manager.create_app_template(app_name, app_type)
        print(f"✅ 应用模板已创建: src/apps/{app_name.lower()}_app.py")
        print("\n下一步:")
        print(f"1. 编辑 src/apps/{app_name.lower()}_app.py 实现您的业务逻辑")
        print(f"2. 运行 'python src/main.py run {app_name}App' 启动应用")
    except Exception as e:
        print(f"❌ 创建应用失败: {e}")


def show_app_info(app_name: str):
    """显示应用信息"""
    app_class = app_manager.get_app(app_name)
    if not app_class:
        print(f"错误: 应用 '{app_name}' 不存在")
        return

    try:
        app = app_class(app_name, f"{app_name} 应用")
        info = app.get_info()

        print(f"应用信息: {app_name}")
        print("-" * 40)
        print(f"名称: {info.get('name', app_name)}")
        print(f"描述: {info.get('description', '无描述')}")
        print(f"版本: {info.get('version', '1.0.0')}")

        # 显示应用类型
        if hasattr(app, "port") and app.port:
            print(f"类型: Gradio 应用")
            print(f"端口: {app.port}")
        else:
            print(f"类型: 控制台应用")

    except Exception as e:
        print(f"获取应用信息失败: {e}")


if __name__ == "__main__":
    main()
