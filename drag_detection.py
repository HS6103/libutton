from pynput import mouse
import pyautogui as pya
import pyperclip
import time

class DragDetection:
    def __init__(self):
        self.dragging = False
        self.has_moved = False
        self.listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)
        self.listener.start()
        self.copy_clipboard_content = None

    def copy_clipboard(self):
        pya.hotkey('ctrl', 'c')
        time.sleep(0.1)  # Allow time for the copy action to complete
        return pyperclip.paste()

    def on_move(self, x, y):
        if self.dragging:
            self.has_moved = True  # Mouse has moved during drag

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left:
            if pressed:
                # Start of the drag
                self.dragging = True
                self.has_moved = False  # Reset movement flag
                ##print(f'Started dragging at {(x, y)}')
            else:
                # End of the drag
                if self.dragging and self.has_moved:
                    ##print(f'Released at {(x, y)}')
                    content = self.copy_clipboard()
                    self.copy_clipboard_content = content
                    return content
                # Reset dragging state
                self.dragging = False
                self.has_moved = False
        elif button == mouse.Button.right:  # 使用右鍵停止程序
            print("Exit")
            self.listener.stop()  # 停止監聽

    def on_scroll(self, x, y, dx, dy):
        print(f'Scrolled {"down" if dy < 0 else "up"} at {(x, y)}')

    def join(self):
        self.listener.join()

    def get_clipboard_content(self):
        return self.copy_clipboard_content
