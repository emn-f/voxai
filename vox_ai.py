import startup_patch

import time
import random

import streamlit as st
import google.generativeai as genai
import os

from data.instrucoes import INSTRUCOES_VOX
from data.saudacao import SAUDACAO
from data.sobre import SOBRE

from src.semantica import semantica
from src.persona import preparar_prompt
from src.utils import data_vox, buscar_tema, git_version

base_vox = data_vox("data/base.json") 

# Configuração da página e título
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
    st.sidebar.markdown(f"<span style='color: #88888888;'>{git_version()}</span>", unsafe_allow_html=True)

# Obtém a chave da API Gemini de forma segura (primeiro dos segredos do Streamlit, depois das variáveis de ambiente)
api_key = st.secrets.get("GEMINI_API_KEY", "") or os.environ.get("GEMINI_API_KEY", "")

# Salva a chave no estado da sessão para uso em outras partes do app
st.session_state.key_api = api_key

# Configura o SDK do Gemini com a chave obtida
genai.configure(api_key=st.session_state.key_api)


# Inicializa o histórico se não existir na sessão
if 'historico' not in st.session_state:
    st.session_state.historico = [{"role": "user", "parts": [INSTRUCOES_VOX]}]
if 'historico_exibir' not in st.session_state:
    st.session_state.historico_exibir = []

# Inicializa o modelo Gemini e o chat, usando o histórico salvo na sessão
modelo = genai.GenerativeModel('gemini-2.0-flash')
chat = modelo.start_chat(history=st.session_state.historico)

for msg in st.session_state.historico_exibir:
    if msg["role"] == "model":
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(msg["parts"][0])
    else:
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(msg["parts"][0])
            
# Checa se a chave da API está disponível para continuar o fluxo do chat
if 'key_api' in st.session_state:
    if 'primeira_vez' not in st.session_state:
        st.session_state.primeira_vez = True
        mensagem_boas_vindas = SAUDACAO
        st.session_state.historico_exibir.append({"role": "model", "parts": [mensagem_boas_vindas]})
         
         # Animação de digitação para a mensagem de boas-vindas
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
        tema_detectado = semantica(prompt, base_vox)
        
        # Busca informações complementares com base no tema detectado
        if tema_detectado:
            resultados = buscar_tema(tema_detectado, base_vox)
            if resultados:
                informacao_complementar = f"\n\n🔍 **Informação baseada na pesquisa do projeto Vox:**\n\n{resultados[0]}"
       
        # Exibe a resposta do assistente com animação de digitação e tratamento de exceções
        with st.chat_message('assistant', avatar="🤖"):
            msg_placeholder = st.empty()
            with st.spinner("🧠 Thinking about it..."):
                try:
                    resposta = ''
                    prompt_final = preparar_prompt(prompt)
                    # Recebe a resposta do modelo Gemini em streaming (chunk a chunk)
                    for chunk in chat.send_message(prompt_final, stream=True):
                        contagem_palavras = 0
                        num_aleatorio = random.randint(5, 10)
                        # Animação: exibe a resposta em blocos de palavras simulando digitação
                        for palavra in chunk.text:
                            resposta += palavra
                            contagem_palavras += 1
                            if contagem_palavras == num_aleatorio:
                                time.sleep(0.05)
                                msg_placeholder.markdown(resposta + '_')
                                contagem_palavras = 0
                                num_aleatorio = random.randint(5, 10)
                    # Adiciona informação complementar (se houver) ao final da resposta
                    resposta_completa = resposta + informacao_complementar
                    msg_placeholder.markdown(resposta_completa)
                # Trata prompts bloqueados pela API Gemini
                except genai.types.generation_types.BlockedPromptException as e:
                    msg_placeholder.empty()
                    st.error("⚠️ Essa pergunta não pode ser respondida pelo Vox.")
                    st.exception(e)
                    resposta = "Desculpe, não posso responder isso."
                # Trata outros erros inesperados durante a geração da resposta
                except Exception as e:
                    msg_placeholder.empty()
                    st.error("❌ Ocorreu um erro inesperado.")
                    st.exception(e)
                    resposta = "Ocorreu um erro, tente novamente."
                    
        # Adiciona a resposta do assistente ao histórico
        st.session_state.historico.append({"role": "model", "parts": [resposta]})
        st.session_state.historico_exibir.append({"role": "model", "parts": [resposta]})
