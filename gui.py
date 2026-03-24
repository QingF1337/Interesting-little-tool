#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图形用户界面模块
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading

class OptimizerGUI:
    def __init__(self, optimizer, logger):
        self.optimizer = optimizer
        self.logger = logger
        self.root = tk.Tk()
        self.root.title("电脑一键优化")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # 设置图标（如果有）
        # self.root.iconbitmap("icon.ico")
        
        self.create_widgets()
    
    def create_widgets(self):
        """创建界面组件"""
        # 标题
        title_frame = ttk.Frame(self.root, padding="20")
        title_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(
            title_frame,
            text="电脑一键优化",
            font=("微软雅黑", 16, "bold")
        )
        title_label.pack()
        
        # 功能描述
        desc_frame = ttk.Frame(self.root, padding="0 10 0 20")
        desc_frame.pack(fill=tk.X)
        
        desc_label = ttk.Label(
            desc_frame,
            text="一键优化电脑性能，清理垃圾文件，提升系统速度",
            font=("微软雅黑", 10)
        )
        desc_label.pack()
        
        # 优化选项
        options_frame = ttk.LabelFrame(self.root, text="优化选项", padding="10")
        options_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # 选项变量
        self.opt_temp = tk.BooleanVar(value=True)
        self.opt_registry = tk.BooleanVar(value=True)
        self.opt_startup = tk.BooleanVar(value=True)
        self.opt_defrag = tk.BooleanVar(value=True)
        self.opt_services = tk.BooleanVar(value=True)
        
        # 选项复选框
        ttk.Checkbutton(
            options_frame,
            text="清理临时文件",
            variable=self.opt_temp
        ).pack(anchor=tk.W, pady=5)
        
        ttk.Checkbutton(
            options_frame,
            text="清理注册表",
            variable=self.opt_registry
        ).pack(anchor=tk.W, pady=5)
        
        ttk.Checkbutton(
            options_frame,
            text="管理启动项",
            variable=self.opt_startup
        ).pack(anchor=tk.W, pady=5)
        
        ttk.Checkbutton(
            options_frame,
            text="磁盘碎片整理",
            variable=self.opt_defrag
        ).pack(anchor=tk.W, pady=5)
        
        ttk.Checkbutton(
            options_frame,
            text="优化系统服务",
            variable=self.opt_services
        ).pack(anchor=tk.W, pady=5)
        
        # 按钮
        button_frame = ttk.Frame(self.root, padding="20")
        button_frame.pack(fill=tk.X)
        
        self.optimize_button = ttk.Button(
            button_frame,
            text="开始优化",
            command=self.start_optimization,
            style="Accent.TButton"
        )
        self.optimize_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="管理启动项",
            command=self.open_startup_manager
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="退出",
            command=self.root.quit
        ).pack(side=tk.RIGHT, padx=5)
        
        # 日志输出
        log_frame = ttk.LabelFrame(self.root, text="优化日志", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.log_text = tk.Text(
            log_frame,
            wrap=tk.WORD,
            height=8,
            font=("Consolas", 10)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(self.log_text, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        # 配置样式
        style = ttk.Style()
        style.configure("Accent.TButton", foreground="white", background="#0078d7")
    
    def log(self, message):
        """添加日志信息"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
    
    def start_optimization(self):
        """开始优化"""
        # 禁用按钮
        self.optimize_button.config(state=tk.DISABLED)
        
        # 清空日志
        self.log_text.delete(1.0, tk.END)
        self.log("开始系统优化...")
        
        # 在新线程中运行优化
        def optimization_thread():
            try:
                results = {}
                
                # 根据用户选择的选项执行优化
                if self.opt_temp.get():
                    self.log("清理临时文件...")
                    cleaned_size = self.optimizer.clean_temp_files()
                    results['temp_files'] = f"清理了 {cleaned_size / 1024 / 1024:.2f} MB 临时文件"
                
                if self.opt_registry.get():
                    self.log("清理注册表...")
                    cleaned_count = self.optimizer.clean_registry()
                    results['registry'] = f"清理了 {cleaned_count} 项注册表"
                
                if self.opt_startup.get():
                    self.log("检查启动项...")
                    startup_items = self.optimizer.manage_startup()
                    results['startup'] = f"发现 {len(startup_items)} 个启动项"
                
                if self.opt_defrag.get():
                    self.log("磁盘碎片整理...")
                    defrag_result = self.optimizer.defrag_disk()
                    results['defrag'] = defrag_result
                
                if self.opt_services.get():
                    self.log("优化系统服务...")
                    optimized_count = self.optimizer.optimize_services()
                    results['services'] = f"优化了 {optimized_count} 项系统服务"
                
                # 显示结果
                for key, value in results.items():
                    self.log(value)
                
                if results:
                    self.log("\n优化完成！")
                    messagebox.showinfo("优化完成", "电脑优化已完成，系统性能已提升！")
                else:
                    self.log("\n未选择任何优化选项！")
                    messagebox.showinfo("提示", "请至少选择一项优化选项")
            except Exception as e:
                self.log(f"优化过程中出错: {e}")
                messagebox.showerror("错误", f"优化过程中出错: {e}")
            finally:
                # 启用按钮
                self.optimize_button.config(state=tk.NORMAL)
        
        thread = threading.Thread(target=optimization_thread)
        thread.daemon = True
        thread.start()
    
    def open_startup_manager(self):
        """打开启动项管理窗口"""
        # 创建启动项管理窗口
        startup_window = tk.Toplevel(self.root)
        startup_window.title("启动项管理")
        startup_window.geometry("800x400")
        startup_window.resizable(True, True)
        
        # 创建列表框
        list_frame = ttk.Frame(startup_window, padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建树状视图
        columns = ("name", "path", "location")
        tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        tree.heading("name", text="名称")
        tree.heading("path", text="路径")
        tree.heading("location", text="位置")
        
        tree.column("name", width=150)
        tree.column("path", width=400)
        tree.column("location", width=200)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        # 加载启动项
        def load_startup_items():
            # 清空树状视图
            for item in tree.get_children():
                tree.delete(item)
            
            # 获取启动项
            startup_items = self.optimizer.manage_startup()
            
            # 添加到树状视图
            for name, value, hive, location in startup_items:
                hive_name = "HKEY_CURRENT_USER" if hive == 2147483649 else "HKEY_LOCAL_MACHINE"
                tree.insert("", tk.END, values=(name, value, f"{hive_name}\\{location}"))
        
        # 加载启动项
        load_startup_items()
        
        # 按钮框架
        button_frame = ttk.Frame(startup_window, padding="10")
        button_frame.pack(fill=tk.X)
        
        # 禁用所选启动项
        def disable_selected():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showinfo("提示", "请选择要禁用的启动项")
                return
            
            item = tree.item(selected_item[0])
            name = item["values"][0]
            location = item["values"][2]
            
            # 解析注册表位置
            if "HKEY_CURRENT_USER" in location:
                hive = 2147483649  # HKEY_CURRENT_USER
                reg_path = location.replace("HKEY_CURRENT_USER\\", "")
            else:
                hive = 2147483650  # HKEY_LOCAL_MACHINE
                reg_path = location.replace("HKEY_LOCAL_MACHINE\\", "")
            
            # 禁用启动项
            success = self.optimizer.disable_startup_item(name, hive, reg_path)
            if success:
                messagebox.showinfo("成功", f"启动项 {name} 已禁用")
                load_startup_items()
            else:
                messagebox.showerror("错误", f"禁用启动项 {name} 失败")
        
        # 按钮
        ttk.Button(button_frame, text="禁用所选", command=disable_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新", command=load_startup_items).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="关闭", command=startup_window.destroy).pack(side=tk.RIGHT, padx=5)
    
    def run(self):
        """运行GUI"""
        self.root.mainloop()
