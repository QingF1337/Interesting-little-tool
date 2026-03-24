#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电脑一键优化程序
"""

import sys
import os
import ctypes
from gui import OptimizerGUI
from optimizer import SystemOptimizer
from logger import Logger

def is_admin():
    """检查是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":
    # 确保以管理员权限运行
    if not os.name == 'nt':
        print("此程序仅支持Windows系统")
        sys.exit(1)
    
    # 检查管理员权限
    if not is_admin():
        print("请以管理员权限运行此程序")
        # 重新以管理员权限运行
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(1)
    
    try:
        # 创建日志记录器
        logger = Logger()
        
        # 创建系统优化器实例
        optimizer = SystemOptimizer(logger)
        
        # 创建并运行GUI
        app = OptimizerGUI(optimizer, logger)
        app.run()
    except Exception as e:
        print(f"程序运行出错: {e}")
        sys.exit(1)
