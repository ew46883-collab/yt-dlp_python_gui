import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import subprocess
import threading
import os
import shlex
import time  # 导入时间库用于休眠
import ctypes # 导入 ctypes 用于 Windows API 调用

class YtDlpGui:
    def __init__(self, root):
        self.root = root
        self.version = 'v1.0.2'
        self.current_lang = "English"

        # --- 翻译字典 (新增右键菜单相关词条) ---
        self.translations = {
            "English": {
                "title": "YouTube Batch Downloader Pro "+self.version,
                "url_label": "Video URLs (one per line):",
                "param_label": "yt-dlp Arguments:",
                "sleep_label": "Sleep between downloads (sec):",
                "reset_btn": "Reset",
                "start_btn": "Start Download",
                "stop_btn": "Force Stop All",
                "pause_btn": "Pause",
                "resume_btn": "Resume",
                "clear_btn": "Clear Log",
                "clear_urls_btn": "Clear URLs",
                "log_label": "Execution Log:",
                "msg_empty": "Please enter video URLs!",
                "msg_stop": "EMERGENCY STOP: All processes terminated.",
                "msg_paused": "Download paused.",
                "msg_resumed": "Download resumed.",
                "msg_sleeping": "Sleeping for {} seconds before next task...",
                "status_done": "All tasks finished.",
                "menu_cut": "Cut", "menu_copy": "Copy", "menu_paste": "Paste", "menu_select_all": "Select All"
            },
            "简体中文": {
                "title": "YouTube 批量下载器专业版 "+self.version,
                "url_label": "视频链接 (每行一个):",
                "param_label": "yt-dlp 参数设置:",
                "sleep_label": "下载间隔 (秒):",
                "reset_btn": "恢复默认",
                "start_btn": "开始下载",
                "stop_btn": "强制终止所有任务",
                "pause_btn": "暂停下载",
                "resume_btn": "继续下载",
                "clear_btn": "清空日志",
                "clear_urls_btn": "一键清空链接",
                "log_label": "执行日志:",
                "msg_empty": "请输入视频链接！",
                "msg_stop": "紧急停止：已强制关闭所有下载进程。",
                "msg_paused": "下载已暂停。",
                "msg_resumed": "下载已继续。",
                "msg_sleeping": "休眠中... {} 秒后开始下一个任务...",
                "status_done": "所有任务执行完毕。",
                "menu_cut": "剪切", "menu_copy": "复制", "menu_paste": "粘贴", "menu_select_all": "全选"
            },
            "繁體中文": {"title": "YouTube 批量下載器專業版 "+self.version, "url_label": "影片連結", "param_label": "參數設置:",
                         "sleep_label": "下載間隔 (秒):", "reset_btn": "恢復預設", "start_btn": "開始下載",
                         "stop_btn": "強制終止", "pause_btn": "暫停下載", "resume_btn": "繼續下載",
                         "clear_btn": "清空日誌", "clear_urls_btn": "清空連結",
                         "log_label": "執行日誌:",
                         "msg_empty": "請輸入連結！", "msg_stop": "緊急停止。", "msg_paused": "下載已暫停。", "msg_resumed": "下載已繼續。",
                         "msg_sleeping": "休眠中... {} 秒後開始下一個任務...", "status_done": "任務結束。",
                         "menu_cut": "剪下", "menu_copy": "複製", "menu_paste": "貼上", "menu_select_all": "全選"},
            "日本語": {"title": "YouTube一括ダウンロード Pro "+self.version, "url_label": "ビデオURL", "param_label": "引数",
                       "sleep_label": "待機時間 (秒):", "reset_btn": "リセット", "start_btn": "開始",
                       "stop_btn": "強制終了", "pause_btn": "一時停止", "resume_btn": "再開",
                       "clear_btn": "ログ消去", "clear_urls_btn": "URLクリア",
                       "log_label": "ログ:",
                       "msg_empty": "URLを入力してください", "msg_stop": "停止しました。", "msg_paused": "一時停止しました。", "msg_resumed": "再開しました。",
                       "msg_sleeping": "{} 秒間待機しています...", "status_done": "完了しました。",
                       "menu_cut": "切り取り", "menu_copy": "コピー", "menu_paste": "貼り付け", "menu_select_all": "すべて選択"},
            "Français": {"title": "Téléchargeur Pro "+self.version, "url_label": "URLs", "param_label": "Arguments",
                         "sleep_label": "Pause (sec):", "reset_btn": "Reset", "start_btn": "Démarrer",
                         "stop_btn": "Arrêt Forcé", "pause_btn": "Pause", "resume_btn": "Reprendre",
                         "clear_btn": "Effacer", "clear_urls_btn": "Vider URLs",
                         "log_label": "Log:",
                         "msg_empty": "Entrez des URLs !", "msg_stop": "Arrêté.", "msg_paused": "En pause.", "msg_resumed": "Repris.",
                         "msg_sleeping": "Attente de {} secondes...", "status_done": "Terminé.",
                         "menu_cut": "Couper", "menu_copy": "Copier", "menu_paste": "Coller", "menu_select_all": "Tout sélectionner"},
            "Italiano": {"title": "Downloader Pro "+self.version, "url_label": "URL", "param_label": "Argomenti",
                         "sleep_label": "Pausa (sec):", "reset_btn": "Reset", "start_btn": "Avvia", "stop_btn": "Ferma",
                         "pause_btn": "Pausa", "resume_btn": "Riprendi",
                         "clear_btn": "Pulisci", "clear_urls_btn": "Pulisci URL",
                         "log_label": "Log:", "msg_empty": "Inserisci URL!",
                         "msg_stop": "Terminato.", "msg_paused": "In pausa.", "msg_resumed": "Ripreso.",
                         "msg_sleeping": "In pausa per {} secondi...", "status_done": "Completato.",
                         "menu_cut": "Taglia", "menu_copy": "Copia", "menu_paste": "Incolla", "menu_select_all": "Seleziona tutto"},
            "Español": {"title": "Descargador Pro "+self.version, "url_label": "URLs", "param_label": "Argumentos",
                        "sleep_label": "Espera (seg):", "reset_btn": "Reset", "start_btn": "Iniciar",
                        "stop_btn": "Detener", "pause_btn": "Pausa", "resume_btn": "Reanudar",
                        "clear_btn": "Limpiar", "clear_urls_btn": "Borrar URLs",
                        "log_label": "Log:",
                        "msg_empty": "Ingrese URLs!", "msg_stop": "Detenido.", "msg_paused": "Pausado.", "msg_resumed": "Reanudado.",
                        "msg_sleeping": "Esperando {} segundos...", "status_done": "Finalizado.",
                        "menu_cut": "Cortar", "menu_copy": "Copiar", "menu_paste": "Pegar", "menu_select_all": "Seleccionar todo"},
            "Deutsch": {"title": "Downloader Pro "+self.version, "url_label": "URLs", "param_label": "Parameter",
                        "sleep_label": "Pause (Sek):", "reset_btn": "Reset", "start_btn": "Starten",
                        "stop_btn": "Stopp", "pause_btn": "Pause", "resume_btn": "Fortsetzen",
                        "clear_btn": "Löschen", "clear_urls_btn": "URLs löschen",
                        "log_label": "Log:", "msg_empty": "URLs eingeben!",
                        "msg_stop": "Gestoppt.", "msg_paused": "Pausiert.", "msg_resumed": "Fortgesetzt.",
                        "msg_sleeping": "Warte für {} Sekunden...", "status_done": "Abgeschlossen.",
                        "menu_cut": "Ausschneiden", "menu_copy": "Kopieren", "menu_paste": "Einfügen", "menu_select_all": "Alles auswählen"},
            "Русский": {"title": "Загрузчик Pro "+self.version, "url_label": "URL", "param_label": "Аргументы",
                        "sleep_label": "Пауза (сек):", "reset_btn": "Сброс", "start_btn": "Начать", "stop_btn": "Стоп",
                        "pause_btn": "Пауза", "resume_btn": "Продолжить",
                        "clear_btn": "Очистить", "clear_urls_btn": "Очистить URL",
                        "log_label": "Лог:", "msg_empty": "Введите URL!",
                        "msg_stop": "Остановлено.", "msg_paused": "Пауза.", "msg_resumed": "Продолжено.",
                        "msg_sleeping": "Ожидание {} сек...", "status_done": "Завершено.",
                        "menu_cut": "Вырезать", "menu_copy": "Копировать", "menu_paste": "Вставить", "menu_select_all": "Выбрать все"},
            "한국어": {"title": "일괄 다운로더 Pro "+self.version, "url_label": "URL", "param_label": "매개변수", "sleep_label": "대기 시간 (초):",
                    "reset_btn": "초기화", "start_btn": "시작", "stop_btn": "강제 중지", "pause_btn": "일시정지", "resume_btn": "재개",
                    "clear_btn": "삭제", "clear_urls_btn": "URL 지우기",
                    "log_label": "로그:",
                    "msg_empty": "URL 입력!", "msg_stop": "중지됨.", "msg_paused": "일시정지됨.", "msg_resumed": "재개됨.",
                    "msg_sleeping": "{}초 동안 대기 중...", "status_done": "완료됨.",
                    "menu_cut": "잘라내기", "menu_copy": "복사", "menu_paste": "붙여넣기", "menu_select_all": "전체 선택"}
        }

        self.is_running = False
        self.is_paused = False
        self.current_process = None
        self.DEFAULT_ARGS = '--cookies "./cookies.txt" --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0" --js-runtimes node -f "bv*[height=720]+ba" -o "%(title)s[%(id)s][%(upload_date)s].%(ext)s" --embed-thumbnail --convert-thumbnails png --merge-output-format mkv --ffmpeg-location "./ffmpeg"'

        self.setup_ui()
        self.change_language("English")

    def setup_ui(self):
        self.root.geometry("900x850")

        # 语言选择
        nav_frame = tk.Frame(self.root)
        nav_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(nav_frame, text="🌍 Language:", font=("Arial", 10)).pack(side=tk.LEFT)
        self.lang_combo = ttk.Combobox(nav_frame, values=list(self.translations.keys()), state="readonly", width=15)
        self.lang_combo.set(self.current_lang)
        self.lang_combo.pack(side=tk.LEFT, padx=5)
        self.lang_combo.bind("<<ComboboxSelected>>", lambda e: self.change_language(self.lang_combo.get()))

        # URL 输入
        self.lbl_url = tk.Label(self.root, font=("Arial", 10, "bold"))
        self.lbl_url.pack(pady=(10, 0))
        self.url_input = scrolledtext.ScrolledText(self.root, height=8, width=100)
        self.url_input.pack(padx=10, pady=5)
        self.setup_context_menu() # 为输入框设置右键菜单

        # 参数设置
        self.lbl_param = tk.Label(self.root, font=("Arial", 10, "bold"))
        self.lbl_param.pack()
        param_frame = tk.Frame(self.root)
        param_frame.pack(padx=10, pady=5, fill=tk.X)
        self.param_input = tk.Entry(param_frame)
        self.param_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.param_input.insert(0, self.DEFAULT_ARGS)
        self.btn_reset = tk.Button(param_frame, command=self.reset_params)
        self.btn_reset.pack(side=tk.RIGHT)

        # 休眠间隔设置
        sleep_frame = tk.Frame(self.root)
        sleep_frame.pack(fill=tk.X, padx=10, pady=5)
        self.lbl_sleep = tk.Label(sleep_frame, font=("Arial", 10))
        self.lbl_sleep.pack(side=tk.LEFT)
        self.sleep_val = tk.Spinbox(sleep_frame, from_=0, to=3600, width=5)
        self.sleep_val.delete(0, tk.END)
        self.sleep_val.insert(0, "1")
        self.sleep_val.pack(side=tk.LEFT, padx=5)

        self.btn_clear_urls = tk.Button(sleep_frame, command=self.clear_urls, bg="#FF9800", fg="white", font=("Arial", 9, "bold"))
        self.btn_clear_urls.pack(side=tk.LEFT, padx=20)

        # 控制按钮
        ctrl_frame = tk.Frame(self.root)
        ctrl_frame.pack(pady=10)
        self.start_btn = tk.Button(ctrl_frame, command=self.toggle_download, bg="#4CAF50", fg="white", width=15,
                                   font=("Arial", 11, "bold"))
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.pause_btn = tk.Button(ctrl_frame, command=self.toggle_pause, bg="#FFC107", fg="black", width=15,
                                   font=("Arial", 11, "bold"), state="disabled")
        self.pause_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = tk.Button(ctrl_frame, command=self.force_stop_all, bg="#9e9e9e", fg="white", width=15,
                                  font=("Arial", 11, "bold"), state="disabled")
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.btn_clear = tk.Button(ctrl_frame, command=self.clear_log)
        self.btn_clear.pack(side=tk.LEFT, padx=5)

        # 日志
        self.lbl_log = tk.Label(self.root, font=("Arial", 10, "bold"))
        self.lbl_log.pack()
        self.log_output = scrolledtext.ScrolledText(self.root, height=20, width=100, state='disabled', bg="#1e1e1e",
                                                    fg="#d4d4d4")
        self.log_output.pack(padx=10, pady=5)

    def setup_context_menu(self):
        """创建并绑定右键菜单"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        
        # 定义菜单项及其对应的虚拟事件
        self.context_menu.add_command(label="Cut", command=lambda: self.root.focus_get().event_generate("<<Cut>>"))
        self.context_menu.add_command(label="Copy", command=lambda: self.root.focus_get().event_generate("<<Copy>>"))
        self.context_menu.add_command(label="Paste", command=lambda: self.root.focus_get().event_generate("<<Paste>>"))
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Select All", command=self.select_all_text)

        # 绑定右键点击事件
        self.url_input.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        """在右键点击时显示菜单"""
        # 动态启用/禁用菜单项
        try:
            # 检查剪贴板是否有内容，决定是否启用“粘贴”
            self.root.clipboard_get()
            self.context_menu.entryconfig(2, state="normal")
        except tk.TclError:
            self.context_menu.entryconfig(2, state="disabled")

        try:
            # 检查是否有选中文本，决定是否启用“剪切”和“复制”
            if self.url_input.tag_ranges("sel"):
                self.context_menu.entryconfig(0, state="normal")
                self.context_menu.entryconfig(1, state="normal")
            else:
                self.context_menu.entryconfig(0, state="disabled")
                self.context_menu.entryconfig(1, state="disabled")
        except tk.TclError:
            pass
        
        # 在鼠标位置弹出菜单
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def select_all_text(self):
        """实现文本全选功能"""
        # 使用 "break" 可以防止事件继续传播
        self.url_input.tag_add("sel", "1.0", "end")
        self.url_input.mark_set("insert", "1.0")
        self.url_input.see("insert")
        return "break"

    def change_language(self, lang_name):
        self.current_lang = lang_name
        t = self.translations[lang_name]
        self.root.title(t["title"])
        self.lbl_url.config(text=t["url_label"])
        self.lbl_param.config(text=t["param_label"])
        self.lbl_sleep.config(text=t["sleep_label"])
        self.btn_reset.config(text=t["reset_btn"])
        self.btn_clear.config(text=t["clear_btn"])
        self.btn_clear_urls.config(text=t["clear_urls_btn"])
        self.lbl_log.config(text=t["log_label"])
        self.start_btn.config(text=t["start_btn"])
        self.stop_btn.config(text=t["stop_btn"])
        
        if self.is_paused:
            self.pause_btn.config(text=t["resume_btn"])
        else:
            self.pause_btn.config(text=t["pause_btn"])
            
        # 更新右键菜单的语言
        if hasattr(self, 'context_menu'):
            self.context_menu.entryconfigure(0, label=t["menu_cut"])
            self.context_menu.entryconfigure(1, label=t["menu_copy"])
            self.context_menu.entryconfigure(2, label=t["menu_paste"])
            self.context_menu.entryconfigure(4, label=t["menu_select_all"])

    def reset_params(self):
        self.param_input.delete(0, tk.END)
        self.param_input.insert(0, self.DEFAULT_ARGS)

    def clear_urls(self):
        self.url_input.delete("1.0", tk.END)

    def log(self, message):
        self.log_output.config(state='normal')
        self.log_output.insert(tk.END, message + "\n")
        self.log_output.see(tk.END)
        self.log_output.config(state='disabled')

    def clear_log(self):
        self.log_output.config(state='normal')
        self.log_output.delete(1.0, tk.END)
        self.log_output.config(state='disabled')

    def toggle_download(self):
        if not self.is_running:
            self.start_task()

    def start_task(self):
        urls = [line.strip() for line in self.url_input.get("1.0", tk.END).split('\n') if line.strip()]
        if not urls:
            messagebox.showwarning("!", self.translations[self.current_lang]["msg_empty"])
            return

        self.is_running = True
        self.is_paused = False
        self.start_btn.config(state="disabled", bg="#cccccc")
        self.stop_btn.config(state="normal", bg="#f44336")
        self.pause_btn.config(state="normal", bg="#FFC107", text=self.translations[self.current_lang]["pause_btn"])

        thread = threading.Thread(target=self.run_downloads, args=(urls,))
        thread.daemon = True
        thread.start()

    def toggle_pause(self):
        if not self.current_process: return
        pid = self.current_process.pid
        t = self.translations[self.current_lang]
        if self.is_paused:
            self.resume_process(pid)
            self.is_paused = False
            self.pause_btn.config(text=t["pause_btn"], bg="#FFC107")
            self.log(f"[{t['msg_resumed']}]")
        else:
            self.suspend_process(pid)
            self.is_paused = True
            self.pause_btn.config(text=t["resume_btn"], bg="#2196F3")
            self.log(f"[{t['msg_paused']}]")

    def suspend_process(self, pid):
        try:
            process_handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, pid)
            if process_handle:
                ctypes.windll.ntdll.NtSuspendProcess(process_handle)
                ctypes.windll.kernel32.CloseHandle(process_handle)
        except Exception as e:
            self.log(f"Pause Error: {e}")

    def resume_process(self, pid):
        try:
            process_handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, pid)
            if process_handle:
                ctypes.windll.ntdll.NtResumeProcess(process_handle)
                ctypes.windll.kernel32.CloseHandle(process_handle)
        except Exception as e:
            self.log(f"Resume Error: {e}")

    def force_stop_all(self):
        self.is_running = False
        if self.current_process:
            try:
                if self.is_paused:
                    self.resume_process(self.current_process.pid)
                subprocess.run(['taskkill', '/F', '/T', '/PID', str(self.current_process.pid)],
                               creationflags=subprocess.CREATE_NO_WINDOW)
            except: pass
        self.log(f"\n[!!!] {self.translations[self.current_lang]['msg_stop']}")
        self.reset_ui()

    def run_downloads(self, urls):
        args_str = self.param_input.get().strip()
        user_args = shlex.split(args_str)
        yt_dlp_path = os.path.join(os.getcwd(), "yt-dlp.exe")

        try: sleep_time = int(self.sleep_val.get())
        except: sleep_time = 1

        for i, url in enumerate(urls):
            if not self.is_running: break
            self.log(f"\n>>> [{i + 1}/{len(urls)}] Processing: {url}")

            try:
                self.current_process = subprocess.Popen(
                    [yt_dlp_path] + user_args + [url],
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, encoding='utf-8', errors='replace',
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

                while self.is_running:
                    line = self.current_process.stdout.readline()
                    if not line and self.current_process.poll() is not None: break
                    if line: self.log(line.strip())

                if self.is_running and i < len(urls) - 1 and sleep_time > 0:
                    msg = self.translations[self.current_lang]["msg_sleeping"].format(sleep_time)
                    self.log(f"\n--- {msg} ---")
                    for _ in range(sleep_time):
                        if not self.is_running: break
                        while self.is_paused and self.is_running:
                            time.sleep(0.5)
                        time.sleep(1)

            except Exception as e:
                self.log(f"Error: {e}")

        if self.is_running:
            self.log(f"\n=== {self.translations[self.current_lang]['status_done']} ===")
        self.reset_ui()

    def reset_ui(self):
        self.is_running = False
        self.is_paused = False
        self.current_process = None
        self.root.after(0, lambda: self.start_btn.config(state="normal", bg="#4CAF50"))
        self.root.after(0, lambda: self.stop_btn.config(state="disabled", bg="#9e9e9e"))
        self.root.after(0, lambda: self.pause_btn.config(state="disabled", bg="#FFC107", text=self.translations[self.current_lang]["pause_btn"]))


if __name__ == "__main__":
    root = tk.Tk()
    app = YtDlpGui(root)
    root.mainloop()