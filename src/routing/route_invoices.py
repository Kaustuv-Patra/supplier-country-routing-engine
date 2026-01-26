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
LABEL_MAPPING_FILE = Path("data/training/label_mapping.json")
OCR_TEXT_DIR = Path("data/ocr_text_normalized")

OUTPUT_DIR = Path("outputs")
OUTPUT_FILE = OUTPUT_DIR / "routing_decisions.jsonl"

MAX_LENGTH = 512

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =========================
# Routing Rules (Locked)
# =========================

REGION_MAP = {
    "India": "APAC",
    "China": "APAC",
    "Vietnam": "APAC",
    "Thailand": "APAC",
    "Indonesia": "APAC",
    "Japan": "APAC",
    "South Korea": "APAC",
    "Australia": "APAC",

    "Germany": "EMEA",
    "France": "EMEA",
    "United Kingdom": "EMEA",
    "Italy": "EMEA",
    "Spain": "EMEA",
    "Netherlands": "EMEA",
    "Poland": "EMEA",
    "Czech Republic": "EMEA",
    "Saudi Arabia": "EMEA",
    "United Arab Emirates": "EMEA",

    "United States": "AMER",
    "Canada": "AMER",
    "Mexico": "AMER",
    "Brazil": "AMER"
}

TRANSPORT_MAP = {
    "APAC": {
        "primary": "SEA",
        "secondary": "AIR"
    },
    "EMEA": {
        "primary": "ROAD_RAIL",
        "secondary": "SEA"
    },
    "AMER": {
        "primary": "ROAD",
        "secondary": "RAIL"
    }
}

# =========================
# Inference + Routing
# =========================

def main():
    # Load label mapping
    with open(LABEL_MAPPING_FILE, "r", encoding="utf-8") as f:
        label_to_id = json.load(f)

    id_to_label = {v: k for k, v in label_to_id.items()}

    # Load model and tokenizer
    tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_DIR)
    model = DistilBertForSequenceClassification.from_pretrained(MODEL_DIR)
    model.eval()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
        for text_file in OCR_TEXT_DIR.glob("*.txt"):
            with open(text_file, "r", encoding="utf-8") as f:
                text = f.read().strip()

            encoding = tokenizer(
                text,
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

            predicted_country = id_to_label[pred_id.item()]
            conf_value = round(confidence.item(), 4)

            region = REGION_MAP.get(predicted_country, "UNKNOWN")
            transport = TRANSPORT_MAP.get(region, {})

            decision = {
                "invoice_id": text_file.stem,
                "predicted_country": predicted_country,
                "confidence": conf_value,
                "region": region,
                "primary_transport": transport.get("primary"),
                "secondary_transport": transport.get("secondary"),
                "routing_code": f"{region}-{transport.get('primary')}"
            }

            out_f.write(json.dumps(decision) + "\n")

    print(f"Routing decisions written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()