import os

import google.generativeai as genai
import streamlit as st

from src.config import MODELO_SEMANTICO_NOME
from src.core.database import recuperar_contexto_inteligente


def _configurar_api():
    api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
    else:
        print("GEMINI_API_KEY não encontrada nas variáveis de ambiente.")


def semantica(prompt):
    _configurar_api()
    try:
        result = genai.embed_content(
            model=MODELO_SEMANTICO_NOME, content=prompt, task_type="retrieval_query"
        )
        vetor_prompt = result["embedding"]

        texto_contexto, fonte_identificaadora, lista_ids = (
            recuperar_contexto_inteligente(vetor_prompt)
        )

        if texto_contexto:
            return fonte_identificaadora, texto_contexto, lista_ids

        return None, None, None

    except Exception as e:
        print(f"Erro na geração do embedding semântico: {e}")
        return None, None, None
