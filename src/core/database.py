import streamlit as st
from supabase import create_client, Client
import os
import google.generativeai as genai

@st.cache_resource
def get_db_client() -> Client:
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Erro ao conectar no banco de dados: {e}")
        return None

def salvar_sessao(session_id):
    client = get_db_client()
    if not client:
        print("Não foi possível conectar com o banco de dados.")
        return
    try:
        registro_sessao = {
                "session_id" : session_id
            }
        client.table("sessions").insert(registro_sessao).execute()
    except Exception as e:
        print(f"⚠️ Erro ao tentar registrar sessão no banco de dados: {e}")

def salvar_log_chat(session_id, git_version, prompt, response, tema_match):
    client = get_db_client()
    if not client:
        print("Não foi possível conectar com o banco de dados.")
        return
    try:
        kb_id_real = "vox-kb-0000"
        if tema_match:
            try:
                busca_kb = (
                    client.table("knowledge_base")
                    .select("kb_id") 
                    .eq("tema", tema_match)
                    .execute()
                )
                
                if busca_kb.data and len(busca_kb.data) > 0:
                    kb_id_real = str(busca_kb.data[0]['kb_id'])
                    
            except Exception as e_busca:
                print(f"⚠️ Aviso: Não foi possível recuperar ID do tema: {e_busca}")

        data = {
            "session_id": session_id,
            "prompt": prompt,
            "response": str(response),
            "kb_id": kb_id_real,
            "git_version": git_version,
        }
        
        client.table("chat_logs").insert(data).execute()
        
    except Exception as e:
        print(f"⚠️ Log do chat não está sendo salvo: {e}")

def buscar_referencias_db(vector_embedding, threshold=0.5, limit=1):
    client = get_db_client()
    if not client:
        print("⚠️ Erro: Cliente Supabase não inicializado.")
        return None, None
    try:
        if len(vector_embedding) != 768:
            print(f"⚠️ Erro de Dimensão: O vetor gerado tem {len(vector_embedding)} dimensões, mas o banco espera 768.")
            return None, None

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
            print(f"✅ Match encontrado: {melhor_match['tema']} ({melhor_match['similarity']:.2f})")
            return melhor_match['tema'], melhor_match['descricao']
            
        print("⚠️ Nenhum match encontrado na base com esse threshold.")
        return None, None

    except Exception as e:
        print(f"❌ Erro CRÍTICO na busca vetorial (Supabase): {e}")
        return None, None

def salvar_erro(session_id, git_version, error_msg):
    client = get_db_client()
    if not client:
        return "ERRO-DB"
    try:
        import uuid
        error_id = str(uuid.uuid4())[:8]
        
        data = {
            "error_id": error_id,
            "error_message": str(error_msg),
            "session_id": session_id,
            "git_version": git_version
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