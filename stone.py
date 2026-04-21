import tkinter as tk
from tkinter import font
import platform

# 檢查是否在 Windows 環境並載入音效模組
try:
    import winsound
    has_winsound = True
except ImportError:
    has_winsound = False

class GameTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("輔助計時器")
        
        # 設定視窗半透明 (0.0 完全透明 ~ 1.0 完全不透明)
        self.root.attributes('-alpha', 0.8) 
        # 設定視窗永遠置頂
        self.root.attributes('-topmost', True) 
        # 調整視窗大小以容納三個計時器與三個按鈕
        self.root.geometry("320x180") 
        self.root.resizable(False, False)

        # 時間變數初始化
        self.total_seconds = 0
        self.countdown_seconds = 300       # 5分鐘 = 300秒
        self.countdown_10m_seconds = 600   # 10分鐘 = 600秒
        self.is_popup_open = False
        self.sound_job = None              # 用來記錄音效循環的任務

        # 設定字型
        custom_font = font.Font(size=14, weight="bold")
        btn_font = font.Font(family="微軟正黑體", size=10)

        # 總時間標籤
        self.total_label = tk.Label(root, text="總時間: 00:00:00", font=custom_font)
        self.total_label.pack(pady=5)

        # 5分鐘倒數計時標籤 (紅色)
        self.countdown_label = tk.Label(root, text="五分倒數: 05:00", font=custom_font, fg="red")
        self.countdown_label.pack(pady=2)

        # 10分鐘倒數計時標籤 (藍色)
        self.countdown_10m_label = tk.Label(root, text="十分倒數: 10:00", font=custom_font, fg="#0066cc")
        self.countdown_10m_label.pack(pady=2)

        # 建立一個框架來放置按鈕，讓它們水平並排
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=8)

        # 重置總時間按鈕
        self.btn_reset_total = tk.Button(btn_frame, text="重置總時", font=btn_font, command=self.reset_total_time)
        self.btn_reset_total.grid(row=0, column=0, padx=6)

        # 重置5分倒數按鈕
        self.btn_reset_cd = tk.Button(btn_frame, text="重置五分", font=btn_font, command=self.reset_countdown_time)
        self.btn_reset_cd.grid(row=0, column=1, padx=6)

        # 重置10分倒數按鈕
        self.btn_reset_10m = tk.Button(btn_frame, text="重置十分", font=btn_font, command=self.reset_10m_time)
        self.btn_reset_10m.grid(row=0, column=2, padx=6)

        # 啟動計時器迴圈
        self.update_timer()

    def format_total_time(self, seconds):
        """格式化總時間 (時:分:秒)"""
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    def format_countdown_time(self, seconds):
        """格式化倒數時間 (分:秒)"""
        m, s = divmod(seconds, 60)
        return f"{m:02d}:{s:02d}"

    def update_timer(self):
        # 總時間不斷增加
        self.total_seconds += 1
        self.total_label.config(text=f"總時間: {self.format_total_time(self.total_seconds)}")

        # 5分鐘倒數邏輯 (受彈窗影響)
        if not self.is_popup_open:
            if self.countdown_seconds > 0:
                self.countdown_seconds -= 1
                self.countdown_label.config(text=f"五分倒數: {self.format_countdown_time(self.countdown_seconds)}")
            else:
                self.show_popup()

        # 10分鐘倒數邏輯 (獨立計算，不受彈窗影響)
        if self.countdown_10m_seconds > 0:
            self.countdown_10m_seconds -= 1
            self.countdown_10m_label.config(text=f"十分倒數: {self.format_countdown_time(self.countdown_10m_seconds)}")

        # 設定 1000 毫秒 (1秒) 後再次執行此函數
        self.root.after(1000, self.update_timer)

    def play_periodic_sound(self):
        """播放間隔性的柔和提示音 (每3秒一次)"""
        if self.is_popup_open and platform.system() == "Windows" and has_winsound:
            try:
                # 改用 SystemDefault (通常是較短的叮聲)，且不使用 SND_LOOP
                winsound.PlaySound("SystemDefault", winsound.SND_ALIAS | winsound.SND_ASYNC)
                # 設定 5000 毫秒 (5秒) 後再次呼叫自己，形成帶有間隔的循環
                self.sound_job = self.root.after(5000, self.play_periodic_sound)
            except Exception:
                pass

    def stop_sound(self):
        """停止播放聲音"""
        # 取消等待中的音效任務
        if self.sound_job is not None:
            self.root.after_cancel(self.sound_job)
            self.sound_job = None
            
        if platform.system() == "Windows" and has_winsound:
            try:
                # 中斷正在播放的音效
                winsound.PlaySound(None, winsound.SND_PURGE)
            except Exception:
                pass

    def show_popup(self):
        """顯示提醒彈窗"""
        self.is_popup_open = True
        
        # 開始播放間隔性音效
        self.play_periodic_sound()
        
        # 建立獨立的彈出視窗
        self.popup = tk.Toplevel(self.root)
        self.popup.title("!!! 提醒 !!!")
        self.popup.geometry("300x150")
        self.popup.attributes('-topmost', True) 
        self.popup.attributes('-alpha', 0.95)   
        self.popup.resizable(False, False)

        # 彈窗文字內容
        lbl = tk.Label(
            self.popup, 
            text="五分鐘到", 
            font=("微軟正黑體", 16, "bold"), 
            fg="blue"
        )
        lbl.pack(expand=True, pady=10)

        # 確認按鈕
        btn = tk.Button(
            self.popup, 
            text="確認", 
            font=("微軟正黑體", 14), 
            command=self.close_popup,
            bg="#e0e0e0",
            width=10
        )
        btn.pack(pady=10)

        self.popup.protocol("WM_DELETE_WINDOW", self.close_popup)

    def close_popup(self):
        """關閉彈窗並重置5分鐘計時器與停止音效"""
        self.stop_sound() # 停止音效
        self.popup.destroy()
        self.countdown_seconds = 300 
        self.countdown_label.config(text=f"五分倒數: {self.format_countdown_time(self.countdown_seconds)}")
        self.is_popup_open = False

    def reset_total_time(self):
        """手動重置總時間"""
        self.total_seconds = 0
        self.total_label.config(text=f"總時間: {self.format_total_time(self.total_seconds)}")

    def reset_countdown_time(self):
        """手動重置5分鐘倒數時間"""
        if self.is_popup_open:
            self.close_popup() # 這裡已經包含了停止音效的邏輯
        else:
            self.countdown_seconds = 300
            self.countdown_label.config(text=f"五分倒數: {self.format_countdown_time(self.countdown_seconds)}")

    def reset_10m_time(self):
        """手動重置10分鐘倒數時間"""
        self.countdown_10m_seconds = 600
        self.countdown_10m_label.config(text=f"十分倒數: {self.format_countdown_time(self.countdown_10m_seconds)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GameTimerApp(root)
    root.mainloop()
