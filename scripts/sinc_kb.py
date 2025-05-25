import gspread
import json
import os
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

# Carrega variáveis de ambiente de um arquivo .env para desenvolvimento local
load_dotenv()

def sync_knowledge_base():
    """
    Busca os dados da planilha do Google Sheets e atualiza o 
    arquivo local knowledge_base.json, usando o 'id' como chave.
    """
    try:
        print("Iniciando a sincronização da base de conhecimento...")

        # --- Autenticação ---
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
        ]
        
        gcp_creds_dict = json.loads(os.environ.get("GCP_SERVICE_ACCOUNT"))
        creds = Credentials.from_service_account_info(gcp_creds_dict, scopes=scopes)
        client = gspread.authorize(creds)

        # --- Busca dos Dados ---
        sheet_id = os.environ.get("KB_SHEET_ID", "")
        if not sheet_id:
            raise ValueError("A variável de ambiente KB_SHEET_ID não foi definida.")
            
        spreadsheet = client.open_by_key(sheet_id)
        worksheet = spreadsheet.worksheet("base")
        
        records = worksheet.get_all_records()
        
        if not records:
            print("Nenhum registro encontrado na planilha. O arquivo JSON não será alterado.")
            return

        print(f"Foram encontrados {len(records)} registros na planilha.")

        # --- Processamento e Formatação com base no ID ---
        knowledge_base = []
        processed_ids = set()

        for record in records:
            # Pega o ID e verifica se ele existe e é único
            record_id = record.get("id")
            if not record_id:
                print(f"AVISO: Pulando registro por falta de 'id': {record}")
                continue
            
            if record_id in processed_ids:
                print(f"AVISO: ID duplicado encontrado e ignorado: '{record_id}'")
                continue
            
            processed_ids.add(record_id)

            # Garante que 'tema' e 'descricao' existam
            if not record.get("tema") or not record.get("descricao"):
                print(f"AVISO: Pulando registro com ID '{record_id}' por falta de 'tema' ou 'descricao'.")
                continue

            # Processa as referências
            references_str = record.get("referencias", "")
            references_list = [ref.strip() for ref in references_str.split(';')] if references_str else []
            
            knowledge_base.append({
                "id": str(record_id), # Garante que o ID seja uma string
                "tema": record["tema"],
                "descricao": record["descricao"],
                "referencias": references_list
            })

        # --- Escrita do JSON ---
        json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'knowledge_base.json')
        
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(knowledge_base, f, ensure_ascii=False, indent=2)

        print(f"✅ O arquivo knowledge_base.json foi atualizado com sucesso com {len(knowledge_base)} registros!")

    except gspread.exceptions.SpreadsheetNotFound:
        print(f"ERRO: A planilha com o ID '{sheet_id}' não foi encontrada.")
    except Exception as e:
        print(f"❌ Ocorreu um erro inesperado durante a sincronização: {e}")

if __name__ == "__main__":
    sync_knowledge_base()