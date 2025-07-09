#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 包导入示例
演示各种导入外部包的方法
"""

# 1. 导入标准库模块
import os
import sys
import datetime
import json

# 2. 从模块导入特定函数/类
from datetime import datetime, timedelta
from os import path, makedirs
from json import loads, dumps

# 3. 从包中导入子模块
from urllib import request, parse

# 4. 尝试导入第三方包（需要先安装）
print("=== 尝试导入第三方包 ===")
try:
    import requests
    print("✅ requests 包导入成功")
except ImportError:
    print("❌ requests 包未安装，请运行: pip install requests")

try:
    import numpy as np
    print("✅ numpy 包导入成功")
except ImportError:
    print("❌ numpy 包未安装，请运行: pip install numpy")

try:
    import pandas as pd
    print("✅ pandas 包导入成功")
except ImportError:
    print("❌ pandas 包未安装，请运行: pip install pandas")

def demonstrate_standard_library():
    """演示标准库的使用"""
    print("\n=== 标准库使用示例 ===")
    
    # 使用 os 模块
    current_dir = os.getcwd()
    print(f"当前目录: {current_dir}")
    
    # 使用 datetime
    now = datetime.now()
    print(f"当前时间: {now}")
    
    # 使用 json
    data = {"name": "张三", "age": 25}
    json_str = json.dumps(data, ensure_ascii=False)
    print(f"JSON 字符串: {json_str}")

def demonstrate_third_party_packages():
    """演示第三方包的使用"""
    print("\n=== 第三方包使用示例 ===")
    
    # 检查并演示 numpy
    if 'np' in globals():
        print("numpy 包可用")
        arr = np.array([1, 2, 3, 4, 5])
        print(f"numpy 数组: {arr}")
        print(f"数组平均值: {np.mean(arr)}")
    else:
        print("numpy 包不可用")
    
    # 检查并演示 requests
    if 'requests' in globals():
        print("requests 包可用")
        # 这里可以添加 HTTP 请求示例
    else:
        print("requests 包不可用")

def show_installation_guide():
    """显示安装指南"""
    print("\n" + "="*50)
    print("📦 常用第三方包安装指南")
    print("="*50)
    
    packages = [
        ("requests", "HTTP 请求库"),
        ("numpy", "数值计算库"),
        ("pandas", "数据分析库"),
        ("matplotlib", "绘图库"),
        ("flask", "Web 框架"),
        ("sqlalchemy", "ORM 库"),
        ("pytest", "测试框架"),
        ("jupyter", "Jupyter notebook"),
    ]
    
    print("单个包安装:")
    for package, description in packages:
        print(f"  pip install {package:<15} # {description}")
    
    print("\n批量安装:")
    package_names = [pkg for pkg, _ in packages]
    print(f"  pip install {' '.join(package_names)}")
    
    print("\n使用虚拟环境（推荐）:")
    print("  python3 -m venv myenv")
    print("  source myenv/bin/activate  # macOS/Linux")
    print("  pip install package_name")

if __name__ == "__main__":
    demonstrate_standard_library()
    demonstrate_third_party_packages()
    show_installation_guide() 