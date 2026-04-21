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
        # 稍微加高與加寬視窗，以容納新增的按鈕
        self.root.geometry("280x150") 
        self.root.resizable(False, False)

        # 時間變數初始化
        self.total_seconds = 0
        self.countdown_seconds = 300  # 5分鐘 = 300秒
        self.is_popup_open = False

        # 設定字型
        custom_font = font.Font(size=14, weight="bold")
        btn_font = font.Font(family="微軟正黑體", size=10)

        # 總時間標籤
        self.total_label = tk.Label(root, text="總時間: 00:00:00", font=custom_font)
        self.total_label.pack(pady=8)

        # 倒數計時標籤
        self.countdown_label = tk.Label(root, text="倒數: 05:00", font=custom_font, fg="red")
        self.countdown_label.pack(pady=2)

        # 建立一個框架來放置按鈕，讓它們水平並排
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        # 重置總時間按鈕
        self.btn_reset_total = tk.Button(btn_frame, text="重置總時", font=btn_font, command=self.reset_total_time)
        self.btn_reset_total.grid(row=0, column=0, padx=10)

        # 重置倒數按鈕
        self.btn_reset_cd = tk.Button(btn_frame, text="重置倒數", font=btn_font, command=self.reset_countdown_time)
        self.btn_reset_cd.grid(row=0, column=1, padx=10)

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
        self.popup.attributes('-topmost', True) 
        self.popup.attributes('-alpha', 0.95)   
        self.popup.resizable(False, False)

        # 彈窗文字內容
        lbl = tk.Label(
            self.popup, 
            text="請擊殺鎖水怪 放輪BUFF", 
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
        """關閉彈窗並重置計時器"""
        self.popup.destroy()
        self.countdown_seconds = 300 
        self.countdown_label.config(text=f"倒數: {self.format_countdown_time(self.countdown_seconds)}")
        self.is_popup_open = False

    def reset_total_time(self):
        """手動重置總時間"""
        self.total_seconds = 0
        self.total_label.config(text=f"總時間: {self.format_total_time(self.total_seconds)}")

    def reset_countdown_time(self):
        """手動重置倒數時間"""
        if self.is_popup_open:
            # 如果提醒視窗正開著，直接當作點擊了確認來關閉並重置
            self.close_popup()
        else:
            # 否則單純重置倒數時間
            self.countdown_seconds = 300
            self.countdown_label.config(text=f"倒數: {self.format_countdown_time(self.countdown_seconds)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GameTimerApp(root)
    root.mainloop()
