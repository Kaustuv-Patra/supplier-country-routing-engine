import json
import random
import uuid
from datetime import date, timedelta
from pathlib import Path

# =========================
# Configuration
# =========================

OUTPUT_DIR = Path("data/synthetic_sources")
INVOICES_PER_COUNTRY = 5
RANDOM_SEED = 42

COUNTRIES = {
    "India": {
        "code": "IN",
        "currency_code": "INR",
        "currency_symbol": "₹",
        "tax_type": "GSTIN",
        "phone_prefix": "+91",
        "legal_footer": "Subject to Indian Jurisdiction"
    },
    "China": {
        "code": "CN",
        "currency_code": "CNY",
        "currency_symbol": "¥",
        "tax_type": "Unified Social Credit Code",
        "phone_prefix": "+86",
        "legal_footer": "增值税专用发票。根据中华人民共和国法律。"
    },
    "United States": {
        "code": "US",
        "currency_code": "USD",
        "currency_symbol": "$",
        "tax_type": "EIN",
        "phone_prefix": "+1",
        "legal_footer": "This invoice is governed by U.S. law"
    },
    "Germany": {
        "code": "DE",
        "currency_code": "EUR",
        "currency_symbol": "€",
        "tax_type": "USt-IdNr",
        "phone_prefix": "+49",
        "legal_footer": "Gemäß deutschem Recht"
    },
    "France": {
        "code": "FR",
        "currency_code": "EUR",
        "currency_symbol": "€",
        "tax_type": "TVA",
        "phone_prefix": "+33",
        "legal_footer": "Conformément au droit français"
    },
    "United Kingdom": {
        "code": "GB",
        "currency_code": "GBP",
        "currency_symbol": "£",
        "tax_type": "VAT",
        "phone_prefix": "+44",
        "legal_footer": "Subject to UK law"
    },
    "Italy": {
        "code": "IT",
        "currency_code": "EUR",
        "currency_symbol": "€",
        "tax_type": "Partita IVA",
        "phone_prefix": "+39",
        "legal_footer": "Ai sensi della legge italiana"
    },
    "Spain": {
        "code": "ES",
        "currency_code": "EUR",
        "currency_symbol": "€",
        "tax_type": "CIF",
        "phone_prefix": "+34",
        "legal_footer": "Conforme a la ley española"
    },
    "Netherlands": {
        "code": "NL",
        "currency_code": "EUR",
        "currency_symbol": "€",
        "tax_type": "BTW",
        "phone_prefix": "+31",
        "legal_footer": "Nederlands recht"
    },
    "Poland": {
        "code": "PL",
        "currency_code": "PLN",
        "currency_symbol": "zł",
        "tax_type": "NIP",
        "phone_prefix": "+48",
        "legal_footer": "Zgodnie z prawem polskim"
    },
    "Czech Republic": {
        "code": "CZ",
        "currency_code": "CZK",
        "currency_symbol": "Kč",
        "tax_type": "DIČ",
        "phone_prefix": "+420",
        "legal_footer": "Podle českého práva"
    },
    "Brazil": {
        "code": "BR",
        "currency_code": "BRL",
        "currency_symbol": "R$",
        "tax_type": "CNPJ",
        "phone_prefix": "+55",
        "legal_footer": "Conforme legislação brasileira"
    },
    "Mexico": {
        "code": "MX",
        "currency_code": "MXN",
        "currency_symbol": "$",
        "tax_type": "RFC",
        "phone_prefix": "+52",
        "legal_footer": "Conforme a la ley mexicana"
    },
    "Canada": {
        "code": "CA",
        "currency_code": "CAD",
        "currency_symbol": "$",
        "tax_type": "BN",
        "phone_prefix": "+1",
        "legal_footer": "Governed by Canadian law"
    },
    "Japan": {
        "code": "JP",
        "currency_code": "JPY",
        "currency_symbol": "¥",
        "tax_type": "Corporate Number",
        "phone_prefix": "+81",
        "legal_footer": "日本国法に準拠"
    },
    "South Korea": {
        "code": "KR",
        "currency_code": "KRW",
        "currency_symbol": "₩",
        "tax_type": "Business Registration Number",
        "phone_prefix": "+82",
        "legal_footer": "대한민국 법률에 따름"
    },
    "Vietnam": {
        "code": "VN",
        "currency_code": "VND",
        "currency_symbol": "₫",
        "tax_type": "MST",
        "phone_prefix": "+84",
        "legal_footer": "Theo pháp luật Việt Nam"
    },
    "Thailand": {
        "code": "TH",
        "currency_code": "THB",
        "currency_symbol": "฿",
        "tax_type": "Tax ID",
        "phone_prefix": "+66",
        "legal_footer": "ตามกฎหมายไทย"
    },
    "Indonesia": {
        "code": "ID",
        "currency_code": "IDR",
        "currency_symbol": "Rp",
        "tax_type": "NPWP",
        "phone_prefix": "+62",
        "legal_footer": "Sesuai hukum Indonesia"
    },
    "Australia": {
        "code": "AU",
        "currency_code": "AUD",
        "currency_symbol": "$",
        "tax_type": "ABN",
        "phone_prefix": "+61",
        "legal_footer": "Governed by Australian law"
    },
    "United Arab Emirates": {
        "code": "AE",
        "currency_code": "AED",
        "currency_symbol": "د.إ",
        "tax_type": "TRN",
        "phone_prefix": "+971",
        "legal_footer": "Subject to UAE law"
    },
    "Saudi Arabia": {
        "code": "SA",
        "currency_code": "SAR",
        "currency_symbol": "﷼",
        "tax_type": "VAT Registration Number",
        "phone_prefix": "+966",
        "legal_footer": "وفقاً لأنظمة المملكة العربية السعودية"
    }
}

