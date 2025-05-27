import gspread
import json
import os
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from datetime import datetime
import pytz

# Carrega variáveis de ambiente de um arquivo .env para desenvolvimento local
load_dotenv()

def sync_knowledge_base():
    """
    Busca dados da planilha, atualiza o JSON local para registros com status 'pendente',
    e depois atualiza o status desses registros na própria planilha para 'Sincronizado'.
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

        # --- Define caminhos e timezone ---
        json_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'knowledge_base.json')
        local_tz = pytz.timezone('America/Bahia')

        # --- Carrega a base de conhecimento existente ---
        knowledge_base_dict = {}
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                for item in existing_data:
                    knowledge_base_dict[item['id']] = item
        else:
            print("Arquivo knowledge_base.json não encontrado. Um novo será criado.")

        # --- Acessa a Planilha ---
        sheet_id = os.environ.get("KB_SHEET_ID", "")
        if not sheet_id:
            raise ValueError("A variável de ambiente KB_SHEET_ID não foi definida.")
            
        spreadsheet = client.open_by_key(sheet_id)
        worksheet = spreadsheet.worksheet("origin")
        
        # Pega os cabeçalhos para encontrar a coluna 'status'
        headers = worksheet.row_values(1)
        try:
            # Adiciona 1 porque a lista é baseada em 0, e as colunas da planilha em 1
            status_col_index = headers.index("status") + 1
        except ValueError:
            print("ERRO: A coluna 'status' não foi encontrada na planilha. A sincronização não pode continuar.")
            return

        records = worksheet.get_all_records(expected_headers=headers)
        print(f"Planilha '{worksheet.title}' carregada com sucesso com {len(records)} registros.")
        
        updates_count = 0
        cells_to_update_on_sheet = []

        # Itera sobre os registros para encontrar os pendentes
        # 'enumerate' nos dá o número da linha (começando em 2, pois a linha 1 é o cabeçalho)
        for row_num, record in enumerate(records, start=2):
            if str(record.get("status", "")).lower() == "pendente":
                record_id = record.get("id")
                if not record_id or not record.get("tema") or not record.get("descricao"):
                    print(f"AVISO: Pulando linha {row_num} por falta de dados essenciais (id, tema ou descricao).")
                    continue

                # Prepara a atualização do status para a planilha
                cells_to_update_on_sheet.append(gspread.Cell(row_num, status_col_index, "Sincronizado"))
                
                # Prepara a atualização do JSON
                current_time_iso = datetime.now(local_tz).isoformat()
                creation_date = knowledge_base_dict.get(record_id, {}).get('criacao', record.get('criacao') or current_time_iso)
                
                references_str = record.get("referencias", "")
                references_list = [ref.strip() for ref in references_str.split(';') if ref.strip()]

                knowledge_base_dict[str(record_id)] = {
                    "id": str(record_id),
                    "tema": record["tema"],
                    "descricao": record["descricao"],
                    "referencias": references_list,
                    "criacao": creation_date,
                    "modificado_em": current_time_iso,
                }
                updates_count += 1
                print(f"Registro '{record_id}' (linha {row_num}) processado para atualização.")

        # --- Executa as atualizações se houver registros pendentes ---
        if updates_count > 0:
            # 1. Salva as alterações no arquivo JSON
            final_knowledge_base = list(knowledge_base_dict.values())
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(final_knowledge_base, f, ensure_ascii=False, indent=2)
            print(f"✅ Arquivo knowledge_base.json atualizado com {updates_count} alterações.")

            # 2. Atualiza as células de status na planilha de uma só vez (em lote)
            if cells_to_update_on_sheet:
                worksheet.update_cells(cells_to_update_on_sheet, value_input_option='USER_ENTERED')
                print(f"✅ Status de {len(cells_to_update_on_sheet)} registros foi atualizado para 'Sincronizado' na planilha.")
        else:
            print("Nenhum registro com status 'pendente' encontrado. Nenhuma alteração foi feita.")

    except gspread.exceptions.SpreadsheetNotFound:
        print(f"ERRO: A planilha com o ID '{sheet_id}' não foi encontrada.")
    except Exception as e:
        print(f"❌ Ocorreu um erro inesperado durante a sincronização: {e}")

if __name__ == "__main__":
    sync_knowledge_base()