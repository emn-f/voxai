import streamlit as st
import uuid
import unicodedata
import re
import io
import base64
from gtts import gTTS

from data.prompts.ui_content import SAUDACAO, SIDEBAR
from src.app.ui import configurar_pagina, carregar_css, carregar_sidebar, stream_resposta
from src.core.genai import configurar_api_gemini, gerar_resposta, inicializar_chat_modelo
from src.core.semantica import semantica
from src.core.sheets_integration import append_to_sheet
from src.utils import BASE_PRINCIPAL_PATH, data_vox, buscar_tema, git_version

base_vox_items, kb_version_str = data_vox(BASE_PRINCIPAL_PATH)
configurar_pagina()
carregar_css()

# --- Session State Initialization ---
default_session_values = {
    'kb_version_str': kb_version_str,
    'git_version_str': git_version(),
    'session_id': str(uuid.uuid4()),
    'hist': [],
    'hist_exibir': [],
    'primeira_vez': True # To control welcome message
}
for key, value in default_session_values.items():
    if key not in st.session_state:
        st.session_state[key] = value

carregar_sidebar(SIDEBAR, st.session_state.git_version_str, st.session_state.kb_version_str)
st.session_state.key_api = configurar_api_gemini()

# --- Function to generate TTS and return HTML audio player ---
def get_tts_audio_html(text, unique_id):
    try:
        tts = gTTS(text=text, lang='pt-br')
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        audio_b64 = base64.b64encode(audio_fp.read()).decode()
        return f'<audio id="audio_{unique_id}" autoplay="true"><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mpeg">Seu navegador não suporta o elemento de áudio.</audio>'
    except Exception as e:
        st.error(f"Erro ao gerar áudio: {e}")
        st.warning("Verifique sua conexão com a internet ou se a mensagem não é muito longa.")
        return ""

# --- Display Past Chat History ---
# This loop iterates through messages already processed and added to hist_exibir.
# It should not handle the live streaming of a new response.
if st.session_state.hist_exibir:
    for msg_index, msg_data in enumerate(st.session_state.hist_exibir):
        role = msg_data["role"]
        text = msg_data["parts"][0]
        avatar = "🤖" if role == "model" else "🧑‍💻"
        with st.chat_message(role, avatar=avatar):
            st.markdown(text, unsafe_allow_html=True)
            if role == "model":
                # Use a unique key for each button in the history
                tts_hist_key = f"tts_hist_{msg_data.get('id', msg_index)}_{st.session_state.session_id}"
                if st.button("🔊", key=tts_hist_key, help="Ouvir esta resposta"):
                    audio_html = get_tts_audio_html(text, f"hist_{msg_data.get('id', msg_index)}")
                    if audio_html:
                        st.markdown(audio_html, unsafe_allow_html=True)

# --- Handle Welcome Message ---
if st.session_state.key_api and st.session_state.primeira_vez:
    mensagem_boas_vindas = SAUDACAO
    # Add to display history and main history (if model needs to be aware of it)
    welcome_msg_id = f"welcome_{st.session_state.session_id}"
    st.session_state.hist_exibir.append({"role": "model", "parts": [mensagem_boas_vindas], "id": welcome_msg_id})
    st.session_state.hist.append({"role": "assistant", "parts": [mensagem_boas_vindas]}) # Or "model" if genai expects that

    with st.chat_message("assistant", avatar="🤖"):
        # Stream the welcome message directly
        st.write_stream(stream_resposta(mensagem_boas_vindas))
        # Add TTS button for this welcome message
        if st.button("🔊", key=f"tts_{welcome_msg_id}", help="Ouvir esta saudação"):
            audio_html = get_tts_audio_html(mensagem_boas_vindas, welcome_msg_id)
            if audio_html:
                st.markdown(audio_html, unsafe_allow_html=True)
    st.session_state.primeira_vez = False # Ensure it only runs once per session


# --- Chat Input and Processing ---
if st.session_state.key_api:
    with open("static/js/focus_input.js") as f: # JS for input focus
        js_code = f.read()
        st.components.v1.html(f"<script>{js_code}</script>", height=0, scrolling=False)

    prompt = st.chat_input("Digite aqui...")

    if prompt:
        # Add user message to histories and display it immediately
        user_msg_id = f"user_{len(st.session_state.hist_exibir)}_{st.session_state.session_id}"
        st.session_state.hist.append({"role": "user", "parts": [prompt]})
        st.session_state.hist_exibir.append({"role": "user", "parts": [prompt], "id": user_msg_id})
        
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        # Semantic search
        info_adicional_str = ""
        tema_match, descricao_match = semantica(prompt, base_vox_items)
        if tema_match:
            resultados = buscar_tema(tema_match, base_vox_items)
            if resultados:
                 if isinstance(resultados, list): info_adicional_str = " ".join(map(str, resultados))
                 elif isinstance(resultados, dict): info_adicional_str = str(resultados)
                 else: info_adicional_str = str(resultados)
        else:
            descricao_match = "N/A"

        # Generate and display model's response (live)
        with st.chat_message("assistant", avatar="🤖"):
            # `gerar_resposta` from `genai.py` handles its own st.empty() and write_stream for the text
            resposta = gerar_resposta(inicializar_chat_modelo(), prompt, info_adicional_str)

            # After text is streamed and `resposta` contains the full string, add TTS button
            if resposta and not resposta.startswith("Desculpe") and not resposta.startswith("Ocorreu um erro"):
                model_msg_id = f"model_live_{len(st.session_state.hist_exibir)}_{st.session_state.session_id}"
                if st.button("🔊", key=f"tts_{model_msg_id}", help="Ouvir esta resposta"):
                    audio_html = get_tts_audio_html(resposta, model_msg_id)
                    if audio_html:
                        st.markdown(audio_html, unsafe_allow_html=True)

        # Add model's response to histories for future display by the history loop
        # The 'id' helps ensure keys are unique if we were to differentiate live vs historic display more.
        st.session_state.hist.append({"role": "model", "parts": [resposta]})
        st.session_state.hist_exibir.append({"role": "model", "parts": [resposta], "id": f"model_hist_{len(st.session_state.hist_exibir)}_{st.session_state.session_id}"})

        # Logging
        try:
            resposta_log = str(resposta)
            descricao_match_str = "N/A"
            if descricao_match and descricao_match != "N/A":
                descricao_match_str = str(descricao_match)
                descricao_match_str = unicodedata.normalize('NFKD', descricao_match_str).encode('ascii', 'ignore').decode('utf-8')
                descricao_match_str = re.sub(r'<[^>]+>', '', descricao_match_str)
            append_to_sheet(st.session_state.git_version_str, st.session_state.session_id, prompt, resposta_log, tema_match, descricao_match_str)
        except Exception as e:
            print(f"Falha ao registrar log na planilha: {e}")

        # No st.rerun() here. Streamlit's natural flow after button click (for TTS) or
        # when a new chat_input is submitted should handle rerenders.
        # The new messages are added to hist_exibir, so on the next natural rerun,
        # the history loop will display them. The live message is already displayed.
else:
    st.error("API Key não configurada corretamente. Verifique as configurações.")