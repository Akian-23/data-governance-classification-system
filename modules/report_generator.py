from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def create_text_report(df):
    summary = df["Classification"].value_counts()

    report = []

    report.append("\n==============================")
    report.append("DATA GOVERNANCE REPORT")
    report.append("==============================\n")

    report.append("CLASSIFICATION SUMMARY:")
    report.append("------------------------")

    for k, v in summary.items():
        report.append(f"{k}: {v}")

    report.append("\nFULL DATASET OUTPUT:")
    report.append("------------------------")

    report.append(df[["id", "description", "Classification", "Retention", "Action"]].to_string(index=False))

    report.append("\n==============================")
    report.append("END OF REPORT")
    report.append("==============================\n")

    return "\n".join(report)

def create_pdf_report(df, summary, filename="governance_report.pdf"):
    doc = SimpleDocTemplate(filename)

    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("Data Governance Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Summary
    elements.append(Paragraph("Classification Summary", styles["Heading2"]))
    elements.append(Spacer(1, 6))

    summary_data = [["Category", "Count"]] + list(summary.reset_index().values)

    table = Table(summary_data, colWidths=[200, 100])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))

    # Build PDF
    doc.build(elements)
    
def print_governance_report(df):
    report = create_text_report(df)
    print(report)


def save_text_report(df, filename="governance_report.txt"):
    report = create_text_report(df)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nReport saved as {filename}")