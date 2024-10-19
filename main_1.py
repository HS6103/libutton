from drag_detection import DragDetection
from model import CodePredictor
import time

def main():
    predictor = CodePredictor()
    drag_detector = DragDetection()


    while True:
        time.sleep(0.1)

        # 抓剪貼簿的內容
        content = drag_detector.get_clipboard_content()

        if content:
            predicted_action = predictor.predict_action(content)
            print(f'Suggested action: {predicted_action}')
            drag_detector.clipboard_content = None
        
        # 按下右鍵中斷迴圈
        if not drag_detector.listener.running:
            break

if __name__ == "__main__":
    main()
