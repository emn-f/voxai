import streamlit as st
import google.generativeai as genai
import os
from src.config import SEMANTICA_THRESHOLD
from src.core.database import buscar_referencias_db

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
            model="models/text-embedding-004",
            content=prompt,
            task_type="retrieval_query" 
        )
        vetor_prompt = result['embedding']
        
        tema, descricao = buscar_referencias_db(vetor_prompt, threshold=SEMANTICA_THRESHOLD)
        
        if tema:
            return tema, descricao
            
        return None, None

    except Exception as e:
        print(f"Erro na geração do embedding semântico: {e}")
        return None, None