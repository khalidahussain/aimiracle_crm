from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle,
    Paragraph, Spacer, Image
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

import io
import os
from django.conf import settings


def generate_invoice(order):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    elements = []
    styles = getSampleStyleSheet()

    # -------------------------------
    # LOGO + COMPANY HEADER
    # -------------------------------
    logo_path = os.path.join(settings.BASE_DIR, 'static/images/logo.png')

    if os.path.exists(logo_path):
        logo = Image(logo_path, width=1.5 * inch, height=1 * inch)
    else:
        logo = Paragraph("Aimiracle", styles['Title'])

    company_info = Paragraph(
        "<b>Aimiracle Pvt Ltd</b><br/>"
        "Raipur, Chhattisgarh<br/>"
        "Phone: +91-XXXXXXXXXX<br/>"
        "Email: info@aimiracle.in<br/>"
        "<b>GST:</b> 22XXXXX1234Z5",
        styles['Normal']
    )

    header_table = Table([
        [logo, company_info]
    ], colWidths=[2.5 * inch, 4 * inch])

    elements.append(header_table)
    elements.append(Spacer(1, 20))

    # -------------------------------
    # INVOICE TITLE
    # -------------------------------
    elements.append(Paragraph(f"<b>INVOICE #{order.id}</b>", styles['Title']))
    elements.append(Spacer(1, 10))

    # -------------------------------
    # CLIENT + INVOICE DETAILS
    # -------------------------------
    client_info = Paragraph(
        f"<b>Bill To:</b><br/>"
        f"{order.client.school_name}<br/>"
        f"{order.client.address}<br/>"
        f"Phone: {order.client.phone}",
        styles['Normal']
    )

    invoice_info = Paragraph(
        f"<b>Date:</b> {order.created_at.strftime('%d-%m-%Y')}<br/>"
        f"<b>Status:</b> {order.status}",
        styles['Normal']
    )

    info_table = Table([
        [client_info, invoice_info]
    ], colWidths=[3.5 * inch, 3 * inch])

    elements.append(info_table)
    elements.append(Spacer(1, 20))

    # -------------------------------
    # ITEMS TABLE
    # -------------------------------
    data = [["#", "Product", "Qty", "Price", "Total"]]

    for i, item in enumerate(order.items.all(), start=1):
        data.append([
            i,
            item.product.name,
            item.quantity,
            f"₹{item.price}",
            f"₹{item.get_total_price()}",
        ])

    # TOTAL ROW
    data.append(["", "", "", "Total", f"₹{order.total_amount}"])

    table = Table(data, repeatRows=1)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('ALIGN', (2, 1), (-1, -1), 'CENTER'),

        ('GRID', (0, 0), (-1, -1), 1, colors.grey),

        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

        ('BACKGROUND', (-2, -1), (-1, -1), colors.lightgrey),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # -------------------------------
    # BANK DETAILS
    # -------------------------------
    bank_details = Paragraph(
        "<b>Bank Details:</b><br/>"
        "Account Name: Aimiracle Pvt Ltd<br/>"
        "Bank: HDFC Bank<br/>"
        "Account No: XXXXXXXXXXXX<br/>"
        "IFSC: HDFC000XXXX<br/>"
        "UPI: aimiracle@upi",
        styles['Normal']
    )

    elements.append(bank_details)
    elements.append(Spacer(1, 20))

    # -------------------------------
    # FOOTER
    # -------------------------------
    elements.append(Paragraph(
        "Thank you for your business!<br/>"
        "This is a computer-generated invoice.",
        styles['Normal']
    ))

    # -------------------------------
    # BUILD PDF
    # -------------------------------
    doc.build(elements)
    buffer.seek(0)

    return buffer.getvalue()