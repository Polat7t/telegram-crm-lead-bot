import asyncio
import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDS_PATH = os.path.join(BASE_DIR, "creds.json")


def append_lead_sync(name: str, contact: str, task: str):
    creds = Credentials.from_service_account_file(CREDS_PATH, scopes=SCOPES)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(SPREADSHEET_ID).sheet1

    sheet.append_row([name, contact, task])


async def append_lead(name: str, contact: str, task: str):
    await asyncio.to_thread(append_lead_sync, name, contact, task)
