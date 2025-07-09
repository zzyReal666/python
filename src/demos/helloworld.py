#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hello World 程序
一个简单的 Python 示例程序
"""
import logging
def main():
    """主函数，打印 Hello World"""
    logger.info("Hello, World!")
    logger.debug("Debug message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
    print("Hello, World!")
    print("你好，世界！")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    main()
