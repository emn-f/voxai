import os
import streamlit as st
import gspread
from gspread.exceptions import SpreadsheetNotFound
from google.oauth2.service_account import Credentials
from datetime import datetime
import pytz
import uuid

from src.utils import get_current_branch

def append_to_sheet(git_version, session_id, prompt, response, tema_match, desc_match):
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
        new_row = [git_version, session_id, timestamp, prompt, response, tema_match, desc_match]
        worksheet.append_row(new_row)
        
    except SpreadsheetNotFound as e:
        error_message = f"ERRO INESPERADO DURANTE A INTEGRAÇÃO: {e}"
        print(error_message)
        raise Exception(error_message)
    
def log_exception(git_version, session_id, error_detail):

    error_id = str(uuid.uuid4())[:8]
    
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
        
        worksheet = spreadsheet.worksheet('errors')
        
        local_tz = pytz.timezone('America/Bahia')
        timestamp = datetime.now(local_tz).strftime("%Y-%m-%d %H:%M:%S")
        
        error_str = str(error_detail)
        
        new_row = [error_id, timestamp, git_version, session_id, error_str]
        worksheet.append_row(new_row)
        
        return error_id

    except Exception as e:
        print(f"CRITICAL: Falha ao registrar erro na planilha. ID: {error_id} - Erro original: {error_detail} - Erro do Log: {e}")
        return error_id

def log_report(git_version, session_id, history_data):
    """
    Registra uma denúncia de comportamento inadequado na aba 'reports'.
    Salva o histórico da conversa formatado.
    """
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
        
        try:
             worksheet = spreadsheet.worksheet('reports')
        except gspread.exceptions.WorksheetNotFound:
             worksheet = spreadsheet.add_worksheet(title="reports", rows="1000", cols="4")
             worksheet.append_row(["Timestamp", "Session ID", "Git Version", "Chat History"])
        
        local_tz = pytz.timezone('America/Bahia')
        timestamp = datetime.now(local_tz).strftime("%Y-%m-%d %H:%M:%S")
        
        full_history_text = ""
        for msg in history_data:
            role_display = "👤 Usuário" if msg['role'] == 'user' else "🤖 Vox"
            content = msg.get('parts', [''])[0] if isinstance(msg.get('parts'), list) else str(msg.get('parts', ''))
            full_history_text += f"{role_display}: {content}\n{'-'*20}\n"
            
        new_row = [timestamp, session_id, git_version, full_history_text]
        worksheet.append_row(new_row)
        
        return True

    except Exception as e:
        error_msg = f"Erro ao salvar denúncia: {str(e)}"
        print(error_msg)
        st.error(error_msg)
        return False