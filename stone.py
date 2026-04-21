import tkinter as tk
from tkinter import font

class GameTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("輔助計時器")
        
        # 設定視窗半透明 (0.0 完全透明 ~ 1.0 完全不透明)
        self.root.attributes('-alpha', 0.8) 
        # 設定視窗永遠置頂
        self.root.attributes('-topmost', True) 
        self.root.geometry("250x120")
        self.root.resizable(False, False)

        # 時間變數初始化
        self.total_seconds = 0
        self.countdown_seconds = 300  # 5分鐘 = 300秒
        self.is_popup_open = False

        # 設定字型
        custom_font = font.Font(size=14, weight="bold")

        # 總時間標籤
        self.total_label = tk.Label(root, text="總時間: 00:00:00", font=custom_font)
        self.total_label.pack(pady=10)

        # 倒數計時標籤
        self.countdown_label = tk.Label(root, text="倒數: 05:00", font=custom_font, fg="red")
        self.countdown_label.pack(pady=5)

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

        # 如果彈窗沒有開啟，才進行倒數
        if not self.is_popup_open:
            if self.countdown_seconds > 0:
                self.countdown_seconds -= 1
                self.countdown_label.config(text=f"倒數: {self.format_countdown_time(self.countdown_seconds)}")
            else:
                self.show_popup()

        # 設定 1000 毫秒 (1秒) 後再次執行此函數
        self.root.after(1000, self.update_timer)

    def show_popup(self):
        """顯示提醒彈窗"""
        self.is_popup_open = True
        
        # 建立獨立的彈出視窗
        self.popup = tk.Toplevel(self.root)
        self.popup.title("!!! 提醒 !!!")
        self.popup.geometry("300x150")
        self.popup.attributes('-topmost', True) # 彈窗也永遠置頂
        self.popup.attributes('-alpha', 0.95)   # 彈窗稍微不透明一點以引起注意
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

        # 綁定視窗右上角的 'X' 關閉事件與確認按鈕相同邏輯
        self.popup.protocol("WM_DELETE_WINDOW", self.close_popup)

    def close_popup(self):
        """關閉彈窗並重置計時器"""
        self.popup.destroy()
        # 重新設定倒數 5 分鐘
        self.countdown_seconds = 300
        self.countdown_label.config(text=f"倒數: {self.format_countdown_time(self.countdown_seconds)}")
        # 標記彈窗已關閉，讓倒數重新開始
        self.is_popup_open = False

if __name__ == "__main__":
    root = tk.Tk()
    app = GameTimerApp(root)
    root.mainloop()
