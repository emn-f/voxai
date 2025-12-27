"""
Script de teste para debug da função salvar_log_chat
"""
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configura o Streamlit secrets mock se necessário
import streamlit as st

# Mock dos secrets
if "supabase" not in st.secrets:
    print("⚠️ Aviso: Secrets do Supabase não configurados no ambiente de teste")

# Importa a função
from src.core.database import salvar_log_chat, salvar_sessao

# Dados de teste
session_id_teste = "test-session-123"
git_version_teste = "v2.0-test"
prompt_teste = "teste de salvamento"
response_teste = "resposta de teste"
fonte_info_teste = "Teste"
lista_kb_ids_teste = ["vox-kb-0001", {"kb_id": "vox-kb-0002", "similarity": 0.95}]

print("=" * 60)
print("🧪 INICIANDO TESTE DA FUNÇÃO salvar_log_chat")
print("=" * 60)

# Cria a sessão primeiro para evitar erro de FK
try:
    print(f"Criando sessão de teste: {session_id_teste}")
    salvar_sessao(session_id_teste)
except Exception as e:
    print(f"Aviso: erro ao criar sessão (pode já existir): {e}")

# Chama a função
try:
    salvar_log_chat(
        session_id=session_id_teste,
        git_version=git_version_teste,
        prompt=prompt_teste,
        response=response_teste,
        fonte_info=fonte_info_teste,
        lista_kb_ids=lista_kb_ids_teste,
    )
    print("\n" + "=" * 60)
    print("✅ Teste concluído sem exceções!")
    print("=" * 60)
except Exception as e:
    print("\n" + "=" * 60)
    print(f"❌ ERRO durante o teste: {e}")
    print("=" * 60)
    import traceback
    traceback.print_exc()
