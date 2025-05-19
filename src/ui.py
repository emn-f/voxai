# src/ui.py
import streamlit as st
import time

def configurar_pagina():
    st.set_page_config(
        page_title='VoxAI',
        page_icon='🏳️‍🌈',
    )
    st.title("Vox AI🌈")
    st.caption("Assistente de Apoio e Informação LGBTQIA+")

def carregar_css(path="static/style.css"):
    with open(path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def carregar_sidebar(sobre, git_version):
    with st.sidebar:
        st.markdown(sobre, unsafe_allow_html=True)
        st.sidebar.markdown(f"<span style='color: #88888888;'>{git_version}</span>", unsafe_allow_html=True)

def animar_texto(texto, placeholder, delay=0.03, por_palavra=True):
    resposta = ""
    if por_palavra:
        palavras = texto.split()
        for i, palavra in enumerate(palavras):
            resposta += palavra + " "
            placeholder.markdown(resposta + "_")
            time.sleep(delay)
        placeholder.markdown(resposta.strip())
    else:
        for letra in texto:
            resposta += letra
            placeholder.markdown(resposta + "_")
            time.sleep(delay)
        placeholder.markdown(resposta)