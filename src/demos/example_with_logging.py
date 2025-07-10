#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用日志模块的示例应用
展示如何在实际项目中使用日志系统
"""

import random
import time

from utils.logger_utils import get_logger, get_structured_logger


def main():
    """主函数 - 演示日志使用"""

    # 获取日志记录器
    logger = get_logger("ExampleApp", level="DEBUG")
    struct_logger = get_structured_logger("ExampleApp")

    logger.info("=== 应用启动 ===")

    # 模拟用户操作
    simulate_user_actions(logger, struct_logger)

    # 模拟API调用
    simulate_api_calls(logger, struct_logger)

    # 模拟性能监控
    simulate_performance_monitoring(logger, struct_logger)

    # 模拟错误处理
    simulate_error_handling(logger, struct_logger)

    logger.info("=== 应用结束 ===")


def simulate_user_actions(logger, struct_logger):
    """模拟用户操作"""
    logger.info("开始模拟用户操作...")

    users = ["user001", "user002", "user003", "user004", "user005"]
    actions = ["login", "logout", "search", "download", "upload", "delete"]

    for i in range(5):
        user = random.choice(users)
        action = random.choice(actions)
        details = f"操作详情 #{i+1}"

        # 使用结构化日志记录用户操作
        struct_logger.log_user_action(user, action, details)

        # 模拟操作耗时
        time.sleep(0.1)

    logger.info("用户操作模拟完成")


def simulate_api_calls(logger, struct_logger):
    """模拟API调用"""
    logger.info("开始模拟API调用...")

    endpoints = [
        ("/api/users", "GET"),
        ("/api/posts", "POST"),
        ("/api/comments", "PUT"),
        ("/api/files", "DELETE"),
        ("/api/search", "GET"),
    ]

    for endpoint, method in endpoints:
        # 模拟API调用
        duration = random.uniform(0.1, 2.0)
        status_code = random.choice([200, 201, 400, 401, 404, 500])

        # 记录API调用日志
        struct_logger.log_api_call(endpoint, method, status_code, duration)

        # 模拟网络延迟
        time.sleep(0.05)

    logger.info("API调用模拟完成")


def simulate_performance_monitoring(logger, struct_logger):
    """模拟性能监控"""
    logger.info("开始性能监控...")

    operations = [
        "database_query",
        "file_processing",
        "image_resize",
        "data_analysis",
        "report_generation",
    ]

    for operation in operations:
        # 模拟操作耗时
        duration = random.uniform(0.5, 3.0)

        # 记录性能日志
        struct_logger.log_performance(operation, duration, threshold=1.5)

        # 模拟处理时间
        time.sleep(0.1)

    logger.info("性能监控完成")


def simulate_error_handling(logger, struct_logger):
    """模拟错误处理"""
    logger.info("开始错误处理测试...")

    error_types = [
        ValueError("无效的参数值"),
        TypeError("类型错误"),
        RuntimeError("运行时错误"),
        FileNotFoundError("文件未找到"),
        ConnectionError("连接错误"),
    ]

    for error in error_types:
        try:
            # 模拟抛出异常
            raise error
        except Exception as e:
            # 记录错误日志
            struct_logger.log_error(e, f"测试错误处理 - {type(e).__name__}")

            # 记录到普通日志
            logger.error(f"捕获到异常: {type(e).__name__}: {str(e)}")

        time.sleep(0.1)

    logger.info("错误处理测试完成")


def demonstrate_log_levels(logger):
    """演示不同日志级别"""
    logger.debug("这是一条调试信息 - 通常只在开发时使用")
    logger.info("这是一条一般信息 - 记录程序正常运行状态")
    logger.warning("这是一条警告信息 - 可能有问题，但不影响程序运行")
    logger.error("这是一条错误信息 - 程序出错，但可以继续运行")
    logger.critical("这是一条严重错误信息 - 程序可能崩溃")


if __name__ == "__main__":
    try:
        main()

        # 演示日志级别
        logger = get_logger("LevelDemo")
        print("\n=== 日志级别演示 ===")
        demonstrate_log_levels(logger)

        print("\n✅ 示例运行完成！")
        print("📁 查看 logs/ 目录中的日志文件")

    except Exception as e:
        # 确保错误也被记录
        logger = get_logger("ErrorHandler")
        logger.critical(f"程序运行出错: {str(e)}", exc_info=True)
        raise
