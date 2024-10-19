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

def action_prediction(code_snippet, user_behavior, clipboard_content):

    if code_snippet == '':
        return 'save'

    # 如果剪貼簿有內容，將預測行為設為 paste
    if clipboard_content and user_behavior == 'select_blank':
        return 'paste'
    
    if user_behavior == 'delete':
        return 'undo'
    
    # 將代碼片段和用戶行為拼接為一個輸入
    input_text = f"{code_snippet} {user_behavior}"
    
    # 將文本轉換為模型可以接受的格式
    inputs = tokenizer(input_text, return_tensors='pt')

    # 進行預測
    with torch.no_grad():
        outputs = model(**inputs)
    
    # 獲取預測的標籤
    predicted_class = outputs.logits.argmax().item()
    
    # 返回對應的行為
    return label_map[predicted_class]