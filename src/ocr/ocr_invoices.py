import pytesseract
from pathlib import Path
from pdf2image import convert_from_path

# =========================
# Configuration
# =========================

PDF_INPUT_DIR = Path("data/raw_pdfs")
TEXT_OUTPUT_DIR = Path("data/ocr_text")

TEXT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# If Tesseract is not on PATH, uncomment and set explicitly:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# =========================
# OCR Logic
# =========================

def ocr_pdf(pdf_path: Path) -> str:
    images = convert_from_path(pdf_path, dpi=300)
    extracted_text = []

    for page_number, image in enumerate(images, start=1):
        text = pytesseract.image_to_string(image, lang="eng")
        extracted_text.append(f"\n--- PAGE {page_number} ---\n{text}")

    return "\n".join(extracted_text)


def main():
    pdf_files = list(PDF_INPUT_DIR.glob("*.pdf"))

    for pdf_file in pdf_files:
        text = ocr_pdf(pdf_file)
        output_file = TEXT_OUTPUT_DIR / f"{pdf_file.stem}.txt"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)


if __name__ == "__main__":
    main()