import json
import uuid
from pathlib import Path

import torch
import torch.nn.functional as F
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

import pytesseract
from pdf2image import convert_from_bytes

from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification
)

from src.routing.api import router as routing_router

# =========================
# App Initialization (ONLY ONCE)
# =========================

app = FastAPI(title="Supplier Country Classification & Routing Engine")
app.include_router(routing_router)

# =========================
# App & Paths
# =========================

MODEL_DIR = Path("models/country_classifier")
LABEL_MAPPING_FILE = Path("data/training/label_mapping.json")
DECISION_LOG = Path("outputs/routing_decisions.jsonl")
DECISION_LOG.parent.mkdir(parents=True, exist_ok=True)

MAX_LENGTH = 512

# =========================
# Routing Rules (Locked)
# =========================

REGION_MAP = {
    "India": "APAC", "China": "APAC", "Vietnam": "APAC", "Thailand": "APAC",
    "Indonesia": "APAC", "Japan": "APAC", "South Korea": "APAC", "Australia": "APAC",

    "Germany": "EMEA", "France": "EMEA", "United Kingdom": "EMEA", "Italy": "EMEA",
    "Spain": "EMEA", "Netherlands": "EMEA", "Poland": "EMEA", "Czech Republic": "EMEA",
    "Saudi Arabia": "EMEA", "United Arab Emirates": "EMEA",

    "United States": "AMER", "Canada": "AMER", "Mexico": "AMER", "Brazil": "AMER"
}

TRANSPORT_MAP = {
    "APAC": {"primary": "SEA", "secondary": "AIR"},
    "EMEA": {"primary": "ROAD_RAIL", "secondary": "SEA"},
    "AMER": {"primary": "ROAD", "secondary": "RAIL"}
}

# =========================
# Load Model (Once)
# =========================

with open(LABEL_MAPPING_FILE, "r", encoding="utf-8") as f:
    label_to_id = json.load(f)

id_to_label = {v: k for k, v in label_to_id.items()}

tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_DIR)
model = DistilBertForSequenceClassification.from_pretrained(MODEL_DIR)
model.eval()

# =========================
# Helpers
# =========================

def ocr_pdf_bytes(pdf_bytes: bytes) -> str:
    images = convert_from_bytes(pdf_bytes, dpi=300)
    text = []
    for img in images:
        text.append(pytesseract.image_to_string(img, lang="eng"))
    return "\n".join(text).lower()


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def route_country(country: str):
    region = REGION_MAP.get(country, "UNKNOWN")
    transport = TRANSPORT_MAP.get(region, {})
    return region, transport.get("primary"), transport.get("secondary")


# =========================
# API Endpoint
# =========================

@app.post("/route-invoice")
async def route_invoice(file: UploadFile = File(...)):
    invoice_id = file.filename or str(uuid.uuid4())

    pdf_bytes = await file.read()
    raw_text = ocr_pdf_bytes(pdf_bytes)
    normalized_text = normalize_text(raw_text)

    encoding = tokenizer(
        normalized_text,
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

    probs = F.softmax(outputs.logits, dim=-1)
    confidence, pred_id = torch.max(probs, dim=-1)

    predicted_country = id_to_label[pred_id.item()]
    conf_value = round(confidence.item(), 4)

    region, primary, secondary = route_country(predicted_country)

    decision = {
        "invoice_id": invoice_id,
        "supplier_country": predicted_country,
        "confidence": conf_value,
        "continent": region,
        "primary_transport": primary,
        "secondary_transport": secondary,
        "routing_code": f"{region}-{primary}"
    }

    with open(DECISION_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(decision) + "\n")

    return JSONResponse(content=decision)