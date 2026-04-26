import pandas as pd

def detect_data_type(row):
    if pd.notna(row.get("medical_note")):
        return "medical"
    if pd.notna(row.get("ssn")) or pd.notna(row.get("credit_card")):
        return "financial"
    return "general"

def apply_governance(classification):
    rules = {
        "Public": {
            "retention": "No restriction",
            "action": "Standard storage"
        },
        "Internal": {
            "retention": "3-5 years",
            "action": "Internal access only"
        },
        "Confidential": {
            "retention": "7 years",
            "action": "Restricted access"
        },
        "Highly Sensitive": {
            "retention": "7-10 years",
            "action": "Encryption + restricted access"
        }
    }

    return rules.get(classification, {
        "retention": "Unknown",
        "action": "Unknown"
    })


def apply_governance_to_dataset(df):
    df = df.copy()
    retention_list = []
    action_list = []
    
    for _, row in df.iterrows():
        classification = row["Classification"]
        data_type = detect_data_type(row)

        policy = apply_governance(classification)

        # Optional refinement (this is the improvement layer)
        if classification == "Highly Sensitive":
            if data_type == "medical":
                policy["retention"] = "6 years (HIPAA-inspired)"
            elif data_type == "financial":
                policy["retention"] = "8 years (SOX-inspired)"

        retention_list.append(policy["retention"])
        action_list.append(policy["action"])

    df["Retention"] = retention_list
    df["Action"] = action_list

    return df