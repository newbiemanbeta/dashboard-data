
import time
import datetime
import pandas as pd
import gspread
# from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
import json
import openai
import psycopg2
from psycopg2.extras import Json
import re
import os
from dotenv import load_dotenv

# --- CONFIGURATION ---
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = service_account.Credentials.from_service_account_file("secret_key.json", scopes=scopes)

load_dotenv()

File_name = os.getenv("File_name")
sheet_name = os.getenv("sheet_name")
shtindx = int(os.getenv("shtindx"))




def gspreadget(sheet_name, worksheet_index):
    gc = gspread.authorize(creds)
    sh = gc.open(sheet_name)
    worksheet = sh.get_worksheet(worksheet_index)
    return pd.DataFrame(worksheet.get_all_records())

slowtide_data = gspreadget(File_name, shtindx)

platform_data = slowtide_data.groupby(['Date','Platform','Country'])[['Amount Spent', 'Impressions',
       '3-second video plays', 'Outbound Clicks', 'Adds To Cart',
       'Website Purchases', 'Website Purchases Conversion Value']].sum().reset_index()
US_platform_data = platform_data[platform_data['Country']=="USA"]
CA_platform_data = platform_data[platform_data['Country']=="CAN"]
