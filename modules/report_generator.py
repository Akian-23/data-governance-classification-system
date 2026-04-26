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


def print_governance_report(df):
    report = create_text_report(df)
    print(report)


def save_text_report(df, filename="governance_report.txt"):
    report = create_text_report(df)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nReport saved as {filename}")