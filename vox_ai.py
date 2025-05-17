import time
import random

import streamlit as st
import google.generativeai as genai
import os

from data.instrucoes import INSTRUCOES_VOX
from data.saudacao import SAUDACAO
from data.info import SOBRE
from src.persona import preparar_prompt
from src.utils import carregar_base_vox, buscar_por_tema

# Utilizando base de dados local
base_vox = carregar_base_vox("data/base.json") 

# Interface da página
st.set_page_config(
    page_title='Vox - Assistente de Apoio e Informação LGBTQIA+',
    page_icon='🗣️',
    layout="wide",  # Melhora a responsividade em dispositivos móveis
    initial_sidebar_state="collapsed"  # Sidebar começa fechada, útil para celular
)
st.title("Vox 🌈")
st.caption("Assistente de Apoio e Informação LGBTQIA+")

st.markdown(
    """
    <style>
    #vox-float-btn {
        position: fixed;
        top: 24px;
        left: 24px;
        z-index: 9999;
        background: #b5179e;
        color: #fff;
        border: none;
        border-radius: 50%;
        width: 48px;
        height: 48px;
        font-size: 2em;
        cursor: pointer;
        box-shadow: 0 2px 8px #0002;
    }
    #vox-float-menu {
        display: none;
        position: fixed;
        top: 80px;
        left: 24px;
        z-index: 9999;
        background: #fff;
        border-radius: 16px;
        box-shadow: 0 4px 24px 0 rgba(0,0,0,0.15);
        padding: 24px;
        min-width: 220px;
        max-width: 90vw;
    }
    #vox-float-menu.active {
        display: block;
    }
    </style>
    <div id="vox-float-menu">
        <h4>Sobre o Vox 🌈</h4>
        <p>O <b>Vox</b> é um assistente de apoio e informação <b>LGBTQIA+</b>.<br>
        Aqui você encontra acolhimento, informações e recursos confiáveis.</p>
        <h5>Equipe do Projeto</h5>
        <ul>
            <li><b>👑 Emanuel Arlan Sousa Silva Ferreira</b> — Engenharia de Software (Líder)</li>
            <li>Alicia Santos Silva Batista — Direito</li>
            <li>Brenda Moreira Lobo Pires — Direito</li>
            <li>Fernanda Carvalho do Souza — Biomedicina</li>
            <li>Kauã Araujo Santos — Engenharia de Software</li>
            <li>Lucca Rievers Pertigas — Engenharia de Software</li>
            <li>Marcio Claudio Ventura Ferreira — Engenharia de Software</li>
        </ul>
        <button onclick="document.getElementById('vox-float-menu').classList.remove('active')">Fechar</button>
    </div>
    <script>
    const btn = window.parent.document.getElementById('vox-float-btn');
    const menu = window.parent.document.getElementById('vox-float-menu');
    if(btn && menu){
        btn.onclick = () => menu.classList.toggle('active');
    }
    </script>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.markdown(SOBRE, unsafe_allow_html=True)
       
# Configuração da API (secreta no deploy)
api_key = st.secrets.get("GEMINI_API_KEY", "") or os.environ.get("GEMINI_API_KEY", "")
st.session_state.key_api = api_key
genai.configure(api_key=st.session_state.key_api)


# Histórico do modelo (com instruções) e histórico de exibição (sem)
if 'historico' not in st.session_state:
    st.session_state.historico = [{"role": "user", "parts": [INSTRUCOES_VOX]}]
if 'historico_exibir' not in st.session_state:
    st.session_state.historico_exibir = []

modelo = genai.GenerativeModel('gemini-2.0-flash')
chat = modelo.start_chat(history=st.session_state.historico)

# Só exibe o histórico real, sem o prompt do sistema
for msg in st.session_state.historico_exibir:
    if msg["role"] == "model":
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(msg["parts"][0])
    else:
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(msg["parts"][0])

# Primeira mensagem do assistente
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

    # Foco no campo de input do chat
    st.components.v1.html(
        """
        <script>
        // Aguarda o DOM carregar e tenta focar o campo de input do chat
        window.addEventListener('DOMContentLoaded', (event) => {
            const chatInputs = window.parent.document.querySelectorAll('textarea');
            if (chatInputs.length > 0) {
                chatInputs[chatInputs.length-1].focus();
            }
        });
        </script>
        """,
        height=0,
        scrolling=False,
    )

    if prompt:
        st.session_state.historico.append({"role": "user", "parts": [prompt]})
        st.session_state.historico_exibir.append({"role": "user", "parts": [prompt]})

        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        # Detecta tema no prompt
        temas_chave = ["acolhimento", "prep", "hiv", "retificação", "documento", "psicológico", "direitos"]
        tema_detectado = next((t for t in temas_chave if t in prompt.lower()), None)

        # Busca por informação complementar
        informacao_complementar = ""
        if tema_detectado:
            resultados = buscar_por_tema(tema_detectado, base_vox)
            if resultados:
                informacao_complementar = f"\n\n🔍 Informação baseada na pesquisa do projeto Vox: \n\n {resultados[0]}"

            
        chat = modelo.start_chat(history=st.session_state.historico)

        with st.chat_message('assistant', avatar="🤖"):
            msg_placeholder = st.empty()
            with st.spinner("🧠 Vox está pensando..."):
                try:
                    resposta = ''
                    prompt_final = preparar_prompt(prompt)
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
                    resposta += informacao_complementar
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
