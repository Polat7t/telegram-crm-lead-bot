import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

if not BOT_TOKEN:
    exit("Error: BOT_TOKEN not replaced in the file .env")