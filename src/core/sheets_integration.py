# src/core/sheets_integration.py
import os
import streamlit as st
import gspread
from gspread.exceptions import SpreadsheetNotFound
from google.oauth2.service_account import Credentials
from datetime import datetime
import pytz

from src.utils import get_current_branch

def append_to_sheet(session_id, prompt, response):
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
        ]
        
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"], scopes=scopes
        )
        client = gspread.authorize(creds)
        sheet_id = st.secrets.get("LOG", "") or os.environ.get("LOG", "")
        
        spreadsheet = client.open_by_key(sheet_id)

        if get_current_branch() == 'Production':
            worksheet_name = 'prod'
        else:
            worksheet_name = 'dev'
        
        worksheet = spreadsheet.worksheet(worksheet_name)
        local_tz = pytz.timezone('America/Bahia')
        timestamp = datetime.now(local_tz).strftime("%Y-%m-%d %H:%M:%S")
        new_row = [session_id, timestamp, prompt, response]
        worksheet.append_row(new_row)
        
    except SpreadsheetNotFound as e:
        error_message = f"ERRO INESPERADO DURANTE A INTEGRAÇÃO: {e}"
        print(error_message)
        raise Exception(error_message)