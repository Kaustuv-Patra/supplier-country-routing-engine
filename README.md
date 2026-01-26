# Supplier Country Classification & Routing Engine

AI-powered backend system that processes invoice PDFs, predicts the supplier country using a fine-tuned BERT model, and applies deterministic logistics routing rules. The system exposes a REST API and logs all routing decisions for auditability.

---

## Problem Statement

In logistics and supply-chain systems, supplier country identification from invoices is often manual, error-prone, and slow. This project demonstrates how OCR and NLP can automate supplier country classification and drive downstream routing decisions in a transparent and explainable way.

---

## Architecture Overview

Invoice PDF  
→ OCR (Tesseract)  
→ Text Normalization  
→ BERT-based Country Classification  
→ Confidence Scoring  
→ Deterministic Logistics Routing  
→ Logged Decision Output  
→ REST API (FastAPI)

---

## Key Features

- Multiclass supplier country classification (22 countries)
- Confidence scoring using softmax probabilities
- Continent-based logistics routing (APAC / EMEA / AMER)
- Deterministic transport mode selection
- Persistent, auditable decision logging (JSONL)
- REST API for PDF upload and inference
- Fully reproducible Python environment

---

## Tech Stack

- **Python 3.9**
- **Tesseract OCR**
- **Hugging Face Transformers (DistilBERT)**
- **PyTorch**
- **FastAPI**
- **Uvicorn**

---

## Routing Logic (Business Rules)

Routing is intentionally **non-ML** and fully explainable.

| Region | Countries | Primary Transport | Secondary Transport |
|------|---------|------------------|--------------------|
| APAC | India, China, Vietnam, Japan, Australia, etc. | Sea | Air |
| EMEA | Germany, France, UK, UAE, Saudi Arabia, etc. | Road / Rail | Sea |
| AMER | USA, Canada, Mexico, Brazil | Road | Rail |

ML is used **only** to predict the country.

---

## API Usage

### Start the Server

```bash
uvicorn src.api.app:app --host 0.0.0.0 --port 8000
