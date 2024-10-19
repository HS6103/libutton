import tkinter as tk
import time

class SuggestionsWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Suggested Action")
        self.root.geometry("150x100")
        self.root.overrideredirect(True)  # 去掉邊框
        self.root.attributes('-topmost', True)  # 視窗永遠保持在最上層
        self.root.withdraw() # 先隱藏
        self.root.config(bg='black')
        self.root.attributes('-transparentcolor', 'black')  # 設置透明背景
        # 創建一個標籤來顯示Suggested Action
        self.label = tk.Label(self.root, text="Waiting for action...", font=("Arial", 8))
        self.label.pack(pady=20)

    def update_label(self, input_text):
        self.label.config(text=f"{input_text}")
        self.root.update()

    def update_window_position(self, x, y):
        offset_x = 8
        offset_y = 2
        self.root.geometry(f"+{x + offset_x}+{y + offset_y}")
        self.root.update()
    
    def show(self):
        self.root.deiconify()
    
    def hide(self):
        self.root.withdraw()
    
    def kill(self):
        self.root.destroy()


if __name__ == "__main__":
    window = SuggestionsWindow()
    window.update_label("Suggested action: None")
    window.update_window_position(1, 1)
    time.sleep(3)
    window.kill()