import time
import random
import streamlit as st
import google.generativeai as genai

# Interface da página
st.set_page_config(page_title='Vox', page_icon='🏳️‍🌈')
st.title("Vox")
st.caption("Assistente de Apoio e Informação LGBTQIA+")

# Configurações do funcionamento básico do Vox
st.session_state.key_api = 'GEMINI_API_KEY'

if 'historico' not in st.session_state:
    st.session_state.historico = []

modelo = genai.GenerativeModel('gemini-2.0-flash')

chat = modelo.start_chat(history=st.session_state.historico)

for msg in chat.history:
    if msg.role == 'model':
        role = 'assistant'
    else:
        role = msg.role
    with st.chat_message(role):
        st.markdown(msg.parts[0].text)

if 'key_api' in st.session_state:
    if 'primeira_vez' not in st.session_state:
        st.session_state.primeira_vez = True
        with st.chat_message('assistant', avatar="🤖"):
            st.markdown("""
            Hey! Eu sou Vox - Assistente de Apoio e Informação LGBTQIA+.
            Como posso ajudar você hoje?

            Você pode me perguntar sobre:
            - Informações sobre a comunidade LGBTQIA+
            - Recursos de apoio
            - Dúvidas gerais
            """)

    prompt = st.chat_input('Digite aqui...')
    if prompt:
        prompt = prompt.replace('\n', '\n')
        # Entrada de dados
        with st.chat_message('user', avatar="👤"):
            st.markdown(prompt)
        # Mensagem do Gemini
        with st.chat_message('assistant', avatar="🤖"):
            msg_placeholder = st.empty()
            with st.spinner("🧠 Vox está pensando..."):
                # Verificando erro de entrada
                try:
                    # Resposta do Gemini
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
                    msg_placeholder.empty()  # esconde o spinner
                    st.error("⚠️ Essa pergunta não pode ser respondida pelo Vox.")
                    st.exception(e)
                except Exception as e:
                    msg_placeholder.empty()
                    st.error("❌ Ocorreu um erro inesperado.")
                    st.exception(e)
                st.session_state.historico = chat.history
