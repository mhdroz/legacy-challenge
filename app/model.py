import torch, torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class RiskModel:
    def __init__(self, model_dir: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_dir)
        self.model.eval()

    def score(self, text: str, max_len: int = 512):
        tokens = self.tokenizer(text, truncation=True, padding="max_length",
                                max_length=max_len, return_tensors="pt")
        
        with torch.no_grad():
            logits = self.model(**tokens).logits
            probs = F.softmax(logits, dim=1).squeeze()
            id_ = torch.argmax(probs).item()
            conf = probs[id_].item()

        return id_, conf, probs.tolist()