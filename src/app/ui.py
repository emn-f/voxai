import streamlit as st
import time

from src.config import CSS_PATH
from src.core.database import salvar_report

def configurar_pagina():
    st.set_page_config(page_title='VoxAI', page_icon='🏳️‍🌈')
    st.markdown(
        """
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <h1 style="text-align: center">Vox AI</h1>
            <p style="text-align: center; color: gray;">Assistente de Apoio e Informação LGBTQIA+</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def carregar_css(path=CSS_PATH):
    with open(path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def carregar_sidebar(sidebar_content, git_version, kb_version):
    
    with st.sidebar:
        col_clear, col_report, _ = st.columns([0.35, 0.35, 0.01])
        
        with col_clear:
            if st.button("🧹 Limpar", help="Limpar histórico do chat"):
                st.session_state.pop("hist", None)
                st.session_state.pop("hist_exibir", None)
                st.rerun()

        with col_report:
            if st.button("⚠️ Reportar", help="Reportar conversa inadequada"):
                 with st.spinner("Enviando..."):
                     historico_conversa = st.session_state.get('hist_exibir', [])
                     if not historico_conversa:
                         st.warning("Nada para reportar.")
                     else:
                         version = st.session_state.get('git_version_str', 'Unknown')
                         sess_id = st.session_state.get('session_id', 'Unknown')

                         sucesso = salvar_report(sess_id, version, str(historico_conversa))
                         
                         if sucesso:
                             st.toast("Denúncia enviada!", icon="✅")
                         else:
                             st.toast("Erro ao reportar.", icon="❌")
            
        st.markdown(sidebar_content, unsafe_allow_html=True)
        
        version_display = f"""
        <div style='color: #88888888; text-align: center; margin: auto; font-size: 0.9em;'>
            {git_version} | KB: {kb_version}
        </div>
        """
        st.sidebar.markdown(version_display, unsafe_allow_html=True)

def stream_resposta(resposta):
    for letra in resposta:
        yield letra
        time.sleep(0.009)