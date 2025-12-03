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
from src.core.sheets_integration import append_to_sheet, log_exception
from src.utils import data_vox, git_version

configurar_pagina()
carregar_css()

base_vox_items, kb_version_str = data_vox()

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
            
        try:
            if "teste erro" in prompt.lower():
                raise Exception("Simulação de falha crítica para teste de LOG!")

            tema_match, descricao_match = semantica(prompt, base_vox_items) 
            
            info_adicional_contexto = ""
            if tema_match:
                info_adicional_contexto = descricao_match
            else:
                resultados = None
                descricao_match = "N/A" 

            with st.chat_message("assistant", avatar="🤖"):
                resposta = gerar_resposta(inicializar_chat_modelo(), prompt, info_adicional_contexto)
                
            st.session_state.hist.append({"role": "model", "parts": [resposta]})
            st.session_state.hist_exibir.append({"role": "model", "parts": [resposta]})

            try:
                if isinstance(resposta, list):
                    resposta_log = " ".join(resposta)
                else:
                    resposta_log = str(resposta)
                
                if descricao_match is None:
                    descricao_match_str = "N/A"
                else:
                    descricao_match_str = str(descricao_match)
                    descricao_match_str = unicodedata.normalize('NFKD', descricao_match_str).encode('ascii', 'ignore').decode('utf-8')
                    descricao_match_str = re.sub(r'<[^>]+>', '', descricao_match_str)
                    descricao_match_str = re.sub(r'\[.*?\]\(.*?\)', '', descricao_match_str)
                    descricao_match_str = re.sub(r'\*\*(.*?)\*\*', r'\1', descricao_match_str)
                
                append_to_sheet(st.session_state.git_version_str, st.session_state.session_id, prompt, resposta_log, tema_match, descricao_match_str)
            
            except Exception as e_log:
                print(f"⚠️ Falha silenciosa ao registrar log de conversa: {e_log}")

        except Exception as e:
            error_id = log_exception(st.session_state.git_version_str, st.session_state.session_id, e)
            
            st.error(f"""
            Putz, algo deu errado por aqui :/
            
            Por favor, reporte este erro para nossa equipe informando o código: **{error_id}**
            """, icon="🚫")
            
            print(f"❌ ERRO CRÍTICO (ID {error_id}): {e}")