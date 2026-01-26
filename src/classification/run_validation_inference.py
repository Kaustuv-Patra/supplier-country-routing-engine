import json
from pathlib import Path
import torch
import torch.nn.functional as F

from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification
)

# =========================
# Configuration
# =========================

MODEL_DIR = Path("models/country_classifier")
VAL_FILE = Path("data/training/val.jsonl")
LABEL_MAPPING_FILE = Path("data/training/label_mapping.json")

MAX_LENGTH = 512

# =========================
# Inference
# =========================

def main():
    # Load label mapping
    with open(LABEL_MAPPING_FILE, "r", encoding="utf-8") as f:
        label_to_id = json.load(f)

    id_to_label = {v: k for k, v in label_to_id.items()}

    # Load tokenizer and model
    tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_DIR)
    model = DistilBertForSequenceClassification.from_pretrained(MODEL_DIR)
    model.eval()

    results = []

    with open(VAL_FILE, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)

            encoding = tokenizer(
                record["text"],
                truncation=True,
                padding="max_length",
                max_length=MAX_LENGTH,
                return_tensors="pt"
            )

            with torch.no_grad():
                outputs = model(
                    input_ids=encoding["input_ids"],
                    attention_mask=encoding["attention_mask"]
                )

            logits = outputs.logits
            probs = F.softmax(logits, dim=-1)

            confidence, pred_id = torch.max(probs, dim=-1)

            result = {
                "predicted_country": id_to_label[pred_id.item()],
                "confidence": round(confidence.item(), 4)
            }

            results.append(result)

    # Print a small sample
    print("Sample predictions (validation):")
    for r in results[:5]:
        print(r)

    avg_conf = sum(r["confidence"] for r in results) / len(results)
    print(f"\nAverage confidence on validation set: {avg_conf:.4f}")


if __name__ == "__main__":
    main()