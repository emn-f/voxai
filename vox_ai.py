import streamlit as st

import startup_patch
import os
import uuid
import unicodedata
import re

from data.prompts.ui_content import SAUDACAO, SIDEBAR

from src.app.ui import configurar_pagina, carregar_css, carregar_sidebar, stream_resposta
from src.core.genai import configurar_api_gemini, gerar_resposta, inicializar_chat_modelo
from src.core.semantica import semantica
from src.core.sheets_integration import append_to_sheet
from src.utils import BASE_PRINCIPAL_PATH, data_vox, buscar_tema, git_version

base_vox_items, kb_version_str = data_vox(BASE_PRINCIPAL_PATH)
    
configurar_pagina()
carregar_css()

if 'kb_version_str' not in st.session_state:
    st.session_state.kb_version_str = kb_version_str

if 'git_version_str' not in st.session_state:
    st.session_state.git_version_str = git_version()

if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    

carregar_sidebar(SIDEBAR, st.session_state.git_version_str, st.session_state.kb_version_str)

st.session_state.key_api = configurar_api_gemini()

inicializar_chat_modelo()

for msg in st.session_state.hist_exibir:
    if msg["role"] == "model":
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(msg["parts"][0], unsafe_allow_html=True)
    else:
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(msg["parts"][0])

if 'key_api' in st.session_state:
    if 'primeira_vez' not in st.session_state:
        mensagem_boas_vindas = SAUDACAO
        st.session_state.hist_exibir.append({"role": "model", "parts": [mensagem_boas_vindas]})
        st.session_state.primeira_vez = True

        with st.chat_message("assistant", avatar="🤖"):
            msg_placeholder = st.empty()
            msg_placeholder.write_stream(stream_resposta(mensagem_boas_vindas))

    prompt = st.chat_input("Digite aqui...")

    if prompt:
        st.session_state.prompt = prompt
        st.session_state.hist.append({"role": "user", "parts": [prompt]})
        st.session_state.hist_exibir.append({"role": "user", "parts": [prompt]})
        
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)
        info_adicional= ""
        tema_match = semantica(prompt, base_vox_items)

        tema_match, descricao_match = semantica(prompt, base_vox_items) 
        
        if tema_match:
            resultados = buscar_tema(tema_match, base_vox_items)
        else:
            resultados = None
            descricao_match = "N/A" 

        with st.chat_message("assistant", avatar="🤖"):
            resposta = gerar_resposta(inicializar_chat_modelo(), prompt, resultados)
            
        try:
            if isinstance(resposta, list):
                resposta = " ".join(resposta)
            else:
                resposta = str(resposta)
            
            if descricao_match is None:
                descricao_match_str = "N/A"
            else:
                descricao_match_str = str(descricao_match)

                descricao_match_str = unicodedata.normalize('NFKD', descricao_match_str).encode('ascii', 'ignore').decode('utf-8')

                descricao_match_str = re.sub(r'<[^>]+>', '', descricao_match_str)
                descricao_match_str = re.sub(r'\[.*?\]\(.*?\)', '', descricao_match_str)
                descricao_match_str = re.sub(r'\*\*(.*?)\*\*', r'\1', descricao_match_str)
                descricao_match_str = re.sub(r'__(.*?)__', r'\1', descricao_match_str)
                descricao_match_str = re.sub(r'\*(.*?)\*', r'\1', descricao_match_str)
                descricao_match_str = re.sub(r'_(.*?)_', r'\1', descricao_match_str)
            append_to_sheet(st.session_state.git_version_str, st.session_state.session_id, prompt, resposta, tema_match, descricao_match_str)
        
        except Exception as e:
            print(f"Falha ao registrar log na planilha: {e}")
    
        st.session_state.hist.append({"role": "model", "parts": [resposta]})
        st.session_state.hist_exibir.append({"role": "model", "parts": [resposta]})