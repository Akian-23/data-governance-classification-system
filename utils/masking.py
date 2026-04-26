import pandas as pd

def mask_ssn(ssn):
    if pd.isna(ssn):
        return ssn
    ssn = str(ssn)
    return "***-**-" + ssn[-4:]


def mask_credit_card(card):
    if pd.isna(card):
        return card
    card = str(card)
    return "****-****-****-" + card[-4:]


def mask_email(email):
    if pd.isna(email):
        return email
    email = str(email)
    parts = email.split("@")
    if len(parts) != 2:
        return email
    return parts[0][0] + "***@" + parts[1]


def mask_medical_note(note):
    if pd.isna(note):
        return note
    return "REDACTED (Medical Information)"