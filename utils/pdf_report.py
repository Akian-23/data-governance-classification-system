from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from utils.masking import mask_ssn, mask_credit_card, mask_email, mask_medical_note
from reportlab.platypus import Image
from reportlab.lib.pagesizes import landscape, letter


def create_pdf_report(df, summary, filename="governance_report.pdf"):

    # APPLY MASKING 
    df = df.copy()

    if "ssn" in df.columns:
        df["ssn"] = df["ssn"].apply(mask_ssn)

    if "credit_card" in df.columns:
        df["credit_card"] = df["credit_card"].apply(mask_credit_card)

    if "email" in df.columns:
        df["email"] = df["email"].apply(mask_email)

    if "medical_note" in df.columns:
        df["medical_note"] = df["medical_note"].apply(mask_medical_note)

    doc = SimpleDocTemplate(filename, pagesize=landscape(letter))
    elements = []
    styles = getSampleStyleSheet()

    # Title 
    elements.append(Paragraph("Data Governance Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Summary 
    elements.append(Paragraph("Classification Summary", styles["Heading2"]))
    elements.append(Spacer(1, 6))

    summary_data = [["Category", "Count"]] + list(summary.reset_index().values)

    summary_table = Table(summary_data, colWidths=[200, 100])

    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ]))

    elements.append(summary_table)

    # Chart
    elements.append(Spacer(1, 12))
    elements.append(Image("chart.png", width=450, height=300))
    elements.append(Spacer(1, 20))

    # Split data
    core_cols = ["id", "description", "Classification", "Retention", "Action"]
    core_df = df[core_cols]

    # Everything else = sensitive
    sensitive_cols = [col for col in df.columns if col not in core_cols]
    sensitive_df = df[["id"] + sensitive_cols] if sensitive_cols else None

    # Governance Table 
    elements.append(PageBreak())

    elements.append(Paragraph("Governance Decisions", styles["Heading2"]))
    elements.append(Spacer(1, 6))

    def format_table_data(df, styles):
        data = []

        data.append([
            Paragraph(f"<b>{col}</b>", styles["BodyText"])
            for col in df.columns
        ])

        for row in df.values:
            data.append([
                Paragraph(str(cell), styles["BodyText"])
                for cell in row
            ])

        return data
      

    core_table_data = format_table_data(core_df, styles)

    core_table = Table(
        core_table_data,
        repeatRows=1,
        colWidths=[50, 300, 100, 100, 140]
    )

    core_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.black),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.25, colors.black),
        ("FONTSIZE", (0,0), (-1,-1), 7),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.lightgrey]),
        
        ]))

    elements.append(core_table)

    # Sensitive Data
    if sensitive_df is not None and len(sensitive_df.columns) > 1:

        elements.append(PageBreak())
        elements.append(Paragraph("Sensitive Data (Masked)", styles["Heading2"]))
        elements.append(Spacer(1, 6))

        def format_table_data(df):
            data = []

            data.append([
                Paragraph(f"<b>{col}</b>", styles["BodyText"])
                for col in df.columns
            ])

            for row in df.values:
                data.append([
                    Paragraph(str(cell), styles["BodyText"])
                    for cell in row
                ])

            return data

        table_data = format_table_data(sensitive_df)
        num_cols = len(sensitive_df.columns)
        page_width = 750  

        col_widths = [page_width / num_cols] * num_cols

        sensitive_table = Table(
            table_data,
            repeatRows=1,
            colWidths=col_widths
        )

        sensitive_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.darkgrey),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("GRID", (0,0), (-1,-1), 0.25, colors.black),
            ("FONTSIZE", (0,0), (-1,-1), 7),
            ("LEFTPADDING", (0,0), (-1,-1), 4),
            ("RIGHTPADDING", (0,0), (-1,-1), 4),
            ("TOPPADDING", (0,0), (-1,-1), 3),
            ("BOTTOMPADDING", (0,0), (-1,-1), 3),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.lightgrey]),
        ]))

        elements.append(sensitive_table)

    doc.build(elements)