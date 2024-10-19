import tkinter as tk

# 創建主窗口
root = tk.Tk()
root.title("懸浮視窗")

# 設置窗口大小
root.geometry("300x200")

# 設置窗口為懸浮（置頂）視窗
root.wm_attributes("-topmost", 1)

# 添加一個標籤
label = tk.Label(root, text="這是懸浮視窗")
label.pack(pady=20)

# 添加按鈕以關閉窗口
button = tk.Button(root, text="關閉視窗", command=root.destroy)
button.pack(pady=20)

# 運行主循環
root.mainloop()