import json
import random
from pathlib import Path

import torch
from torch.utils.data import Dataset

from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments,
    set_seed
)

# =========================
# Configuration
# =========================

RANDOM_SEED = 42
MODEL_NAME = "distilbert-base-uncased"
NUM_EPOCHS = 5
TRAIN_BATCH_SIZE = 8
EVAL_BATCH_SIZE = 8
LEARNING_RATE = 5e-5
MAX_LENGTH = 512

TRAIN_FILE = Path("data/training/train.jsonl")
VAL_FILE = Path("data/training/val.jsonl")
LABEL_MAPPING_FILE = Path("data/training/label_mapping.json")

OUTPUT_DIR = Path("models/country_classifier")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =========================
# Dataset
# =========================

class CountryDataset(Dataset):
    def __init__(self, jsonl_file, tokenizer, max_length):
        self.records = []
        self.tokenizer = tokenizer
        self.max_length = max_length

        with open(jsonl_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                self.records.append(json.loads(line))

    def __len__(self):
        return len(self.records)

    def __getitem__(self, idx):
        record = self.records[idx]

        encoding = self.tokenizer(
            record["text"],
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt"
        )

        item = {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "labels": torch.tensor(record["label"], dtype=torch.long)
        }

        return item

# =========================
# Training
# =========================

def main():
    set_seed(RANDOM_SEED)

    with open(LABEL_MAPPING_FILE, "r", encoding="utf-8") as f:
        label_mapping = json.load(f)

    num_labels = len(label_mapping)

    tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_NAME)

    train_dataset = CountryDataset(TRAIN_FILE, tokenizer, MAX_LENGTH)
    val_dataset = CountryDataset(VAL_FILE, tokenizer, MAX_LENGTH)

    model = DistilBertForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=num_labels
    )

    training_args = TrainingArguments(
        output_dir=str(OUTPUT_DIR),
        evaluation_strategy="epoch",
        save_strategy="epoch",
        learning_rate=LEARNING_RATE,
        per_device_train_batch_size=TRAIN_BATCH_SIZE,
        per_device_eval_batch_size=EVAL_BATCH_SIZE,
        num_train_epochs=NUM_EPOCHS,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        logging_dir=str(OUTPUT_DIR / "logs"),
        seed=RANDOM_SEED,
        save_total_limit=2,
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        tokenizer=tokenizer
    )

    trainer.train()

    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)

    print("Training complete. Model saved to:", OUTPUT_DIR)


if __name__ == "__main__":
    main()