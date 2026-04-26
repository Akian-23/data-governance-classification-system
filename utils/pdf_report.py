from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def create_pdf_report(df, summary, filename="governance_report.pdf"):
    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()
    content = []

    # TITLE
    content.append(Paragraph("Data Governance Report", styles["Title"]))
    content.append(Spacer(1, 12))

    # SUMMARY
    content.append(Paragraph("Classification Summary", styles["Heading2"]))

    summary_data = [[k, str(v)] for k, v in summary.items()]
    summary_table = Table([["Category", "Count"]] + summary_data)

    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
    ]))

    content.append(summary_table)
    content.append(Spacer(1, 12))

    # DATA TABLE (limited columns for readability)
    content.append(Paragraph("Detailed Records", styles["Heading2"]))

    table_data = [df.columns.tolist()] + df[["id","description","Classification","Retention","Action"]].values.tolist()

    data_table = Table(table_data)

    data_table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
    ]))

    content.append(data_table)

    doc.build(content)