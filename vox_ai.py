import time
import random

import streamlit as st
import google.generativeai as genai
import os

from data.instrucoes import INSTRUCOES_VOX
from data.saudacao import SAUDACAO
from data.sobre import SOBRE

from src.semantica import detectar_tema_semantico
from src.persona import preparar_prompt
from src.utils import carregar_base_vox, buscar_por_tema

base_vox = carregar_base_vox("data/base.json") 

st.set_page_config(
    page_title='Vox',
    page_icon='🏳️‍🌈',
    layout="wide", 
    initial_sidebar_state="collapsed"
)
st.title("Vox 🌈")
st.caption("Assistente de Apoio e Informação LGBTQIA+")


with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(SOBRE, unsafe_allow_html=True)
       
api_key = st.secrets.get("GEMINI_API_KEY", "") or os.environ.get("GEMINI_API_KEY", "")
st.session_state.key_api = api_key
genai.configure(api_key=st.session_state.key_api)


if 'historico' not in st.session_state:
    st.session_state.historico = [{"role": "user", "parts": [INSTRUCOES_VOX]}]
if 'historico_exibir' not in st.session_state:
    st.session_state.historico_exibir = []

modelo = genai.GenerativeModel('gemini-2.0-flash')
chat = modelo.start_chat(history=st.session_state.historico)

for msg in st.session_state.historico_exibir:
    if msg["role"] == "model":
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(msg["parts"][0])
    else:
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(msg["parts"][0])

if 'key_api' in st.session_state:
    if 'primeira_vez' not in st.session_state:
        st.session_state.primeira_vez = True
        mensagem_boas_vindas = SAUDACAO
        st.session_state.historico_exibir.append({"role": "model", "parts": [mensagem_boas_vindas]})
        
        with st.chat_message("assistant", avatar="🤖"):
            msg_placeholder = st.empty()
            resposta = ""
            for letra in mensagem_boas_vindas:
                resposta += letra
                msg_placeholder.markdown(resposta + "_")
                time.sleep(0.01)
            msg_placeholder.markdown(resposta)

    prompt = st.chat_input('Digite aqui...')

    with open("static/focus_input.js") as f:
        js_code = f.read()
    st.components.v1.html(
        f"<script>{js_code}</script>",
        height=0,
        scrolling=False,
    )

    if prompt:
        st.session_state.historico.append({"role": "user", "parts": [prompt]})
        st.session_state.historico_exibir.append({"role": "user", "parts": [prompt]})

        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        informacao_complementar = ""
        tema_detectado = detectar_tema_semantico(prompt, base_vox)

        if tema_detectado:
            resultados = buscar_por_tema(tema_detectado, base_vox)
            if resultados:
                informacao_complementar = f"\n\n🔍 **Informação baseada na pesquisa do projeto Vox:**\n\n{resultados[0]}"
       
        with st.chat_message('assistant', avatar="🤖"):
            msg_placeholder = st.empty()
            with st.spinner("🧠 Thinking about it..."):
                try:
                    resposta = ''
                    prompt_final = preparar_prompt(prompt)
                    for chunk in chat.send_message(prompt_final, stream=True):
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
                    resposta_completa = resposta + informacao_complementar
                    msg_placeholder.markdown(resposta_completa)

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
