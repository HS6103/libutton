import keyboard
import pyperclip
import time
import pyautogui as pya
from pynput import mouse
from model import action_prediction
import tkinter as tk

last_action = None
dragging = False
has_moved = False
ctrl_pressed = False
idle = True
selected_code_snippet = ""
clipboard = ""
mouse_x=0
mouse_y=0

# 初始化Tkinter主視窗
root = tk.Tk()
root.title("Suggested Action")
root.geometry("300x100")
root.overrideredirect(True)  # 去掉邊框
root.attributes('-topmost', True)  # 視窗永遠保持在最上層


# 創建一個標籤來顯示Suggested Action
label = tk.Label(root, text="Waiting for action...", font=("Arial", 12))
label.pack(pady=20)

def update_window_position(x, y):
    offset_x = 20  # X軸偏移，讓視窗不直接覆蓋在滑鼠上
    offset_y = 20  # Y軸偏移
    root.geometry(f"+{x + offset_x}+{y + offset_y}")
    
def get_user_behavior():
    global last_action, clipboard

    # 開始捕捉滑鼠事件
    listener = mouse.Listener(on_move=on_move, on_click=on_click)
    listener.start()

    # 當檢測到行為時，返回選取的程式碼片段和行為
    while True:
        suggested_action = action_prediction(selected_code_snippet, last_action, clipboard)
        
        # 更新Tkinter標籤的文字內容
        label.config(text=f"Suggested action: {suggested_action}")
        update_window_position(mouse_x, mouse_y)  # 每次滑鼠移動時更新視窗位置
        # 讓Tkinter主視窗更新
        root.update()
        
        time.sleep(1)
        clipboard = ""

def store_selected_code():
    global last_action, clipboard
    pya.hotkey('ctrl', 'c')  # 執行複製操作（不影響剪貼簿的原本內容）
    time.sleep(0.1)  # 等待複製完成

    selected_content = pyperclip.paste()

    if last_action == 'copy':
        clipboard = selected_content

    pyperclip.copy(clipboard) 

    # 檢查內容是否為空白字符
    if selected_content.strip() == "":
        return None
    
    return selected_content

def on_move(x, y):
    global has_moved, mouse_x, mouse_y
    if dragging:
        has_moved = True
    mouse_x = x
    mouse_y = y

def on_click(x, y, button, pressed):
    global dragging, has_moved, last_action, selected_code_snippet
    if button == mouse.Button.left:
        if pressed:
            dragging = True
            has_moved = False
        else:
            if dragging and has_moved:
                selected_content = store_selected_code()  # 儲存選取內容到變數
                if selected_content:
                    selected_code_snippet = selected_content  # 更新選取的程式碼
                    last_action = 'select'
                else:
                    last_action = 'select_blank'  # 選取的是空白行
            dragging = False
            has_moved = False
 
def on_key_event(event):
    global last_action, ctrl_pressed, clipboard
    if event.name == 'backspace':
        last_action = 'delete'
    elif event.name == 'ctrl':
        if event.event_type == 'down':
            ctrl_pressed = True
        else:
            ctrl_pressed = False
    elif event.name == 'c' and ctrl_pressed:
        last_action = 'copy'
    elif event.name == 'v' and ctrl_pressed:
        last_action = 'paste'
    elif event.name == 's' and ctrl_pressed:
        last_action = 'save'
    else:
        last_action = 'other'

keyboard.hook(on_key_event)

get_user_behavior()

