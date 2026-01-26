import json
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

INPUT_DIR = Path("data/synthetic_sources")
OUTPUT_DIR = Path("data/raw_pdfs")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PAGE_WIDTH, PAGE_HEIGHT = A4


def draw_multiline_text(c, text, x, y, line_height=14):
    for line in text.split("\n"):
        c.drawString(x, y, line)
        y -= line_height
    return y


def render_invoice(json_path: Path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    pdf_name = json_path.stem + ".pdf"
    pdf_path = OUTPUT_DIR / pdf_name

    c = canvas.Canvas(str(pdf_path), pagesize=A4)

    y = PAGE_HEIGHT - 40

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y, "INVOICE")
    y -= 30

    c.setFont("Helvetica", 10)
    meta = data["invoice_metadata"]
    c.drawString(40, y, f"Invoice Number: {meta['invoice_number']}")
    y -= 15
    c.drawString(40, y, f"Invoice Date: {meta['invoice_date']}")
    y -= 15
    c.drawString(40, y, f"Due Date: {meta['due_date']}")
    y -= 25

    # Supplier
    supplier = data["supplier"]
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Supplier")
    y -= 15

    c.setFont("Helvetica", 10)
    supplier_text = (
        f"{supplier['legal_name']}\n"
        f"{supplier['address']['line_1']}\n"
        f"{supplier['address']['city']}\n"
        f"{supplier['country']}\n"
        f"Tax ID ({supplier['tax_id']['type']}): {supplier['tax_id']['value']}\n"
        f"Phone: {supplier['phone']}\n"
        f"Email: {supplier['email']}"
    )
    y = draw_multiline_text(c, supplier_text, 40, y)
    y -= 20

    # Buyer
    buyer = data["buyer"]
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Bill To")
    y -= 15

    c.setFont("Helvetica", 10)
    buyer_text = (
        f"{buyer['name']}\n"
        f"{buyer['address']['city']}\n"
        f"{buyer['country']}"
    )
    y = draw_multiline_text(c, buyer_text, 40, y)
    y -= 25

    # Financials
    financials = data["financials"]
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Financial Summary")
    y -= 15

    c.setFont("Helvetica", 10)
    fin_text = (
        f"Subtotal: {financials['currency_symbol']} {financials['subtotal']}\n"
        f"Tax ({int(financials['tax_rate'] * 100)}%): {financials['currency_symbol']} {financials['tax_amount']}\n"
        f"Total: {financials['currency_symbol']} {financials['total_amount']}\n"
        f"Payment Terms: {financials['payment_terms']}"
    )
    y = draw_multiline_text(c, fin_text, 40, y)
    y -= 25

    # Line items
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Description")
    y -= 15

    c.setFont("Helvetica", 10)
    y = draw_multiline_text(c, data["text_blocks"]["line_items_text"], 40, y)
    y -= 40

    # Footer
    c.setFont("Helvetica", 9)
    footer = data["text_blocks"]["legal_footer_text"]
    c.drawString(40, 40, footer)

    c.showPage()
    c.save()


def main():
    for json_file in INPUT_DIR.glob("*.json"):
        render_invoice(json_file)


if __name__ == "__main__":
    main()