#!/usr/bin/env python3
"""
PDF Invoice Generator
Version: 1.0.0

Generates professional PDF invoices from JSON order data.
Uses ReportLab for PDF generation.

Usage:
    python invoice_generator.py --input orders.json --output invoices/

Requirements:
    pip install reportlab

Input JSON format:
    {
        "invoice_number": "INV-2026-0001",
        "date": "2026-04-07",
        "due_date": "2026-04-21",
        "from": {
            "name": "Your Company",
            "address": "123 Business St",
            "email": "billing@yourcompany.com"
        },
        "to": {
            "name": "Customer Name",
            "address": "456 Customer Ave",
            "email": "customer@email.com"
        },
        "items": [
            {"description": "Product Name", "quantity": 1, "unit_price": 29.00}
        ],
        "tax_rate": 0.0,
        "notes": "Thank you for your business!"
    }
"""

import argparse
import json
import os
import sys
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
except ImportError:
    print("ERROR: reportlab not installed. Run: pip install reportlab")
    sys.exit(1)


# ─── Configuration ────────────────────────────────────────────────────────────
COMPANY_NAME = os.environ.get("INVOICE_COMPANY_NAME", "Your Company Name")
COMPANY_ADDRESS = os.environ.get("INVOICE_COMPANY_ADDRESS", "Your Address")
COMPANY_EMAIL = os.environ.get("INVOICE_COMPANY_EMAIL", "billing@yourcompany.com")
LOGO_PATH = os.environ.get("INVOICE_LOGO_PATH", "")  # Optional: path to logo image


def generate_invoice(order_data: dict, output_path: str):
    """Generate a PDF invoice from order data."""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()
    elements = []

    # ── Header ────────────────────────────────────────────────────────────────
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontSize=24,
        textColor=colors.HexColor("#1a1a2e"),
        spaceAfter=10,
    )
    elements.append(Paragraph("INVOICE", title_style))

    # Invoice meta
    meta_style = ParagraphStyle("Meta", parent=styles["Normal"], fontSize=10, textColor=colors.grey)
    invoice_no = order_data.get("invoice_number", "INV-0000")
    invoice_date = order_data.get("date", datetime.now().strftime("%Y-%m-%d"))
    due_date = order_data.get("due_date", "")

    meta_text = f"<b>Invoice #:</b> {invoice_no}<br/><b>Date:</b> {invoice_date}"
    if due_date:
        meta_text += f"<br/><b>Due Date:</b> {due_date}"
    elements.append(Paragraph(meta_text, meta_style))
    elements.append(Spacer(1, 15 * mm))

    # ── From / To ─────────────────────────────────────────────────────────────
    from_data = order_data.get("from", {})
    to_data = order_data.get("to", {})

    address_style = ParagraphStyle("Address", parent=styles["Normal"], fontSize=10)
    from_text = f"<b>From:</b><br/>{from_data.get('name', COMPANY_NAME)}<br/>{from_data.get('address', COMPANY_ADDRESS)}<br/>{from_data.get('email', COMPANY_EMAIL)}"
    to_text = f"<b>Bill To:</b><br/>{to_data.get('name', 'Customer')}<br/>{to_data.get('address', '')}<br/>{to_data.get('email', '')}"

    address_table = Table([[Paragraph(from_text, address_style), Paragraph(to_text, address_style)]], colWidths=[100 * mm, 100 * mm])
    address_table.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    elements.append(address_table)
    elements.append(Spacer(1, 15 * mm))

    # ── Line Items ────────────────────────────────────────────────────────────
    items = order_data.get("items", [])
    if not items:
        elements.append(Paragraph("No items.", styles["Normal"]))
        return

    table_data = [["Description", "Qty", "Unit Price", "Amount"]]
    subtotal = Decimal("0")

    for item in items:
        qty = Decimal(str(item.get("quantity", 1)))
        unit_price = Decimal(str(item.get("unit_price", 0)))
        amount = qty * unit_price
        subtotal += amount
        table_data.append([
            item.get("description", ""),
            str(qty),
            f"${unit_price:,.2f}",
            f"${amount:,.2f}",
        ])

    tax_rate = Decimal(str(order_data.get("tax_rate", 0)))
    tax_amount = subtotal * tax_rate
    total = subtotal + tax_amount

    # Add subtotal, tax, total rows
    if tax_rate > 0:
        table_data.append(["", "", "Subtotal", f"${subtotal:,.2f}"])
        table_data.append(["", "", f"Tax ({float(tax_rate)*100:.1f}%)", f"${tax_amount:,.2f}"])

    table_data.append(["", "", "Total", f"${total:,.2f}"])

    items_table = Table(table_data, colWidths=[110 * mm, 20 * mm, 35 * mm, 35 * mm])
    items_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a1a2e")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
                ("ALIGN", (0, 0), (0, -1), "LEFT"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("TOPPADDING", (0, 0), (-1, 0), 8),
                ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.HexColor("#f9f9f9"), colors.white]),
                ("FONTNAME", (-1, -1), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (-1, -1), (-1, -1), 11),
                ("LINEABOVE", (2, -1), (-1, -1), 1, colors.HexColor("#1a1a2e")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
                ("GRID", (0, 0), (-1, -2), 0.25, colors.HexColor("#e0e0e0")),
            ]
        )
    )
    elements.append(items_table)
    elements.append(Spacer(1, 15 * mm))

    # ── Notes ─────────────────────────────────────────────────────────────────
    notes = order_data.get("notes", "")
    if notes:
        notes_para = Paragraph(f"<i>{notes}</i>", styles["Normal"])
        elements.append(notes_para)

    # ── Footer ─────────────────────────────────────────────────────────────────
    elements.append(Spacer(1, 20 * mm))
    footer_style = ParagraphStyle("Footer", parent=styles["Normal"], fontSize=8, textColor=colors.grey, alignment=1)
    elements.append(Paragraph(f"{COMPANY_NAME} — {COMPANY_EMAIL}", footer_style))

    doc.build(elements)
    return output_path


def process_batch(input_path: str, output_dir: str):
    """Process a batch of orders from a JSON file or directory."""
    os.makedirs(output_dir, exist_ok=True)

    if os.path.isdir(input_path):
        files = [f for f in os.listdir(input_path) if f.endswith(".json")]
    else:
        files = [input_path]
        input_path = os.path.dirname(input_path)

    generated = 0
    for fname in files:
        fpath = os.path.join(input_path, fname) if os.path.isdir(input_path) else fname
        try:
            with open(fpath) as f:
                order_data = json.load(f)

            invoice_no = order_data.get("invoice_number", fname.replace(".json", ""))
            out_filename = f"invoice_{invoice_no}.pdf"
            out_path = os.path.join(output_dir, out_filename)

            generate_invoice(order_data, out_path)
            print(f"✅ Generated: {out_path}")
            generated += 1
        except Exception as e:
            print(f"❌ Error processing {fname}: {e}")

    print(f"\nDone. Generated {generated} invoice(s).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF Invoice Generator")
    parser.add_argument("--input", required=True, help="Input JSON file or directory")
    parser.add_argument("--output", default="invoices/", help="Output directory")
    args = parser.parse_args()

    process_batch(args.input, args.output)
