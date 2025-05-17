import time
import random

import streamlit as st
import google.generativeai as genai

from instrucoes import INSTRUCOES_VOX


# Interface da página
st.set_page_config(page_title='Vox', page_icon='🏳️‍🌈')
st.title("Vox")
st.caption("Assistente de Apoio e Informação LGBTQIA+")

# Configuração da API (secreta no deploy)
st.session_state.key_api = 'GEMINI_API_KEY'
genai.configure(api_key=st.session_state.key_api)

# Checa se a chave da API está presente e válida
api_key = st.secrets.get("GEMINI_API_KEY", "") or os.environ.get("GEMINI_API_KEY", "")
api_online = api_key.startswith("AI")  # Gemini API keys geralmente começam com "AI"

# Status API
if api_online:
    st.success("🟢 Chave API do Gemini AI Online")
else:
    st.error("🔴 Chave não localizada. Entre em contato com o administrador")

# Histórico do modelo (com instruções) e histórico de exibição (sem)
if 'historico' not in st.session_state:
    st.session_state.historico = [{"role": "user", "parts": [INSTRUCOES_VOX]}]
if 'historico_exibir' not in st.session_state:
    st.session_state.historico_exibir = []

modelo = genai.GenerativeModel('gemini-2.0-flash')
chat = modelo.start_chat(history=st.session_state.historico)

# Só exibe o histórico real, sem o prompt do sistema
for msg in st.session_state.historico_exibir:
    with st.chat_message("assistant" if msg["role"] == "model" else "user"):
        st.markdown(msg["parts"][0])

# Primeira mensagem do assistente
if 'key_api' in st.session_state:
    if 'primeira_vez' not in st.session_state:
        st.session_state.primeira_vez = True
        mensagem_boas_vindas = """
        Hey! Eu sou Vox - Assistente de Apoio e Informação LGBTQIA+.
        Como posso ajudar você hoje?

        Você pode me perguntar sobre:
        - Informações sobre a comunidade LGBTQIA+
        - Recursos de apoio
        - Dúvidas gerais
        """
        st.session_state.historico_exibir.append({"role": "model", "parts": [mensagem_boas_vindas]})
        with st.chat_message("assistant", avatar="🤖"):
          st.markdown(mensagem_boas_vindas)
    if api_online:
        prompt = st.chat_input('Digite aqui...')
    else:
        st.chat_input('API OFFLINE: verifique a configuração da chave Gemini.', disabled=True)
        prompt = None

    prompt = st.chat_input('Digite aqui...')
    if prompt:
        st.session_state.historico.append({"role": "user", "parts": [prompt]})
        st.session_state.historico_exibir.append({"role": "user", "parts": [prompt]})

        chat = modelo.start_chat(history=st.session_state.historico)

        with st.chat_message('assistant', avatar="🤖"):
            msg_placeholder = st.empty()
            with st.spinner("🧠 Vox está pensando..."):
                try:
                    resposta = ''
                    for chunk in chat.send_message(prompt, stream=True):
                        contagem_palavras = 0
                        num_aleatorio = random.randint(5, 10)
                        for palavra in chunk.text:
                            resposta += palavra
                            contagem_palavras += 1
                            if contagem_palavras == num_aleatorio:
                                time.sleep(0.05)
                                msg_placeholder.markdown(resposta + '_')
                                contagem_palavras = 0
                                num_aleatorio = random.randint(5, 10)
                    msg_placeholder.markdown(resposta)
                except genai.types.generation_types.BlockedPromptException as e:
                    msg_placeholder.empty()
                    st.error("⚠️ Essa pergunta não pode ser respondida pelo Vox.")
                    st.exception(e)
                    resposta = "Desculpe, não posso responder isso."
                except Exception as e:
                    msg_placeholder.empty()
                    st.error("❌ Ocorreu um erro inesperado.")
                    st.exception(e)
                    resposta = "Ocorreu um erro, tente novamente."

        st.session_state.historico.append({"role": "model", "parts": [resposta]})
        st.session_state.historico_exibir.append({"role": "model", "parts": [resposta]})
