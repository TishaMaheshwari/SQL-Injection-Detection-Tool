from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime


def generate_pdf(target, manual_result, payloads, auto_result, severity, scan_time):

    styles = getSampleStyleSheet()

    file_name = "SQL_Report.pdf"

    pdf = SimpleDocTemplate(file_name, pagesize=A4)

    elements = []

    elements.append(Paragraph("SQL Injection Detection Report", styles['Title']))
    elements.append(Spacer(1,10))

    elements.append(Paragraph(f"Date: {datetime.now()}", styles['Normal']))
    elements.append(Spacer(1,10))

    elements.append(Paragraph(f"Target URL: {target}", styles['Normal']))
    elements.append(Spacer(1,10))

    elements.append(Paragraph(f"Manual Result: {manual_result}", styles['Normal']))
    elements.append(Paragraph(f"Severity: {severity}", styles['Normal']))
    elements.append(Spacer(1,10))

    elements.append(Paragraph("Payloads Tested:", styles['Heading2']))

    for p in payloads:
        elements.append(Paragraph(p, styles['Normal']))

    elements.append(Spacer(1,10))

    elements.append(Paragraph(f"Automated Result: {auto_result}", styles['Normal']))
    elements.append(Spacer(1,10))

    elements.append(Paragraph("Vulnerability Details", styles['Heading2']))
    elements.append(Paragraph("Type: SQL Injection", styles['Normal']))
    elements.append(Paragraph("Impact: Database Access Possible", styles['Normal']))

    elements.append(Spacer(1,10))

    elements.append(Paragraph(f"Scan Time: {scan_time} seconds", styles['Normal']))

    pdf.build(elements)
