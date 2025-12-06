import streamlit as st
from sentence_transformers import SentenceTransformer
from src.config import MODELO_SEMANTICO_NOME, SEMANTICA_THRESHOLD
from src.core.database import buscar_referencias_db

@st.cache_resource
def carregar_modelo():
    return SentenceTransformer(MODELO_SEMANTICO_NOME)

def semantica(prompt):
    modelo_semantico = carregar_modelo()
    vetor_prompt = modelo_semantico.encode(prompt, convert_to_tensor=False).tolist()
    tema, descricao = buscar_referencias_db(vetor_prompt, threshold=SEMANTICA_THRESHOLD)
    
    if tema:
        print(f"Prompt: {prompt}")
        print(f"Tema encontrado no DB: {tema}")
        return tema, descricao
    return None, None