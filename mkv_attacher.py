import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import subprocess
import os
import threading
from pathlib import Path


class MKVAttachmentTool:
    def __init__(self, root):
        self.root = root
        self.root.title("MKV 批量附件添加工具 (基于 mkvpropedit)")
        self.root.geometry("700x600")

        # 变量存储
        self.mkv_files = []
        self.attachment_files = []
        self.mkvtoolnix_path = tk.StringVar(value=r"C:\Program Files\MKVToolNix\mkvpropedit.exe")

        self.create_widgets()

    def create_widgets(self):
        # --- 设置区域 ---
        frame_settings = tk.LabelFrame(self.root, text="设置", padx=5, pady=5)
        frame_settings.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_settings, text="mkvpropedit.exe 路径:").pack(side="left")
        tk.Entry(frame_settings, textvariable=self.mkvtoolnix_path).pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(frame_settings, text="浏览", command=self.select_exe).pack(side="left")

        # --- MKV 文件选择区域 ---
        frame_mkv = tk.LabelFrame(self.root, text="1. 选择视频文件 (MKV)", padx=5, pady=5)
        frame_mkv.pack(fill="both", expand=True, padx=10, pady=5)

        btn_frame_mkv = tk.Frame(frame_mkv)
        btn_frame_mkv.pack(fill="x")
        tk.Button(btn_frame_mkv, text="添加文件", command=self.add_files).pack(side="left", padx=5)
        tk.Button(btn_frame_mkv, text="添加目录", command=self.add_folder).pack(side="left", padx=5)
        tk.Button(btn_frame_mkv, text="清空列表", command=lambda: self.clear_list(self.list_mkv, self.mkv_files)).pack(
            side="left", padx=5)

        self.list_mkv = tk.Listbox(frame_mkv, selectmode=tk.EXTENDED, height=6)
        self.list_mkv.pack(fill="both", expand=True, pady=5)

        # --- 附件选择区域 ---
        frame_att = tk.LabelFrame(self.root, text="2. 选择附件文件 (字体/图片/字幕等)", padx=5, pady=5)
        frame_att.pack(fill="both", expand=True, padx=10, pady=5)

        btn_frame_att = tk.Frame(frame_att)
        btn_frame_att.pack(fill="x")
        tk.Button(btn_frame_att, text="添加附件", command=self.add_attachments).pack(side="left", padx=5)
        tk.Button(btn_frame_att, text="清空列表",
                  command=lambda: self.clear_list(self.list_att, self.attachment_files)).pack(side="left", padx=5)

        self.list_att = tk.Listbox(frame_att, selectmode=tk.EXTENDED, height=4)
        self.list_att.pack(fill="both", expand=True, pady=5)

        # --- 操作与日志区域 ---
        frame_action = tk.Frame(self.root, padx=5, pady=5)
        frame_action.pack(fill="both", expand=True, padx=10)

        self.btn_run = tk.Button(frame_action, text="开始处理", command=self.start_processing_thread, bg="#DDDDDD",
                                 font=("Arial", 10, "bold"))
        self.btn_run.pack(fill="x", pady=5)

        self.progress = ttk.Progressbar(frame_action, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", pady=2)

        self.log_area = scrolledtext.ScrolledText(frame_action, height=8, state='disabled')
        self.log_area.pack(fill="both", expand=True)

    # --- 逻辑功能 ---

    def log(self, message):
        """线程安全的日志输出"""
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def select_exe(self):
        filename = filedialog.askopenfilename(title="选择 mkvpropedit.exe", filetypes=[("Executable", "*.exe")])
        if filename:
            self.mkvtoolnix_path.set(filename)

    def add_files(self):
        files = filedialog.askopenfilenames(title="选择 MKV 文件", filetypes=[("MKV Video", "*.mkv")])
        for f in files:
            if f not in self.mkv_files:
                self.mkv_files.append(f)
                self.list_mkv.insert(tk.END, f)

    def add_folder(self):
        folder = filedialog.askdirectory(title="选择包含 MKV 的文件夹")
        if folder:
            count = 0
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith(".mkv"):
                        full_path = os.path.join(root, file)
                        if full_path not in self.mkv_files:
                            self.mkv_files.append(full_path)
                            self.list_mkv.insert(tk.END, full_path)
                            count += 1
            self.log(f"已从目录添加 {count} 个 MKV 文件。")

    def add_attachments(self):
        files = filedialog.askopenfilenames(title="选择附件文件")
        for f in files:
            # 检查大小 < 2GB (2 * 1024 * 1024 * 1024 bytes)
            size_bytes = os.path.getsize(f)
            if size_bytes >= 2 * 1024 ** 3:
                messagebox.showerror("错误", f"附件 {os.path.basename(f)} 太大！\n单个附件必须小于 2GB。")
                continue

            if f not in self.attachment_files:
                self.attachment_files.append(f)
                self.list_att.insert(tk.END, f"{os.path.basename(f)} ({size_bytes / 1024 / 1024:.2f} MB)")

    def clear_list(self, listbox, data_list):
        listbox.delete(0, tk.END)
        data_list.clear()

    def start_processing_thread(self):
        if not self.mkv_files:
            messagebox.showwarning("提示", "请先添加 MKV 文件！")
            return
        if not self.attachment_files:
            messagebox.showwarning("提示", "请先添加附件！")
            return
        exe = self.mkvtoolnix_path.get()
        if not os.path.exists(exe):
            messagebox.showerror("错误", "找不到 mkvpropedit.exe，请在设置中指定正确路径。")
            return

        # 禁用按钮防止重复点击
        self.btn_run.config(state="disabled")
        self.progress['value'] = 0
        self.progress['maximum'] = len(self.mkv_files)

        # 开启新线程
        threading.Thread(target=self.process_logic, daemon=True).run()

    def process_logic(self):
        exe_path = self.mkvtoolnix_path.get()
        success_count = 0

        self.log("-" * 30)
        self.log("开始批量处理...")

        for idx, mkv_file in enumerate(self.mkv_files):
            filename = os.path.basename(mkv_file)
            self.log(f"正在处理: {filename}")

            # 构建命令
            # 格式: mkvpropedit "video.mkv" --add-attachment "att1" --add-attachment "att2"
            cmd = [exe_path, mkv_file]

            for att in self.attachment_files:
                cmd.append("--add-attachment")
                cmd.append(att)

            try:
                # hide_window flag 用于隐藏弹出的 cmd 窗口 (Windows specific)
                startupinfo = None
                if os.name == 'nt':
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    startupinfo=startupinfo,
                    encoding='utf-8',  # 防止中文路径乱码
                    errors='replace'
                )

                if result.returncode == 0:
                    self.log(f"✅ 成功: {filename}")
                    success_count += 1
                else:
                    self.log(f"❌ 失败: {filename}")
                    self.log(f"错误信息: {result.stderr}")

            except Exception as e:
                self.log(f"❌ 异常: {e}")

            # 更新进度条
            self.root.after(0, lambda v=idx + 1: self.progress.configure(value=v))

        self.log("-" * 30)
        self.log(f"处理完成。成功: {success_count}/{len(self.mkv_files)}")
        self.btn_run.config(state="normal")
        messagebox.showinfo("完成", f"批量任务结束！\n成功: {success_count} 个文件")


if __name__ == "__main__":
    root = tk.Tk()
    # 尝试设置高 DPI 清晰度 (Windows)
    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

    app = MKVAttachmentTool(root)
    root.mainloop()