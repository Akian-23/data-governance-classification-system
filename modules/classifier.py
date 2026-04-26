import re

def classify_record(row):
    # Combine all non-null values into one string
    text = " ".join([str(v).lower() for v in row.values if v and str(v) != "nan"])

    # COLUMN-BASED CHECKS
    if str(row.get("ssn")) != "nan" and row.get("ssn"): # SSN
        return "Highly Sensitive"
    
    if str(row.get("credit_card")) != "nan" and row.get("credit_card"): # Credit Card
        return "Highly Sensitive"

    if str(row.get("medical_note")) != "nan" and row.get("medical_note"):
        return "Highly Sensitive"

    # PATTERN CHECKS 
    if re.search(r"\d{3}-\d{2}-\d{4}", text):
        return "Highly Sensitive"

    if re.search(r"\d{4}-\d{4}-\d{4}-\d{4}", text):
        return "Highly Sensitive"

    # CONFIDENTIAL
    if (
        "salary" in text
        or "compensation" in text
        or "invoice" in text
        or "billing" in text
        or "financial" in text
        or "performance" in text
        or "evaluation" in text
    ):
        return "Confidential"

    # INTERNAL 
    if (
        "internal" in text
        or "strategy" in text
        or "audit" in text
        or "project" in text
        or "hr" in text
        or "policy" in text
        or "support" in text
        or "training" in text
    ):
        return "Internal"

    # DEFAULT 
    return "Public"


def classify_dataset(df):
    df["Classification"] = df.apply(classify_record, axis=1)
    return df