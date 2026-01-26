import json
from pathlib import Path

# =========================
# Configuration
# =========================

NORMALIZED_TEXT_DIR = Path("data/ocr_text_normalized")
SOURCE_JSON_DIR = Path("data/synthetic_sources")
OUTPUT_DIR = Path("data/training")
OUTPUT_FILE = OUTPUT_DIR / "country_classification_dataset.jsonl"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =========================
# Dataset Builder
# =========================

def load_ground_truth():
    """
    Load ground-truth supplier_country labels from synthetic source JSON files.
    Returns a dict: {invoice_stem: country}
    """
    mapping = {}

    for json_file in SOURCE_JSON_DIR.glob("*.json"):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        stem = json_file.stem
        country = data["ground_truth"]["supplier_country"]
        mapping[stem] = country

    return mapping


def main():
    ground_truth_map = load_ground_truth()
    records_written = 0

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
        for text_file in NORMALIZED_TEXT_DIR.glob("*.txt"):
            stem = text_file.stem

            if stem not in ground_truth_map:
                # Skip if ground truth is missing
                continue

            with open(text_file, "r", encoding="utf-8") as f:
                text = f.read().strip()

            if not text:
                # Skip empty OCR outputs
                continue

            record = {
                "text": text,
                "label": ground_truth_map[stem]
            }

            out_f.write(json.dumps(record, ensure_ascii=False) + "\n")
            records_written += 1

    print(f"Dataset created with {records_written} records at {OUTPUT_FILE}")


if __name__ == "__main__":
    main()