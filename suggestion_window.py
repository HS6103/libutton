import tkinter as tk
import time

class SuggestionsWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Suggested Action")
        self.root.geometry("300x100")
        self.root.overrideredirect(True)  # 去掉邊框
        self.root.attributes('-topmost', True)  # 視窗永遠保持在最上層
        # 創建一個標籤來顯示Suggested Action
        self.label = tk.Label(self.root, text="Waiting for action...", font=("Arial", 12))
        self.label.pack(pady=20)

    def update_label(self, input_text):
        self.label.config(text=f"{input_text}")
        self.root.update()

    def update_window_position(self, x, y):
        offset_x = 20
        offset_y = 20
        self.root.geometry(f"+{x + offset_x}+{y + offset_y}")
        self.root.update()
    
    def kill(self):
        self.root.destroy()
        