from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch

# 初始化模型和分詞器
tokenizer = RobertaTokenizer.from_pretrained('microsoft/codebert-base')
model = RobertaForSequenceClassification.from_pretrained('microsoft/codebert-base', num_labels=6)

# 模型輸出標籤對應的行為
label_map = {
    0: 'save',
    1: 'paste',
    2: 'copy',
    3: 'undo',
    4: 'delete',
    5: 'comment'
}

previous_clipboard = ""

def action_prediction(code_snippet, user_behavior, clipboard_content):
    global previous_clipboard

    if clipboard_content:
        if user_behavior == 'copy' or previous_clipboard != clipboard_content:
            previous_clipboard = clipboard_content
            return 'paste'

    if user_behavior == 'select' and code_snippet != '':
        # 將代碼片段和用戶行為拼接為一個輸入
        input_text = f"{code_snippet} {user_behavior}"
        
        # 將文本轉換為模型可以接受的格式
        inputs = tokenizer(input_text, return_tensors='pt')

        # 進行預測
        with torch.no_grad():
            outputs = model(**inputs)

        # 獲取預測的標籤
        predicted_class = outputs.logits.argmax().item()

        # 返回模型判斷的行為
        return label_map[predicted_class]
    
    if user_behavior == 'delete':
        return 'undo'

    return 'save'
