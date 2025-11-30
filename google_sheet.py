import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

def get_next_row():
    credentials_json = os.getenv("GOOGLE_SHEET_CREDENTIALS")
    sheet_id = os.getenv("SHEET_ID")

    creds_dict = json.loads(credentials_json)

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).worksheet("Master")

    rows = sheet.get_all_records()

    for index, row in enumerate(rows, start=2):  # starts row indexing at 2 to skip header
        if row['status'].lower() == 'pending':
            return row, index

    return None, None

