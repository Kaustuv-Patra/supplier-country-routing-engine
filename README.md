# Supplier Country Classification & Routing Engine

AI-powered backend system that processes invoice PDFs, predicts the supplier country using a fine-tuned BERT model, and applies deterministic logistics routing rules.

The system exposes a REST API, provides an analytics dashboard, and logs all routing decisions for auditability and traceability.

---

## Problem Statement

In logistics and supply-chain systems, supplier country identification from invoices is often:

- Manual
- Error-prone
- Slow

This leads to downstream issues in:

- Transport planning
- Customs handling
- Cost estimation
- Delivery timelines

This project demonstrates how OCR and NLP can automate supplier country classification and drive **transparent, explainable routing decisions** using deterministic business rules.

---

### Architecture Overview

text
Invoice PDF
→ OCR (Tesseract)
→ Text Normalization
→ BERT-based Country Classification
→ Confidence Scoring
→ Deterministic Logistics Routing
→ Logged Decision Output
→ REST API (FastAPI)
→ Analytics Dashboard (React)

###Key Features
- Machine Learning & Backend Capabilities
- Multiclass supplier country classification covering 22 countries
- Fine-tuned DistilBERT model trained on invoice text
- Confidence scores derived from softmax probabilities
- Clear separation between inference and routing logic
- Deterministic routing rules implemented as business logic
- Persistent and auditable decision logging using JSONL
- REST API for document upload and inference
- Reproducible Python environment with pinned dependencies

###Frontend & Analytics Capabilities
- React-based analytics dashboard
- Visualization of routing decisions and model outputs
- Analytical views include:
- Supplier country distribution
- Region / continent distribution
- Transport mode distribution
- Confidence score distribution
- Routing code breakdown
- Confidence band split
- Cross-filtering across all charts
- Compound filters (routing code → region + transport)
- Visual filter indicators with individual removal
- Real-time filtering without additional backend calls

###Tech Stack
Backend
- Python 3.9 – stable and widely supported
- Tesseract OCR – text extraction from invoice PDFs
- Hugging Face Transformers (DistilBERT) – NLP model
- PyTorch – model training and inference
- FastAPI – REST API framework
- Uvicorn – ASGI server

###Frontend
- React – UI framework
- Vite – frontend build tooling
- Apache ECharts – interactive visualizations
- JavaScript (ES6) – frontend logic

###Dashboard Purpose
- The dashboard is designed to:
- Inspect model behavior through confidence distributions
- Analyze routing outcomes across regions and transport modes
- Enable interactive cross-filtering for exploratory analysis
- Maintain strict separation from backend logic

---
