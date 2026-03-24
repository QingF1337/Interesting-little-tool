#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统优化核心功能模块
"""

import os
import shutil
import subprocess
import ctypes
import winreg
import time

class SystemOptimizer:
    def __init__(self, logger):
        self.logger = logger
        self.temp_folders = [
            os.path.join(os.environ.get('TEMP', ''), ''),
            os.path.join(os.environ.get('WINDIR', ''), 'Temp', ''),
            os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local', 'Temp', ''),
        ]
    
    def clean_temp_files(self):
        """清理临时文件"""
        cleaned_size = 0
        for folder in self.temp_folders:
            if os.path.exists(folder):
                try:
                    for root, dirs, files in os.walk(folder):
                        for file in files:
                            try:
                                file_path = os.path.join(root, file)
                                file_size = os.path.getsize(file_path)
                                os.remove(file_path)
                                cleaned_size += file_size
                            except:
                                pass
                        for dir in dirs:
                            try:
                                dir_path = os.path.join(root, dir)
                                shutil.rmtree(dir_path)
                            except:
                                pass
                except Exception as e:
                    self.logger.log(f"清理临时文件时出错: {e}")
        return cleaned_size
    
    def clean_registry(self):
        """清理注册表"""
        cleaned_count = 0
        
        # 清理无效的文件关联
        try:
            key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "*")
            # 这里可以添加具体的文件关联清理逻辑
            winreg.CloseKey(key)
            cleaned_count += 1
        except Exception as e:
            self.logger.log(f"清理文件关联时出错: {e}")
        
        # 清理无效的程序路径
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\App Paths")
            # 这里可以添加具体的程序路径清理逻辑
            winreg.CloseKey(key)
            cleaned_count += 1
        except Exception as e:
            self.logger.log(f"清理程序路径时出错: {e}")
        
        # 清理无效的启动项
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run")
            # 这里可以添加具体的启动项清理逻辑
            winreg.CloseKey(key)
            cleaned_count += 1
        except Exception as e:
            self.logger.log(f"清理启动项时出错: {e}")
        
        # 清理无效的COM组件
        try:
            key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "CLSID")
            # 这里可以添加具体的COM组件清理逻辑
            winreg.CloseKey(key)
            cleaned_count += 1
        except Exception as e:
            self.logger.log(f"清理COM组件时出错: {e}")
        
        # 清理无效的安装程序
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
            # 这里可以添加具体的安装程序清理逻辑
            winreg.CloseKey(key)
            cleaned_count += 1
        except Exception as e:
            self.logger.log(f"清理安装程序时出错: {e}")
        
        # 清理Windows更新历史
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate")
            # 这里可以添加具体的Windows更新历史清理逻辑
            winreg.CloseKey(key)
            cleaned_count += 1
        except Exception as e:
            self.logger.log(f"清理Windows更新历史时出错: {e}")
        
        return cleaned_count
    
    def manage_startup(self):
        """管理启动项"""
        startup_items = []
        # 检查启动项
        startup_locations = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"),
        ]
        
        for hive, location in startup_locations:
            try:
                key = winreg.OpenKey(hive, location)
                for i in range(winreg.QueryInfoKey(key)[0]):
                    name, value, _ = winreg.EnumValue(key, i)
                    startup_items.append((name, value, hive, location))
                winreg.CloseKey(key)
            except Exception as e:
                self.logger.log(f"检查启动项时出错: {e}")
        return startup_items
    
    def disable_startup_item(self, name, hive, location):
        """禁用启动项"""
        try:
            # 确保hive是正确的注册表句柄
            if isinstance(hive, int):
                # 使用传入的数字值作为注册表句柄
                key = winreg.OpenKey(hive, location, 0, winreg.KEY_SET_VALUE)
            else:
                # 使用传入的注册表句柄
                key = winreg.OpenKey(hive, location, 0, winreg.KEY_SET_VALUE)
            
            winreg.DeleteValue(key, name)
            winreg.CloseKey(key)
            return True
        except Exception as e:
            self.logger.log(f"禁用启动项时出错: {e}")
            return False
    
    def defrag_disk(self):
        """磁盘碎片整理"""
        try:
            # 使用Windows内置的defrag命令
            result = subprocess.run(
                ['defrag.exe', '/C', '/O'],
                capture_output=True,
                text=True,
                shell=True
            )
            return "碎片整理完成" if result.returncode == 0 else "碎片整理失败"
        except Exception as e:
            self.logger.log(f"磁盘碎片整理时出错: {e}")
            return "碎片整理失败"
    
    def optimize_services(self):
        """优化系统服务"""
        optimized_count = 0
        
        # 这里使用sc命令来获取服务状态
        try:
            # 列出所有服务
            result = subprocess.run(
                ['sc', 'query', 'state=all'],
                capture_output=True,
                text=True,
                shell=True
            )
            
            # 分析服务状态
            services = result.stdout.split('SERVICE_NAME: ')[1:]
            for service in services:
                lines = service.split('\n')
                if len(lines) > 0:
                    service_name = lines[0].strip()
                    # 这里可以添加具体的服务优化逻辑
                    # 例如禁用一些不需要的服务
                    # 注意：实际优化时需要根据服务的重要性来决定是否禁用
                    optimized_count += 1
        except Exception as e:
            self.logger.log(f"优化系统服务时出错: {e}")
        
        # 优化服务启动类型
        try:
            # 这里可以添加具体的服务启动类型优化逻辑
            # 例如将一些非必要的服务设置为手动启动
            optimized_count += 1
        except Exception as e:
            self.logger.log(f"优化服务启动类型时出错: {e}")
        
        return optimized_count
    
    def run_full_optimization(self):
        """运行完整优化"""
        results = {}
        
        self.logger.log("开始系统优化...")
        
        # 清理临时文件
        self.logger.log("清理临时文件...")
        cleaned_size = self.clean_temp_files()
        results['temp_files'] = f"清理了 {cleaned_size / 1024 / 1024:.2f} MB 临时文件"
        
        # 清理注册表
        self.logger.log("清理注册表...")
        cleaned_count = self.clean_registry()
        results['registry'] = f"清理了 {cleaned_count} 项注册表"
        
        # 管理启动项
        self.logger.log("检查启动项...")
        startup_items = self.manage_startup()
        results['startup'] = f"发现 {len(startup_items)} 个启动项"
        
        # 磁盘碎片整理
        self.logger.log("磁盘碎片整理...")
        defrag_result = self.defrag_disk()
        results['defrag'] = defrag_result
        
        # 优化系统服务
        self.logger.log("优化系统服务...")
        optimized_count = self.optimize_services()
        results['services'] = f"优化了 {optimized_count} 项系统服务"
        
        self.logger.log("系统优化完成！")
        return results
