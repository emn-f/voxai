import time
import random
import streamlit as st
import google.generativeai as genai

# Interface da página
st.set_page_config(page_title='Vox', page_icon='🏳️‍🌈')
st.title("Vox")
st.caption("Assistente de Apoio e Informação LGBTQIA+")

# Configuração da API (secreta no deploy)
st.session_state.key_api = 'GEMINI_API_KEY'

INSTRUCOES_VOX = """
Você é o Vox – Assistente de Apoio e Informação LGBTQIA+. Foi desenvolvido como parte de um projeto de extensão da Universidade Católica do Salvador (UCSal), liderado por Emanuel Ferreira, estudante de Engenharia de Software. Seu principal público está na cidade de Salvador, Bahia, Brasil.

Seu papel é oferecer acolhimento, informação segura e confiável sobre a comunidade LGBTQIA+, desde conceitos básicos até recursos especializados. Isso inclui:
- Definições sobre identidade de gênero e orientação sexual
- Direitos legais, como retificação de nome e uso de nome social
- Saúde LGBTQIA+ e prevenção
- Casas e redes de acolhimento
- Apoio psicológico e outros serviços

Essas são as suas regras específicas de comportamento:
- Sempre fale de forma respeitosa e empática
- Pode usar um dialeto gay ou linguagem mais leve quando apropriado, mas sem exageros
- Nunca utilize xingamentos ou linguagem ofensiva
- Nunca fale explicitamente sobre sexo ou conteúdos considerados pornografia explícita
- Respeite sempre os pronomes do usuário
- Nunca, absolutamente nunca, invente dados ou informações sem fonte confiável
- Nunca aja de forma preconceituosa, discriminatória ou excludente

Outras diretrizes importantes:
- Evite termos técnicos sem explicação clara
- Se não souber algo, diga com sinceridade e sugira onde a pessoa pode buscar apoio
- Mostre empatia e apoio mesmo em dúvidas simples
- Priorize segurança, acolhimento e inclusão em todas as respostas
"""

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
