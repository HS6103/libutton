import keyboard
import pyperclip
import time
import pyautogui as pya
from pynput import mouse
from model import action_prediction
from suggestion_window import SuggestionsWindow

dragging = False
has_moved = False
last_action = None
selected_code_snippet = ""
clipboard = ""
activation = False
code_selected = False  # New flag to track if code has been selected
mouse_x = 0
mouse_y = 0
last_move_time = time.time()
suggested_action = "None"
start_time = time.time()


def get_user_behavior():
    global last_action, clipboard, activation, code_selected, suggested_action

    keyboard.hook(on_key_event)

    # Start mouse listener
    listener = mouse.Listener(on_move=on_move, on_click=on_click)
    listener.start()

    # 初始化Tkinter視窗
    window = SuggestionsWindow()
    window.update_window_position(mouse_x, mouse_y)
    window.update_label("")

    # Loop to suggest actions
    while True:
        if code_selected or last_action:
            suggested_action = action_prediction(selected_code_snippet, last_action, clipboard)
            #print("Suggested action: ", suggested_action)
            time.sleep(0.1)

        if ((time.time() - last_move_time) > 0.2) & ((time.time() - start_time) > 0.5) & (suggested_action != "None"):            
            # 更新Tkinter標籤的文字內容
            window.update_label(suggested_action)
            window.update_window_position(mouse_x, mouse_y)  # 每次滑鼠移動時更新視窗位置
            window.show()
        else:
            window.hide()
            
        if activation:
            activate(suggested_action)
            print(f"Activated {suggested_action}")
            last_action = suggested_action
            code_selected = False  # Reset after activation
            activation = False  # Reset activation
            code_selected = False  # Reset after act
            time.sleep(0.1)
            

        # Reset values
        last_action = ""
        clipboard = pyperclip.paste()
        code_selected = False
        time.sleep(0.2)

def activate(suggested_action):
    # Activate the suggested action
    if suggested_action == "save":
        pya.hotkey('ctrl','s')
    elif suggested_action == "undo":
        pya.hotkey('ctrl','z')
    elif suggested_action == "copy":
        pya.hotkey('ctrl','c')
    elif suggested_action == "paste":
        pya.hotkey('ctrl','v')
    return True

def store_selected_code():
    global last_action, clipboard, selected_code_snippet, code_selected

    if last_action == 'copy':
        clipboard = pyperclip.paste()

    pya.hotkey('ctrl', 'c')  # Perform copy operation
    time.sleep(0.1)  # Wait for the copy to complete

    selected_code_snippet = pyperclip.paste()
    pyperclip.copy(clipboard)  # Restore original clipboard content
    time.sleep(0.1)

    if selected_code_snippet:
        last_action = 'select'
        code_selected = True  # Set flag indicating code has been selected
    else:
        last_action = 'select_blank'

def on_move(x, y):
    global has_moved, mouse_x, mouse_y, last_move_time
    if dragging:
        has_moved = True
    mouse_x = x
    mouse_y = y
    last_move_time = time.time()

def on_click(x, y, button, pressed):
    global dragging, has_moved,activation
    if button == mouse.Button.left:
        if pressed:
            dragging = True
            has_moved = False
        else:
            if dragging and has_moved:
                store_selected_code()
            dragging = False
            has_moved = False

    if button == mouse.Button.x2:
        if pressed:
            activation = True

def set_last_action(action):
    global last_action, clipboard
    last_action = action

    if action == 'copy':
        clipboard = pyperclip.paste()
        time.sleep(0.1)
    if action == 'paste':
        clipboard = ''

def on_key_event(event):
    keyboard.add_hotkey('backspace', lambda: set_last_action('delete'))
    keyboard.add_hotkey('ctrl+c', lambda: set_last_action('copy'))
    keyboard.add_hotkey('ctrl+v', lambda: set_last_action('paste'))
    keyboard.add_hotkey('ctrl+s', lambda: set_last_action('save'))
    keyboard.add_hotkey('ctrl+z', lambda: set_last_action('undo'))

get_user_behavior()