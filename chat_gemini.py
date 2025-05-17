import time
import random
import streamlit as st
import google.generativeai as genai

# Config do site
st.set_page_config(page_title='Vox', page_icon='🏳️‍🌈')

# Título da página
st.title("Vox")
st.caption("Assistente de Apoio e Informação LGBTQIA+")

# Chave API no site
if 'key_api' not in st.session_state:
    key_api = st.sidebar.text_input('Insira sua chave API', type='password')
    if key_api.startswith('AI'):
        st.session_state.key_api = key_api
        genai.configure(api_key=st.session_state.key_api)
        st.sidebar.success('Tudo certo!', icon='✅')
        # KeyAPI: AIzaSyB3p67yshN1VsNaE5oZLXsd5M7mOCWILEA
    else:
        st.sidebar.warning('Informe a Chave API!', icon='⚠️')

# Histórico do chat
if 'historico' not in st.session_state:
    st.session_state.historico = []

# Modelo
modelo = genai.GenerativeModel('gemini-2.0-flash')

# Criação do chat
chat = modelo.start_chat(history=st.session_state.historico)

# Limpeza do chat
with st.sidebar:
    if st.button('Limpar chat', type='primary', use_container_width=True):
        st.session_state.historico = []
        st.rerun()

# Pegando mensagens do histórico
for msg in chat.history:
    if msg.role == 'model':
        role = 'assistant'
    else:
        role = msg.role
    with st.chat_message(role):
        st.markdown(msg.parts[0].text)

# Se tudo ok com a API...
if 'key_api' in st.session_state:
    prompt = st.chat_input('Hey!')
    if prompt:
        prompt = prompt.replace('\n', '\n')
        # Entrada de dados
        with st.chat_message('user'):
            st.markdown(prompt)
        # Mensagem do Gemini
        with st.chat_message('assistant'):
            msg_placeholder = st.empty()
            msg_placeholder.markdown('Thinking about this')
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
                st.exception(e)
            except Exception as e:
                st.exception(e)
            st.session_state.historico = chat.history