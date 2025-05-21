import startup_patch

import streamlit as st
import google.generativeai as genai
import os

from data.instrucoes import INSTRUCOES_VOX
from data.saudacao import SAUDACAO
from data.sobre import SOBRE
from src.ui import configurar_pagina, carregar_css, carregar_sidebar, stream_resposta
from src.chat import processar_prompt

from src.semantica import semantica
from src.persona import preparar_prompt
from src.utils import data_vox, BASE_PRINCIPAL_PATH, buscar_tema, git_version

base_vox = data_vox(BASE_PRINCIPAL_PATH)

# Configuração da página e título
configurar_pagina()
carregar_css()
carregar_sidebar(SOBRE, git_version())

# Obtém a chave da API Gemini de forma segura (primeiro dos segredos do Streamlit, depois das variáveis de ambiente)
api_key = st.secrets.get("GEMINI_API_KEY", "") or os.environ.get("GEMINI_API_KEY", "")

# Salva a chave no estado da sessão para uso em outros lugares
st.session_state.key_api = api_key

# Configura o SDK do Gemini com a chave obtida
genai.configure(api_key=st.session_state.key_api)

# Inicializa o histórico se não existir na sessão
if 'hist' not in st.session_state:
    st.session_state.hist = [{"role": "user", "parts": [INSTRUCOES_VOX]}]
if 'hist_exibir' not in st.session_state:
    st.session_state.hist_exibir = []


# Inicializa o modelo Gemini e o chat, usando o histórico salvo na sessão
modelo = genai.GenerativeModel('gemini-2.0-flash')
chat = modelo.start_chat(history=st.session_state.hist)

# Exibe o histórico do chat
for msg in st.session_state.hist_exibir:
    if msg["role"] == "model":
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(msg["parts"][0], unsafe_allow_html=True)
    else:
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(msg["parts"][0])

# Checa se a chave da API está disponível para continuar o fluxo do chat
if 'key_api' in st.session_state:
    # Mensagem de boas-vindas apenas na primeira vez
    if 'primeira_vez' not in st.session_state:
        mensagem_boas_vindas = SAUDACAO
        st.session_state.hist_exibir.append({"role": "model", "parts": [mensagem_boas_vindas]})
         
        # Animação de digitação para a mensagem de boas-vindas
        with st.chat_message("assistant", avatar="🤖"):
            msg_placeholder = st.empty()
            msg_placeholder.write_stream(stream_resposta(mensagem_boas_vindas))

    # Foco no input
    with open("static/focus_input.js") as f:
        js_code = f.read()
        st.components.v1.html(f"<script>{js_code}</script>", height=0, scrolling=False,)


    prompt = st.chat_input("Digite aqui...")

    # Processa o prompt do usuário
    if prompt:
        st.session_state.hist.append({"role": "user", "parts": [prompt]})
        st.session_state.hist_exibir.append({"role": "user", "parts": [prompt]})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        info_adicional= ""
        tema_match = semantica(prompt, base_vox)
        
        # Busca informações complementares com base no prompt
        if tema_match:
            resultados = buscar_tema(tema_match, base_vox)
            if resultados:
                info_adicional = f"\n\n🔍 **Informação baseada na pesquisa do projeto Vox:**\n\n{resultados[0]}"

        # Exibe a resposta do assistente com animação de digitação e tratamento de exceções
        with st.chat_message('assistant', avatar="🤖"):
            msg_placeholder = st.empty()
            with st.spinner("🧠 Thinking about it..."):
                try:
                    resposta = processar_prompt(prompt, chat, preparar_prompt, info_adicional)
                    msg_placeholder.write_stream(stream_resposta(resposta))
                except genai.types.generation_types.BlockedPromptException as e:
                    msg_placeholder.empty()
                    st.error("⚠️ Essa pergunta não pode ser respondida pelo Vox.")
                    st.exception(e)
                    resposta = "Desculpe, não posso responder isso."
                except Exception as e:
                    msg_placeholder.empty()
                    st.error("❌ Ocorreu um erro inesperado.")
                    st.exception(e)
                    resposta = "❌ Ocorreu um erro, tente novamente."

        # Adiciona a resposta ao histórico
        st.session_state.hist.append({"role": "model", "parts": [resposta]})
        st.session_state.hist_exibir.append({"role": "model", "parts": [resposta]})
