import json
import random
from pathlib import Path
from collections import defaultdict

# =========================
# Configuration
# =========================

RANDOM_SEED = 42
TRAIN_RATIO = 0.8

INPUT_DATASET = Path("data/training/country_classification_dataset.jsonl")
OUTPUT_DIR = Path("data/training")

LABEL_MAPPING_FILE = OUTPUT_DIR / "label_mapping.json"
TRAIN_FILE = OUTPUT_DIR / "train.jsonl"
VAL_FILE = OUTPUT_DIR / "val.jsonl"

# =========================
# Helpers
# =========================

def load_dataset(path: Path):
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


def build_label_mapping(records):
    labels = sorted({r["label"] for r in records})
    return {label: idx for idx, label in enumerate(labels)}


def stratified_split(records, label_to_id):
    buckets = defaultdict(list)
    for r in records:
        buckets[r["label"]].append(r)

    train_records = []
    val_records = []

    random.seed(RANDOM_SEED)

    for label, items in buckets.items():
        random.shuffle(items)
        split_idx = max(1, int(len(items) * TRAIN_RATIO))

        train_records.extend(items[:split_idx])
        val_records.extend(items[split_idx:])

    random.shuffle(train_records)
    random.shuffle(val_records)

    return train_records, val_records


def write_jsonl(path: Path, records, label_to_id):
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            out = {
                "text": r["text"],
                "label": label_to_id[r["label"]]
            }
            f.write(json.dumps(out, ensure_ascii=False) + "\n")


# =========================
# Main
# =========================

def main():
    records = load_dataset(INPUT_DATASET)

    label_to_id = build_label_mapping(records)

    with open(LABEL_MAPPING_FILE, "w", encoding="utf-8") as f:
        json.dump(label_to_id, f, indent=2, ensure_ascii=False)

    train_records, val_records = stratified_split(records, label_to_id)

    write_jsonl(TRAIN_FILE, train_records, label_to_id)
    write_jsonl(VAL_FILE, val_records, label_to_id)

    print(f"Labels: {len(label_to_id)}")
    print(f"Train records: {len(train_records)}")
    print(f"Validation records: {len(val_records)}")


if __name__ == "__main__":
    main()