import streamlit as st
import time

def configurar_pagina():
    st.set_page_config(page_title='VoxAI', page_icon='🏳️‍🌈')
    st.markdown(
        """
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <h1 style="text-align: center">🏳️‍🌈 Vox AI</h1>
            <p style="text-align: center; color: gray;">Assistente de Apoio e Informação LGBTQIA+</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def carregar_css(path="static/css/style.css"):
    with open(path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def carregar_sidebar(sidebar_content, git_version, kb_version):
    with st.sidebar:
        if st.button("🧹 Limpar chat"):
            st.session_state.pop("hist", None)
            st.session_state.pop("hist_exibir", None)
        st.markdown(sidebar_content, unsafe_allow_html=True)
        
        # Exibe a versão do App e da Base de Conhecimento
        version_display = f"""
        <div style='color: #88888888; text-align: center; margin: auto; font-size: 0.9em;'>
            {git_version} | KB: v{kb_version}
        </div>
        """
        st.sidebar.markdown(version_display, unsafe_allow_html=True)

def stream_resposta(resposta):
    for letra in resposta:
        yield letra
        time.sleep(0.009)
