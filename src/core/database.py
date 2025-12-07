import streamlit as st
from supabase import create_client, Client
import os

@st.cache_resource
def get_db_client() -> Client:
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Erro ao conectar no Supabase: {e}")
        return None

def salvar_log_conversa(session_id, git_version, prompt, response, tema_match, desc_match):
    client = get_db_client()
    if not client:
        return

    try:
        data = {
            "session_id": session_id,
            "git_version": git_version,
            "prompt": prompt,
            "response": str(response),
            "tema_match": tema_match if tema_match else "N/A",
            "desc_match": desc_match if desc_match else "N/A"
        }
        client.table("chat_logs").insert(data).execute()
    except Exception as e:
        print(f"⚠️ Erro silencioso ao salvar log: {e}")

def salvar_erro(session_id, git_version, error_msg):
    client = get_db_client()
    if not client: return "ERRO-DB"

    try:
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
    
    if not client:
        return False

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


def buscar_referencias_db(vector_embedding, threshold=0.4, limit=1):
    client = get_db_client()
    if not client:
        return None, None
    try:
        response = client.rpc(
            "match_knowledge_base",
            {
                "query_embedding": vector_embedding,
                "match_threshold": threshold,
                "match_count": limit
            }
        ).execute()

        if response.data and len(response.data) > 0:
            melhor_match = response.data[0]
            return melhor_match['tema'], melhor_match['descricao']
        return None, None

    except Exception as e:
        print(f"⚠️ Erro na busca vetorial: {e}")
        return None, None
    
def add_conhecimento_db(tema, descricao, referencias, autor):
    client = get_db_client()
    if not client:
        return False
    try:
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=f"{tema}: {descricao}",
            task_type="retrieval_document"
        )
        vector_embedding = result['embedding']
        
        data = {
            "tema": tema,
            "descricao": descricao,
            "embedding": vector_embedding,
            "referencias": referencias,
            "autor": autor
        }
        client.table("knowledge_base").insert(data).execute()
        return True

    except Exception as e:
        print(f"⚠️ Erro ao adicionar na base de conhecimento: {e}")
        return False