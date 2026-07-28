from pathlib import Path
from typing import Any

import json
import streamlit as st
import gspread

# Folderul în care se află acest fișier
BASE_DIR = Path(__file__).resolve().parent

# Numele exact al fișierului JSON
CREDENTIALS_FILE = BASE_DIR / "aplicatie-crama-8bdab301466e.json"

# Numele fișierului Google Sheets
SPREADSHEET_NAME = "Crama"

# Numele taburilor
INREGISTRARI_SHEET = "Inregistrari"
PRODUSE_SHEET = "Produse"


def get_client() -> gspread.Client:
    """Conectare la Google Sheets local sau în Streamlit Cloud."""

    credentials_json = None

    # Încearcă să citească Secrets din Streamlit Cloud
    try:
        credentials_json = st.secrets.get("GOOGLE_CREDENTIALS_JSON")
    except Exception:
        # Local nu există secrets.toml, deci continuăm cu fișierul JSON
        credentials_json = None

    if credentials_json:
        credentials_info = json.loads(credentials_json)

        return gspread.service_account_from_dict(
            credentials_info
        )

    # Local, pe laptop
    if CREDENTIALS_FILE.exists():
        return gspread.service_account(
            filename=str(CREDENTIALS_FILE)
        )

    raise FileNotFoundError(
        "Nu există credențiale Google configurate."
    )


def get_spreadsheet() -> gspread.Spreadsheet:
    """Deschide fișierul Google Sheets numit Crama."""
    client = get_client()
    return client.open(SPREADSHEET_NAME)


def get_products() -> list[dict[str, Any]]:
    """
    Citește produsele din tabul Produse.

    Returnează ceva de forma:
    [
        {"ID": "1", "Produs": "Vin alb", "Pret Litru": "8"},
        ...
    ]
    """
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.worksheet(PRODUSE_SHEET)

    return worksheet.get_all_records()

def get_records() -> list[dict[str, Any]]:
    """Citește toate înregistrările din tabul Inregistrari."""
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.worksheet(INREGISTRARI_SHEET)

    return worksheet.get_all_records()

def get_next_id() -> int:
    """Calculează următorul ID disponibil din tabul Inregistrari."""
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.worksheet(INREGISTRARI_SHEET)

    values = worksheet.col_values(1)

    # Dacă există doar antetul sau foaia este goală
    if len(values) <= 1:
        return 1

    existing_ids = []

    for value in values[1:]:
        try:
            existing_ids.append(int(value))
        except (TypeError, ValueError):
            continue

    return max(existing_ids, default=0) + 1


def save_record(
    magazin: str,
    data: str,
    produs: str,
    intrare: float,
    pret_litru: float,
    bani_incasati: float,
    iesire: float,
    nr_bidoane: int,
    produs_special: float,
) -> int:
    """
    Adaugă o înregistrare nouă în tabul Inregistrari.

    Returnează ID-ul creat.
    """
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.worksheet(INREGISTRARI_SHEET)

    record_id = get_next_id()

    row = [
        record_id,
        data,
        magazin,
        produs,
        intrare,
        pret_litru,
        bani_incasati,
        iesire,
        nr_bidoane,
        produs_special,
    ]

    worksheet.append_row(row, value_input_option="USER_ENTERED")

    return record_id