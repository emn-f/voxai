import streamlit as st
import time

def configurar_pagina():
    st.set_page_config(page_title='VoxAI', page_icon='🌈')
    st.markdown(
        """
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <h1 style="text-align: center;">Vox AI 🌈</h1>
            <p style="text-align: center; color: gray;">Assistente de Apoio e Informação LGBTQIA+</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def carregar_css(path="static/style.css"):
    with open(path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def carregar_sidebar(sobre, git_version, rodape):
    with st.sidebar:
        if st.button("🧹 Limpar chat"):
            st.session_state.pop("hist", None)
            st.session_state.pop("hist_exibir", None)
        st.markdown(sobre, unsafe_allow_html=True)
        st.sidebar.markdown(f"<span style='color: #88888888;'>{git_version}</span>", unsafe_allow_html=True)
        st.markdown(rodape, unsafe_allow_html=True)
        
def stream_resposta(resposta):
    for letra in resposta:
        yield letra
        time.sleep(0.009)