import keyboard
import pyperclip
import time
import pyautogui as pya
from pynput import mouse
from model import action_prediction

dragging = False
has_moved = False
last_action = None
selected_code_snippet = ""
clipboard = ""

def get_user_behavior():
    global last_action, clipboard

    keyboard.hook(on_key_event)

    # 開始捕捉滑鼠事件
    listener = mouse.Listener(on_move=on_move, on_click=on_click)
    listener.start()

    # 當檢測到行為時，返回選取的程式碼片段和行為
    while True:
        suggested_action = action_prediction(selected_code_snippet, last_action, clipboard)
        #print(selected_code_snippet)
        #print(last_action)
        print("Suggested action: ", suggested_action)
    
        time.sleep(1)

def store_selected_code():
    global last_action, clipboard, selected_code_snippet

    if last_action == 'copy':
        clipboard = pyperclip.paste()

    pya.hotkey('ctrl', 'c')  # 執行複製操作（不影響剪貼簿的原本內容）
    time.sleep(0.1)  # 等待複製完成

    selected_code_snippet = pyperclip.paste()
    pyperclip.copy(clipboard)
    time.sleep(0.1)

    if selected_code_snippet:
        last_action = 'select'
    else:
        last_action = 'select_blank'

def on_move(x, y):
    global has_moved
    if dragging:
        has_moved = True

def on_click(x, y, button, pressed):
    global dragging, has_moved, last_action, selected_code_snippet
    if button == mouse.Button.left:
        if pressed:
            dragging = True
            has_moved = False
        else:
            if dragging and has_moved:
                store_selected_code()
            dragging = False
            has_moved = False
 
def set_last_action(action):
    global last_action, clipboard
    last_action = action

    if(action == 'paste'):
        clipboard = ''

def on_key_event(event):
    keyboard.add_hotkey('backspace', lambda: set_last_action('delete'))
    keyboard.add_hotkey('ctrl+c', lambda: set_last_action('copy'))
    keyboard.add_hotkey('ctrl+v', lambda: set_last_action('paste'))
    keyboard.add_hotkey('ctrl+s', lambda: set_last_action('save'))


get_user_behavior()
