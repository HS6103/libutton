from pynput import mouse
import pyautogui as pya
import pyperclip  # handy cross-platform clipboard text handler
import time

# Flags to track dragging state and movement
dragging = False
has_moved = False

def copy_clipboard():
    pya.hotkey('ctrl', 'c')
    time.sleep(.1)  # Allow time for the copy action to complete
    return pyperclip.paste()

def on_move(x, y):
    global has_moved
    if dragging:
        has_moved = True  # Mouse has moved during drag

def on_click(x, y, button, pressed):
    global dragging, has_moved
    if button == mouse.Button.left:
        if pressed:
            # Start of the drag
            dragging = True
            has_moved = False  # Reset movement flag
            print(f'Started dragging at {(x, y)}')
        else:
            # End of the drag
            if dragging and has_moved:
                print(f'Released at {(x, y)}')
                content = copy_clipboard()
                if content:
                    pya.alert(text=content, title='Selected Text', button='OK')
            # Reset dragging state
            dragging = False
            has_moved = False

def on_scroll(x, y, dx, dy):
    print(f'Scrolled {"down" if dy < 0 else "up"} at {(x, y)}')

listener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll)
listener.start()

# This will keep the program running until the listener stops
listener.join()
