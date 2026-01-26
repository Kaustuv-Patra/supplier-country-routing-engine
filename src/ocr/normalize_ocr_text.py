from pathlib import Path
import re

# =========================
# Configuration
# =========================

OCR_INPUT_DIR = Path("data/ocr_text")
NORMALIZED_OUTPUT_DIR = Path("data/ocr_text_normalized")

NORMALIZED_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Characters commonly introduced by OCR noise
NOISE_CHARS_PATTERN = re.compile(r"[■•●◦▪︎]")

# Multiple whitespace/newlines normalization
MULTISPACE_PATTERN = re.compile(r"[ \t]+")
MULTINEWLINE_PATTERN = re.compile(r"\n{3,}")

# Lines that are purely decorative or empty after cleanup
EMPTY_LINE_PATTERN = re.compile(r"^\s*$")


# =========================
# Normalization Logic
# =========================

def normalize_text(raw_text: str) -> str:
    """
    Normalize OCR text while preserving country-discriminative signals.
    """
    # 1. Remove common OCR noise characters
    text = NOISE_CHARS_PATTERN.sub(" ", raw_text)

    # 2. Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # 3. Lowercase (non-destructive for non-Latin scripts)
    text = text.lower()

    # 4. Normalize whitespace inside lines
    lines = []
    for line in text.split("\n"):
        line = MULTISPACE_PATTERN.sub(" ", line).strip()
        if not EMPTY_LINE_PATTERN.match(line):
            lines.append(line)

    # 5. Rejoin lines and collapse excessive newlines
    normalized = "\n".join(lines)
    normalized = MULTINEWLINE_PATTERN.sub("\n\n", normalized)

    return normalized.strip()


def main():
    input_files = list(OCR_INPUT_DIR.glob("*.txt"))

    for input_file in input_files:
        with open(input_file, "r", encoding="utf-8") as f:
            raw_text = f.read()

        normalized_text = normalize_text(raw_text)

        output_file = NORMALIZED_OUTPUT_DIR / input_file.name
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(normalized_text)


if __name__ == "__main__":
    main()