import streamlit as st
from sentence_transformers import SentenceTransformer, util
from src.config import MODELO_SEMANTICO_NOME, SEMANTICA_THRESHOLD

@st.cache_resource
def carregar_modelo():
    return SentenceTransformer(MODELO_SEMANTICO_NOME)

def semantica(prompt, base):
    modelo_semantico = carregar_modelo()
    
    temas = [item["tema"] for item in base]
    embeddings_base = modelo_semantico.encode(temas, convert_to_tensor=True)
    embedding_prompt = modelo_semantico.encode(prompt, convert_to_tensor=True)

    similaridades = util.cos_sim(embedding_prompt, embeddings_base)[0]
    indice_mais_proximo = similaridades.argmax().item()
    maior_score = similaridades[indice_mais_proximo].item()
    
    print(f"Prompt: {prompt}")
    print(f"Tema detectado: {temas[indice_mais_proximo]}")
    print(f"Score: {maior_score}")

    if maior_score > SEMANTICA_THRESHOLD: 
        return temas[indice_mais_proximo], base[indice_mais_proximo]["descricao"] 
    return None, None
