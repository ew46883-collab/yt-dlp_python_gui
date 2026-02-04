import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import subprocess
import threading
import os
import shlex
import time  # 导入时间库用于休眠


class YtDlpGui:
    def __init__(self, root):
        self.root = root
        self.current_lang = "English"

        # --- 翻译字典 (新增休眠功能相关词条) ---
        self.translations = {
            "English": {
                "title": "YouTube Batch Downloader Pro",
                "url_label": "Video URLs (one per line):",
                "param_label": "yt-dlp Arguments:",
                "sleep_label": "Sleep between downloads (sec):",
                "reset_btn": "Reset",
                "start_btn": "Start Download",
                "stop_btn": "Force Stop All",
                "clear_btn": "Clear Log",
                "log_label": "Execution Log:",
                "msg_empty": "Please enter video URLs!",
                "msg_stop": "EMERGENCY STOP: All processes terminated.",
                "msg_sleeping": "Sleeping for {} seconds before next task...",
                "status_done": "All tasks finished."
            },
            "简体中文": {
                "title": "YouTube 批量下载器专业版",
                "url_label": "视频链接 (每行一个):",
                "param_label": "yt-dlp 参数设置:",
                "sleep_label": "下载间隔 (秒):",
                "reset_btn": "恢复默认",
                "start_btn": "开始下载",
                "stop_btn": "强制终止所有任务",
                "clear_btn": "清空日志",
                "log_label": "执行日志:",
                "msg_empty": "请输入视频链接！",
                "msg_stop": "紧急停止：已强制关闭所有下载进程。",
                "msg_sleeping": "休眠中... {} 秒后开始下一个任务...",
                "status_done": "所有任务执行完毕。"
            },
            "繁體中文": {"title": "YouTube 批量下載器專業版", "url_label": "影片連結", "param_label": "參數設置:",
                         "sleep_label": "下載間隔 (秒):", "reset_btn": "恢復預設", "start_btn": "開始下載",
                         "stop_btn": "強制終止", "clear_btn": "清空日誌", "log_label": "執行日誌:",
                         "msg_empty": "請輸入連結！", "msg_stop": "緊急停止。",
                         "msg_sleeping": "休眠中... {} 秒後開始下一個任務...", "status_done": "任務結束。"},
            "日本語": {"title": "YouTube一括ダウンロード Pro", "url_label": "ビデオURL", "param_label": "引数",
                       "sleep_label": "待機時間 (秒):", "reset_btn": "リセット", "start_btn": "開始",
                       "stop_btn": "強制終了", "clear_btn": "ログ消去", "log_label": "ログ:",
                       "msg_empty": "URLを入力してください", "msg_stop": "停止しました。",
                       "msg_sleeping": "{} 秒間待機しています...", "status_done": "完了しました。"},
            "Français": {"title": "Téléchargeur Pro", "url_label": "URLs", "param_label": "Arguments",
                         "sleep_label": "Pause (sec):", "reset_btn": "Reset", "start_btn": "Démarrer",
                         "stop_btn": "Arrêt Forcé", "clear_btn": "Effacer", "log_label": "Log:",
                         "msg_empty": "Entrez des URLs !", "msg_stop": "Arrêté.",
                         "msg_sleeping": "Attente de {} secondes...", "status_done": "Terminé."},
            "Italiano": {"title": "Downloader Pro", "url_label": "URL", "param_label": "Argomenti",
                         "sleep_label": "Pausa (sec):", "reset_btn": "Reset", "start_btn": "Avvia", "stop_btn": "Ferma",
                         "clear_btn": "Pulisci", "log_label": "Log:", "msg_empty": "Inserisci URL!",
                         "msg_stop": "Terminato.", "msg_sleeping": "In pausa per {} secondi...",
                         "status_done": "Completato."},
            "Español": {"title": "Descargador Pro", "url_label": "URLs", "param_label": "Argumentos",
                        "sleep_label": "Espera (seg):", "reset_btn": "Reset", "start_btn": "Iniciar",
                        "stop_btn": "Detener", "clear_btn": "Limpiar", "log_label": "Log:",
                        "msg_empty": "Ingrese URLs!", "msg_stop": "Detenido.",
                        "msg_sleeping": "Esperando {} segundos...", "status_done": "Finalizado."},
            "Deutsch": {"title": "Downloader Pro", "url_label": "URLs", "param_label": "Parameter",
                        "sleep_label": "Pause (Sek):", "reset_btn": "Reset", "start_btn": "Starten",
                        "stop_btn": "Stopp", "clear_btn": "Löschen", "log_label": "Log:", "msg_empty": "URLs eingeben!",
                        "msg_stop": "Gestoppt.", "msg_sleeping": "Warte für {} Sekunden...",
                        "status_done": "Abgeschlossen."},
            "Русский": {"title": "Загрузчик Pro", "url_label": "URL", "param_label": "Аргументы",
                        "sleep_label": "Пауза (сек):", "reset_btn": "Сброс", "start_btn": "Начать", "stop_btn": "Стоп",
                        "clear_btn": "Очистить", "log_label": "Лог:", "msg_empty": "Введите URL!",
                        "msg_stop": "Остановлено.", "msg_sleeping": "Ожидание {} сек...", "status_done": "Завершено."},
            "한국어": {"title": "일괄 다운로더 Pro", "url_label": "URL", "param_label": "매개변수", "sleep_label": "대기 시간 (초):",
                    "reset_btn": "초기화", "start_btn": "시작", "stop_btn": "강제 중지", "clear_btn": "삭제", "log_label": "로그:",
                    "msg_empty": "URL 입력!", "msg_stop": "중지됨.", "msg_sleeping": "{}초 동안 대기 중...", "status_done": "완료됨."}
        }

        self.is_running = False
        self.current_process = None
        self.DEFAULT_ARGS = '--cookies "./cookies.txt" --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0" --js-runtimes node -f "bv*[height=720]+ba" --embed-thumbnail --convert-thumbnails png --merge-output-format mkv'

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

        # 休眠间隔设置 (新增)
        sleep_frame = tk.Frame(self.root)
        sleep_frame.pack(fill=tk.X, padx=10, pady=5)
        self.lbl_sleep = tk.Label(sleep_frame, font=("Arial", 10))
        self.lbl_sleep.pack(side=tk.LEFT)
        self.sleep_val = tk.Spinbox(sleep_frame, from_=0, to=3600, width=5)
        self.sleep_val.delete(0, tk.END)
        self.sleep_val.insert(0, "1")  # 默认 1 秒
        self.sleep_val.pack(side=tk.LEFT, padx=5)

        # 控制按钮
        ctrl_frame = tk.Frame(self.root)
        ctrl_frame.pack(pady=10)
        self.start_btn = tk.Button(ctrl_frame, command=self.toggle_download, bg="#4CAF50", fg="white", width=20,
                                   font=("Arial", 11, "bold"))
        self.start_btn.pack(side=tk.LEFT, padx=10)
        self.stop_btn = tk.Button(ctrl_frame, command=self.force_stop_all, bg="#9e9e9e", fg="white", width=20,
                                  font=("Arial", 11, "bold"), state="disabled")
        self.stop_btn.pack(side=tk.LEFT, padx=10)
        self.btn_clear = tk.Button(ctrl_frame, command=self.clear_log)
        self.btn_clear.pack(side=tk.LEFT, padx=10)

        # 日志
        self.lbl_log = tk.Label(self.root, font=("Arial", 10, "bold"))
        self.lbl_log.pack()
        self.log_output = scrolledtext.ScrolledText(self.root, height=20, width=100, state='disabled', bg="#1e1e1e",
                                                    fg="#d4d4d4")
        self.log_output.pack(padx=10, pady=5)

    def change_language(self, lang_name):
        self.current_lang = lang_name
        t = self.translations[lang_name]
        self.root.title(t["title"])
        self.lbl_url.config(text=t["url_label"])
        self.lbl_param.config(text=t["param_label"])
        self.lbl_sleep.config(text=t["sleep_label"])
        self.btn_reset.config(text=t["reset_btn"])
        self.btn_clear.config(text=t["clear_btn"])
        self.lbl_log.config(text=t["log_label"])
        self.start_btn.config(text=t["start_btn"])
        self.stop_btn.config(text=t["stop_btn"])

    def reset_params(self):
        self.param_input.delete(0, tk.END)
        self.param_input.insert(0, self.DEFAULT_ARGS)

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
        self.start_btn.config(state="disabled", bg="#cccccc")
        self.stop_btn.config(state="normal", bg="#f44336")

        thread = threading.Thread(target=self.run_downloads, args=(urls,))
        thread.daemon = True
        thread.start()

    def force_stop_all(self):
        self.is_running = False
        if self.current_process:
            try:
                subprocess.run(['taskkill', '/F', '/T', '/PID', str(self.current_process.pid)],
                               creationflags=subprocess.CREATE_NO_WINDOW)
            except:
                pass
        self.log(f"\n[!!!] {self.translations[self.current_lang]['msg_stop']}")
        self.reset_ui()

    def run_downloads(self, urls):
        args_str = self.param_input.get().strip()
        user_args = shlex.split(args_str)
        yt_dlp_path = os.path.join(os.getcwd(), "yt-dlp.exe")

        # 获取休眠时间设置
        try:
            sleep_time = int(self.sleep_val.get())
        except:
            sleep_time = 1

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

                # 如果任务成功完成，且不是最后一个视频，则进入休眠
                if self.is_running and i < len(urls) - 1 and sleep_time > 0:
                    msg = self.translations[self.current_lang]["msg_sleeping"].format(sleep_time)
                    self.log(f"\n--- {msg} ---")
                    # 为了在休眠时仍能响应“停止”按钮，我们将大休眠切成小段
                    for _ in range(sleep_time):
                        if not self.is_running: break
                        time.sleep(1)

            except Exception as e:
                self.log(f"Error: {e}")

        if self.is_running:
            self.log(f"\n=== {self.translations[self.current_lang]['status_done']} ===")
        self.reset_ui()

    def reset_ui(self):
        self.is_running = False
        self.current_process = None
        self.root.after(0, lambda: self.start_btn.config(state="normal", bg="#4CAF50"))
        self.root.after(0, lambda: self.stop_btn.config(state="disabled", bg="#9e9e9e"))


if __name__ == "__main__":
    root = tk.Tk()
    app = YtDlpGui(root)
    root.mainloop()