import tkinter as tk
from tkinter import font
import platform
import threading
import pygame  # 需要先安裝: pip install pygame

class GameTimerApp:
    # ==========================================
    # ⏱️ 參數設定區：統一在這裡修改倒數秒數
    # ==========================================
    TIMER_1_SECONDS = 300  # 第一組倒數 (原5分鐘)，預設 300 秒
    TIMER_2_SECONDS = 600  # 第二組倒數 (原10分鐘)，預設 600 秒
    # ==========================================

    def __init__(self, root):
        self.root = root
        self.root.title("輔助計時器")
        
        # 初始化 pygame 音效引擎
        pygame.mixer.init()
        # 設定音樂檔案名稱 (請確保檔案在同一資料夾)
        self.music_file = "alert.mp3" 

        # 設定視窗半透明與置頂
        self.root.attributes('-alpha', 0.8) 
        self.root.attributes('-topmost', True) 
        self.root.geometry("320x180") 
        self.root.resizable(False, False)

        # 時間變數初始化
        self.total_seconds = 0
        self.countdown_seconds = self.TIMER_1_SECONDS       
        self.countdown_10m_seconds = self.TIMER_2_SECONDS   
        self.is_popup_open = False

        # 設定字型
        custom_font = font.Font(size=14, weight="bold")
        btn_font = font.Font(family="微軟正黑體", size=10)

        # 介面標籤
        self.total_label = tk.Label(root, text="總時間: 00:00:00", font=custom_font)
        self.total_label.pack(pady=5)

        self.countdown_label = tk.Label(root, text=f"五分倒數: {self.format_time(self.countdown_seconds)}", font=custom_font, fg="red")
        self.countdown_label.pack(pady=2)

        self.countdown_10m_label = tk.Label(root, text=f"十分倒數: {self.format_time(self.countdown_10m_seconds)}", font=custom_font, fg="#0066cc")
        self.countdown_10m_label.pack(pady=2)

        # 按鈕框架
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=8)

        tk.Button(btn_frame, text="重置總時", font=btn_font, command=self.reset_total_time).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="重置五分", font=btn_font, command=self.reset_countdown_time).grid(row=0, column=1, padx=6)
        tk.Button(btn_frame, text="重置十分", font=btn_font, command=self.reset_10m_time).grid(row=0, column=2, padx=6)

        # 啟動計時器
        self.update_timer()

    def format_time(self, seconds, full=False):
        """格式化時間顯示"""
        m, s = divmod(seconds, 60)
        if full:
            h, m = divmod(m, 60)
            return f"{h:02d}:{m:02d}:{s:02d}"
        return f"{m:02d}:{s:02d}"

    def update_timer(self):
        """每秒更新一次計時器狀態"""
        # 總時間遞增
        self.total_seconds += 1
        self.total_label.config(text=f"總時間: {self.format_time(self.total_seconds, True)}")

        # 第一組倒數邏輯 (受彈窗影響)
        if not self.is_popup_open:
            if self.countdown_seconds > 0:
                self.countdown_seconds -= 1
                self.countdown_label.config(text=f"五分倒數: {self.format_time(self.countdown_seconds)}")
            else:
                self.show_popup()

        # 第二組倒數邏輯 (獨立計算)
        if self.countdown_10m_seconds > 0:
            self.countdown_10m_seconds -= 1
            self.countdown_10m_label.config(text=f"十分倒數: {self.format_time(self.countdown_10m_seconds)}")

        # 設定 1 秒後再次執行此函數
        self.root.after(1000, self.update_timer)

    def play_music(self):
        """播放 MP3 音樂"""
        try:
            if pygame.mixer.music.get_busy():
                return
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.play(-1) 
        except Exception as e:
            print(f"無法播放音樂: {e}")

    def stop_music(self):
        """停止音樂"""
        pygame.mixer.music.stop()

    def show_popup(self):
        """顯示提醒彈窗並播放音樂"""
        self.is_popup_open = True
        self.play_music() 
        
        self.popup = tk.Toplevel(self.root)
        self.popup.title("提醒")
        self.popup.geometry("300x150")
        self.popup.attributes('-topmost', True)
        self.popup.attributes('-alpha', 0.95)

        tk.Label(self.popup, text="五分鐘到", font=("微軟正黑體", 16, "bold"), fg="blue").pack(expand=True, pady=10)
        tk.Button(self.popup, text="確認", font=("微軟正黑體", 14), command=self.close_popup, width=10).pack(pady=10)

        self.popup.protocol("WM_DELETE_WINDOW", self.close_popup)

    def close_popup(self):
        """關閉彈窗"""
        self.stop_music() 
        self.popup.destroy()
        self.countdown_seconds = self.TIMER_1_SECONDS 
        self.countdown_label.config(text=f"五分倒數: {self.format_time(self.countdown_seconds)}")
        self.is_popup_open = False

    def reset_total_time(self):
        """手動重置總時間"""
        self.total_seconds = 0
        self.total_label.config(text=f"總時間: {self.format_time(0, True)}")

    def reset_countdown_time(self):
        """手動重置第一組倒數"""
        if self.is_popup_open:
            self.close_popup()
        else:
            self.countdown_seconds = self.TIMER_1_SECONDS
            self.countdown_label.config(text=f"五分倒數: {self.format_time(self.TIMER_1_SECONDS)}")

    def reset_10m_time(self):
        """手動重置第二組倒數"""
        self.countdown_10m_seconds = self.TIMER_2_SECONDS
        self.countdown_10m_label.config(text=f"十分倒數: {self.format_time(self.TIMER_2_SECONDS)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GameTimerApp(root)
    root.mainloop()
