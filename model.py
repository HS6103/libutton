from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch

class CodePredictor:
    def __init__(self):
        # 加載預訓練的 CodeBERT 模型和 Tokenizer
        self.tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
        self.model = RobertaForSequenceClassification.from_pretrained("microsoft/codebert-base", num_labels=6)

    def predict_action(self, code_snippet):
        # 將程式碼片段編碼
        inputs = self.tokenizer(code_snippet, return_tensors="pt", padding=True, truncation=True)

        # 模型預測
        with torch.no_grad():
            outputs = self.model(**inputs)

        # 獲取預測的類別
        predictions = torch.argmax(outputs.logits, dim=-1)
        actions = ['copy', 'paste', 'comment', 'delete', 'undo', 'compile']
        return actions[predictions.item()]
