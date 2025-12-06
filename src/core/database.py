import streamlit as st
from supabase import create_client, Client
import os

# Função para garantir a conexão única (Singleton)
@st.cache_resource
def get_db_client() -> Client:
    try:
        # Tenta pegar dos secrets do Streamlit, ou variáveis de ambiente (local/docker)
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Erro ao conectar no Supabase: {e}")
        return None

# --- FUNÇÕES DE LOG (Substitui sheets_integration) ---

def salvar_log_conversa(session_id, git_version, prompt, response, tema_match, desc_match):
    """Salva o log da conversa no Supabase de forma assíncrona (se possível)"""
    client = get_db_client()
    if not client: return

    try:
        data = {
            "session_id": session_id,
            "git_version": git_version,
            "prompt": prompt,
            "response": str(response), # Garante que é string
            "tema_match": tema_match if tema_match else "N/A",
            "desc_match": desc_match if desc_match else "N/A"
        }
        # table().insert() envia para o banco
        client.table("chat_logs").insert(data).execute()
    except Exception as e:
        print(f"⚠️ Erro silencioso ao salvar log: {e}")

def salvar_erro(session_id, git_version, error_msg):
    client = get_db_client()
    if not client: return "ERRO-DB"

    try:
        # Gera um ID curto para o erro (opcional, ou deixa o banco gerar)
        import uuid
        error_id = str(uuid.uuid4())[:8]
        
        data = {
            "error_id": error_id,
            "session_id": session_id,
            "git_version": git_version,
            "error_message": str(error_msg)
        }
        client.table("error_logs").insert(data).execute()
        return error_id
    except Exception as e:
        print(f"⚠️ Erro ao salvar exceção: {e}")
        return "N/A"

def salvar_report(session_id, git_version, history_text):
    client = get_db_client()
    if not client: return False

    try:
        data = {
            "session_id": session_id,
            "git_version": git_version,
            "chat_history": history_text
        }
        client.table("user_reports").insert(data).execute()
        return True
    except Exception as e:
        print(f"⚠️ Erro ao salvar report: {e}")
        return False

# --- FUNÇÃO DE BUSCA SEMÂNTICA (RAG) ---

def buscar_referencias_db(vector_embedding, threshold=0.4, limit=1):
    """
    Chama a função RPC 'match_knowledge_base' lá no Supabase
    """
    client = get_db_client()
    if not client: return None, None

    try:
        # Chama a função SQL que criamos no Passo 4.0
        response = client.rpc(
            "match_knowledge_base",
            {
                "query_embedding": vector_embedding,
                "match_threshold": threshold,
                "match_count": limit
            }
        ).execute()

        # Se houver dados na resposta
        if response.data and len(response.data) > 0:
            melhor_match = response.data[0]
            return melhor_match['tema'], melhor_match['descricao']
        
        return None, None

    except Exception as e:
        print(f"⚠️ Erro na busca vetorial: {e}")
        return None, None