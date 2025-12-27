import os

import google.generativeai as genai
import streamlit as st

from src.config import LIMITE_TEMAS, MAX_CHUNCK, SEMANTICA_THRESHOLD
from supabase import Client, create_client


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
        registro_sessao = {"session_id": session_id}
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
                    kb_id_real = str(busca_kb.data[0]["kb_id"])

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
            "git_version": git_version,
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
            "chat_history": history_text,
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
            task_type="retrieval_document",
        )
        vector_embedding = result["embedding"]

        data = {
            "tema": tema,
            "descricao": descricao,
            "embedding": vector_embedding,
            "referencias": referencias,
            "autor": autor,
        }
        client.table("knowledge_base").insert(data).execute()
        return True

    except Exception as e:
        print(f"⚠️ Erro ao adicionar na base de conhecimento: {e}")
        return False


def buscar_referencias_db(
    vector_embedding,
    threshold=SEMANTICA_THRESHOLD,
    limit=LIMITE_TEMAS,
    filter_topic=None,
):
    client = get_db_client()
    if not client:
        print("⚠️ Erro: Cliente Supabase não inicializado.")
        return []
    try:
        if len(vector_embedding) != 768:
            print(
                f"⚠️ Erro de Dimensão: O vetor gerado tem {len(vector_embedding)} dimensões, mas o banco espera 768."
            )
            return []

        params = {
            "query_embedding": vector_embedding,
            "match_threshold": threshold,
            "match_count": limit,
            "filter_topic": filter_topic,
        }

        response = client.rpc("match_knowledge_base", params).execute()

        if response.data:
            return response.data
        else:
            print("⚠️ Nenhum match encontrado na base com esse threshold.")
        return []

    except Exception as e:
        print(f"❌ Erro CRÍTICO na busca vetorial (Supabase): {e}")
        return []


def recuperar_contexto_inteligente(vector_embedding):
    client = get_db_client()
    if not client:
        print("⚠️ Erro: Cliente Supabase não inicializado.")
        return [], "Erro DB"
    resultados_iniciais = buscar_referencias_db(
        vector_embedding, SEMANTICA_THRESHOLD, LIMITE_TEMAS, None
    )
    if not resultados_iniciais:
        return None, "Nenhuma referencia encontrada na base de conhecimento."
    contagem_topicos = {}
    for item in resultados_iniciais:
        topico = item.get("topico")
        if topico:
            contagem_topicos[topico] = contagem_topicos.get(topico, 0) + 1
    contexto_final = []
    fonte_origem = "Busca por similaridade (Fragmentos)"
    if not contagem_topicos:
        contexto_final = [item["descricao"] for item in resultados_iniciais[:5]]
        return "\n---\n".join(contexto_final), fonte_origem

    topico_vencedor = max(contagem_topicos, key=contagem_topicos.get)
    votos = contagem_topicos[topico_vencedor]

    if votos >= 3:
        print(f"🚀 Estratégia: Contexto Expandido para o tópico '{topico_vencedor}'")
        try:
            dados_expandidos = (
                client.table("knowledge_base")
                .select("descricao")
                .eq("topico", topico_vencedor)
                .execute()
            )

            dados = dados_expandidos.data[:MAX_CHUNCK]

            contexto_final = [row["descricao"] for row in dados]
            fonte_origem = f"Contexto Completo: {topico_vencedor}"

        except Exception as e:
            print(f"⚠️ Erro ao expandir contexto: {e}. Usando fallback.")
            contexto_final = [item["descricao"] for item in resultados_iniciais[:5]]
    else:
        print(
            f"🔍 Estratégia: Tópicos mistos (Vencedor '{topico_vencedor}' teve poucos votos)"
        )
        contexto_final = [item["descricao"] for item in resultados_iniciais[:5]]

    return "\n---\n".join(contexto_final), fonte_origem
