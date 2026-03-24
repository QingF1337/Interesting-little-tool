#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志记录模块
"""

import os
import datetime

class Logger:
    def __init__(self):
        self.log_dir = "logs"
        self.log_file = os.path.join(self.log_dir, f"optimize_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        
        # 创建日志目录
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def log(self, message):
        """记录日志"""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        
        # 输出到控制台
        print(log_entry)
        
        # 写入文件
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + '\n')
        except Exception as e:
            print(f"写入日志文件失败: {e}")
    
    def get_log_file(self):
        """获取日志文件路径"""
        return self.log_file
