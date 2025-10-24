import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import customtkinter as ctk

class FileClassifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件分类整理工具")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 设置主题
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        self.setup_ui()
        
    def setup_ui(self):
        # 创建主框架
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ctk.CTkLabel(
            main_frame, 
            text="📁 文件分类整理工具", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # 目录选择区域
        dir_frame = ctk.CTkFrame(main_frame)
        dir_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            dir_frame, 
            text="选择要整理的目录:", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        dir_selection_frame = ctk.CTkFrame(dir_frame, fg_color="transparent")
        dir_selection_frame.pack(fill="x", padx=10, pady=5)
        
        self.dir_entry = ctk.CTkEntry(
            dir_selection_frame, 
            placeholder_text="点击浏览选择目录或直接输入路径...",
            height=35
        )
        self.dir_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_button = ctk.CTkButton(
            dir_selection_frame,
            text="浏览",
            command=self.browse_directory,
            width=80,
            height=35
        )
        browse_button.pack(side="right")
        
        # 选项区域
        options_frame = ctk.CTkFrame(main_frame)
        options_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            options_frame, 
            text="分类选项:", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        # 分类方式选择
        self.classify_var = ctk.StringVar(value="extension")
        classify_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        classify_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkRadioButton(
            classify_frame,
            text="📄 按文件扩展名分类",
            variable=self.classify_var,
            value="extension"
        ).pack(side="left", padx=(0, 20))
        
        ctk.CTkRadioButton(
            classify_frame,
            text="📂 按文件类型分类",
            variable=self.classify_var,
            value="type"
        ).pack(side="left")
        
        # 操作按钮区域
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, 20))
        
        self.classify_button = ctk.CTkButton(
            button_frame,
            text="🚀 开始分类整理",
            command=self.start_classification,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#2E8B57",
            hover_color="#3CB371"
        )
        self.classify_button.pack(side="left", padx=(0, 10))
        
        self.preview_button = ctk.CTkButton(
            button_frame,
            text="👀 预览分类",
            command=self.preview_classification,
            height=40,
            font=ctk.CTkFont(size=16),
            fg_color="#1E90FF",
            hover_color="#4169E1"
        )
        self.preview_button.pack(side="left", padx=(0, 10))
        
        self.open_dir_button = ctk.CTkButton(
            button_frame,
            text="📁 打开目录",
            command=self.open_directory,
            height=40,
            font=ctk.CTkFont(size=16)
        )
        self.open_dir_button.pack(side="left")
        
        # 进度和日志区域
        log_frame = ctk.CTkFrame(main_frame)
        log_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            log_frame, 
            text="操作日志:", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        # 创建文本框和滚动条
        text_frame = ctk.CTkFrame(log_frame)
        text_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.log_text = ctk.CTkTextbox(
            text_frame,
            wrap="word",
            font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 进度条
        self.progress_bar = ctk.CTkProgressBar(main_frame)
        self.progress_bar.pack(fill="x", pady=(0, 10))
        self.progress_bar.set(0)
        
        # 状态标签
        self.status_label = ctk.CTkLabel(main_frame, text="✅ 就绪")
        self.status_label.pack()
        
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)
    
    def open_directory(self):
        directory = self.dir_entry.get().strip()
        if directory and os.path.exists(directory):
            try:
                os.startfile(directory)
            except:
                # 如果os.startfile不可用，尝试其他方法
                try:
                    import subprocess
                    if os.name == 'nt':  # Windows
                        subprocess.Popen(f'explorer "{directory}"')
                    elif os.name == 'posix':  # Linux or Mac
                        subprocess.Popen(['xdg-open', directory])
                except:
                    messagebox.showinfo("信息", f"目录路径: {directory}")
        else:
            messagebox.showwarning("警告", "请输入有效的目录路径")
    
    def log_message(self, message):
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.root.update_idletasks()
    
    def clear_log(self):
        self.log_text.delete("1.0", "end")
    
    def update_progress(self, value):
        self.progress_bar.set(value)
        self.root.update_idletasks()
    
    def update_status(self, message):
        self.status_label.configure(text=message)
        self.root.update_idletasks()
    
    def set_buttons_state(self, state):
        state = "normal" if state else "disabled"
        self.classify_button.configure(state=state)
        self.preview_button.configure(state=state)
        self.open_dir_button.configure(state=state)
    
    def get_file_type(self, extension):
        """根据文件扩展名返回文件类型"""
        file_types = {
            '图片': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.ico', '.raw'],
            '文档': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx', '.md'],
            '视频': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg'],
            '音频': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.ape', '.mid'],
            '压缩包': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso'],
            '代码': ['.py', '.java', '.cpp', '.c', '.h', '.html', '.css', '.js', '.php', '.json', '.xml', '.sql'],
            '程序': ['.exe', '.msi', '.bat', '.cmd', '.sh', '.deb', '.rpm', '.apk'],
            '字体': ['.ttf', '.otf', '.woff', '.woff2'],
            '数据': ['.csv', '.tsv', '.db', '.sqlite', '.mdb']
        }
        
        extension_lower = extension.lower()
        for file_type, extensions in file_types.items():
            if extension_lower in extensions:
                return file_type
        return '其他文件'
    
    def classify_files(self, directory, preview_only=False):
        try:
            if not directory or not os.path.exists(directory):
                messagebox.showerror("错误", "请选择有效的目录")
                return
            
            self.clear_log()
            self.set_buttons_state(False)
            self.update_progress(0)
            self.update_status("🔍 正在扫描文件..." if preview_only else "🔄 正在分类文件...")
            
            # 获取所有文件（排除目录）
            files = [f for f in os.listdir(directory) 
                    if os.path.isfile(os.path.join(directory, f))]
            
            total_files = len(files)
            if total_files == 0:
                self.log_message("❌ 没有找到可分类的文件")
                self.update_status("✅ 完成")
                self.set_buttons_state(True)
                return
            
            self.log_message(f"📊 找到 {total_files} 个文件")
            self.log_message("=" * 60)
            
            moved_files = 0
            folder_stats = {}
            
            for index, file in enumerate(files):
                file_path = os.path.join(directory, file)
                
                # 获取文件扩展名
                file_extension = os.path.splitext(file)[1]
                
                # 确定目标文件夹名称
                if self.classify_var.get() == "extension":
                    if file_extension:
                        folder_name = file_extension[1:].upper() + "文件"
                    else:
                        folder_name = "无扩展名文件"
                else:  # 按类型分类
                    folder_name = self.get_file_type(file_extension)
                
                # 统计文件夹信息
                if folder_name not in folder_stats:
                    folder_stats[folder_name] = 0
                folder_stats[folder_name] += 1
                
                folder_path = os.path.join(directory, folder_name)
                
                if preview_only:
                    self.log_message(f"📋 [预览] '{file}' -> '{folder_name}/'")
                else:
                    # 创建分类文件夹（如果不存在）
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                        self.log_message(f"📁 创建文件夹: '{folder_name}'")
                    
                    # 移动文件到分类文件夹
                    source_path = os.path.join(directory, file)
                    destination_path = os.path.join(folder_path, file)
                    
                    try:
                        shutil.move(source_path, destination_path)
                        self.log_message(f"✅ 移动: '{file}' -> '{folder_name}/'")
                        moved_files += 1
                    except Exception as e:
                        self.log_message(f"❌ 错误: 无法移动文件 '{file}': {str(e)}")
                
                # 更新进度
                progress = (index + 1) / total_files
                self.update_progress(progress)
            
            # 显示结果摘要
            self.log_message("=" * 60)
            if preview_only:
                self.log_message("📈 分类统计:")
                for folder, count in folder_stats.items():
                    self.log_message(f"   📂 {folder}: {count} 个文件")
                self.log_message(f"🎯 预览完成: 共 {total_files} 个文件将被分类")
                self.update_status("✅ 预览完成")
            else:
                self.log_message("📈 分类统计:")
                for folder, count in folder_stats.items():
                    self.log_message(f"   📂 {folder}: {count} 个文件")
                self.log_message(f"🎉 分类完成: 成功移动 {moved_files}/{total_files} 个文件")
                self.update_status("✅ 分类完成")
                if moved_files > 0:
                    messagebox.showinfo("完成", 
                                      f"文件分类完成！\n\n"
                                      f"📊 总文件数: {total_files}\n"
                                      f"✅ 成功移动: {moved_files}\n"
                                      f"📂 创建分类: {len(folder_stats)} 个")
            
        except Exception as e:
            error_msg = f"❌ 发生错误: {str(e)}"
            self.log_message(error_msg)
            self.update_status("❌ 错误")
            messagebox.showerror("错误", error_msg)
        finally:
            self.set_buttons_state(True)
    
    def start_classification(self):
        directory = self.dir_entry.get().strip()
        if not directory:
            messagebox.showwarning("警告", "请先选择要整理的目录")
            return
        
        # 确认对话框
        result = messagebox.askyesno("确认", 
                                   "确定要开始分类文件吗？\n此操作将移动文件到相应的分类文件夹。")
        if not result:
            return
        
        # 在新线程中执行分类操作
        thread = threading.Thread(
            target=self.classify_files,
            args=(directory, False)
        )
        thread.daemon = True
        thread.start()
    
    def preview_classification(self):
        directory = self.dir_entry.get().strip()
        if not directory:
            messagebox.showwarning("警告", "请先选择要整理的目录")
            return
        
        # 在新线程中执行预览操作
        thread = threading.Thread(
            target=self.classify_files,
            args=(directory, True)
        )
        thread.daemon = True
        thread.start()

def main():
    try:
        # 创建主窗口
        root = ctk.CTk()
        app = FileClassifierApp(root)
        
        # 启动主循环
        root.mainloop()
    except Exception as e:
        print(f"程序启动错误: {e}")
        input("按回车键退出...")

if __name__ == "__main__":
    main()