# =========================
# Helpers
# =========================

def random_date(start_year=2024, end_year=2025):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))

def generate_invoice(country_name: str) -> dict:
    c = COUNTRIES[country_name]
    inv_date = random_date()

    subtotal = round(random.uniform(1000, 50000), 2)
    tax_rate = random.choice([0.05, 0.1, 0.15, 0.18])
    tax_amount = round(subtotal * tax_rate, 2)
    total_amount = round(subtotal + tax_amount, 2)

    return {
        "invoice_metadata": {
            "invoice_id": str(uuid.uuid4()),
            "invoice_number": f"{c['code']}-{random.randint(10000, 99999)}",
            "invoice_date": inv_date.isoformat(),
            "due_date": (inv_date + timedelta(days=30)).isoformat(),
            "document_language": "en"
        },
        "supplier": {
            "name": f"{country_name} Trading Co.",
            "legal_name": f"{country_name} Trading Company Limited",
            "country": country_name,
            "country_code": c["code"],
            "address": {
                "line_1": "123 Business Street",
                "line_2": "",
                "city": "Capital City",
                "state_province": "",
                "postal_code": "000000"
            },
            "tax_id": {
                "value": str(random.randint(10**7, 10**12)),
                "type": c["tax_type"]
            },
            "phone": f"{c['phone_prefix']} {random.randint(100000000, 999999999)}",
            "email": "billing@example.com",
            "website": "www.example.com"
        },
        "buyer": {
            "name": "Global Buyer Ltd.",
            "country": "United Kingdom",
            "address": {
                "city": "London",
                "postal_code": "SW1A 1AA"
            }
        },
        "financials": {
            "currency_code": c["currency_code"],
            "currency_symbol": c["currency_symbol"],
            "subtotal": subtotal,
            "tax_rate": tax_rate,
            "tax_amount": tax_amount,
            "total_amount": total_amount,
            "payment_terms": "Net 30"
        },
        "banking": {
            "bank_name": "International Bank",
            "account_number": str(random.randint(10**9, 10**12)),
            "swift_bic": "INTLXXXX"
        },
        "text_blocks": {
            "line_items_text": "Supply of industrial components as agreed.",
            "legal_footer_text": c["legal_footer"],
            "compliance_text": "Goods comply with applicable regulations."
        },
        "variation_controls": {
            "omit_fields": random.sample(
                ["banking.swift_bic", "supplier.website", "supplier.phone"],
                k=random.randint(0, 1)
            ),
            "ocr_noise_level": random.choice(["low", "medium", "high"]),
            "language_mix": random.choice([True, False]),
            "ambiguous_currency": random.choice([True, False]),
            "date_format": random.choice(["YYYY-MM-DD", "DD-MM-YYYY"])
        },
        "ground_truth": {
            "supplier_country": country_name,
            "route": "A" if country_name in ["China", "Vietnam"] else "B"
        }
    }

# =========================
# Main
# =========================

def main():
    random.seed(RANDOM_SEED)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for country in COUNTRIES.keys():
        for i in range(INVOICES_PER_COUNTRY):
            invoice = generate_invoice(country)
            filename = f"{country.replace(' ', '_').lower()}_{i+1}.json"
            with open(OUTPUT_DIR / filename, "w", encoding="utf-8") as f:
                json.dump(invoice, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()