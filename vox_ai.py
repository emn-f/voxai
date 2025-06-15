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
    'hist_exibir': [], # List of dicts, e.g., {"role": "user", "parts": ["text"], "id": "unique_msg_id"}
    'primeira_vez': True,
    'tts_request_id': None # Stores the msg_id of the TTS audio currently requested to play
}
for key, value in default_session_values.items():
    if key not in st.session_state:
        st.session_state[key] = value

carregar_sidebar(SIDEBAR, st.session_state.git_version_str, st.session_state.kb_version_str)
st.session_state.key_api = configurar_api_gemini()

# --- Function to generate TTS bytes ---
def generate_tts_bytes(text_to_speak):
    try:
        tts = gTTS(text=text_to_speak, lang='pt-br')
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp.read()
    except Exception as e:
        st.error(f"Erro ao gerar áudio TTS: {e}")
        return None

# --- Display Past Chat History ---
if st.session_state.hist_exibir:
    for msg_index, msg_data in enumerate(st.session_state.hist_exibir):
        role = msg_data["role"]
        text = msg_data["parts"][0]
        msg_id = msg_data.get("id", f"hist_{msg_index}_{st.session_state.session_id}") # Ensure msg_id exists
        avatar = "🤖" if role == "model" else "🧑‍💻"

        with st.chat_message(role, avatar=avatar):
            st.markdown(text, unsafe_allow_html=True)
            if role == "model":
                tts_button_key = f"tts_btn_{msg_id}"
                if st.button("🔊", key=tts_button_key, help="Ouvir esta resposta"):
                    st.session_state.tts_request_id = msg_id
                    # No st.rerun() here, button click triggers it.

                # If this message's TTS was requested, generate and play it
                if st.session_state.tts_request_id == msg_id:
                    with st.spinner("Gerando áudio..."):
                        audio_bytes = generate_tts_bytes(text)
                        if audio_bytes:
                            st.audio(audio_bytes, format="audio/mp3", start_time=0)
                    st.session_state.tts_request_id = None # Reset after playing (or attempting)

# --- Handle Welcome Message ---
if st.session_state.key_api and st.session_state.primeira_vez:
    mensagem_boas_vindas = SAUDACAO
    welcome_msg_id = f"welcome_{st.session_state.session_id}"

    # Add to display history (will be rendered by the loop above on next rerun)
    # For immediate display with TTS, handle it specially here.

    with st.chat_message("assistant", avatar="🤖"):
        st.write_stream(stream_resposta(mensagem_boas_vindas))

        tts_welcome_btn_key = f"tts_btn_{welcome_msg_id}"
        if st.button("🔊", key=tts_welcome_btn_key, help="Ouvir esta saudação"):
            st.session_state.tts_request_id = welcome_msg_id
            # Rerun to trigger audio generation if not already visible due to other state changes
            # This specific rerun is to ensure the tts_request_id change is picked up immediately
            # for the welcome message if it's the first interaction.
            st.rerun()

        if st.session_state.tts_request_id == welcome_msg_id:
            with st.spinner("Gerando áudio..."):
                audio_bytes = generate_tts_bytes(mensagem_boas_vindas)
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3", start_time=0)
            st.session_state.tts_request_id = None # Reset

    # Add to histories after display and TTS interaction setup
    st.session_state.hist_exibir.append({"role": "model", "parts": [mensagem_boas_vindas], "id": welcome_msg_id})
    st.session_state.hist.append({"role": "assistant", "parts": [mensagem_boas_vindas]})
    st.session_state.primeira_vez = False

# --- Chat Input and Processing ---
if st.session_state.key_api:
    prompt = st.chat_input("Digite aqui...")
    if prompt:
        user_msg_id = f"user_{len(st.session_state.hist_exibir)}_{st.session_state.session_id}"
        st.session_state.hist.append({"role": "user", "parts": [prompt]})
        st.session_state.hist_exibir.append({"role": "user", "parts": [prompt], "id": user_msg_id})
        # No need to display user message here, history loop + rerun at end will do it.

        # Generate model's response
        # The response text will be streamed by gerar_resposta.
        # The TTS button and audio playback will be handled by the history loop after it's added.

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

        # Store the live response temporarily to add its TTS button *before* adding to history
        # This is tricky. The user wants the button immediately with the streamed response.
        # The `gerar_resposta` streams directly.
        # Let's ensure the live response also gets a chance to play audio immediately.

        # This is the live response bubble:
        with st.chat_message("assistant", avatar="🤖"):
            resposta = gerar_resposta(inicializar_chat_modelo(), prompt, info_adicional_str)

            # Now, for this live response, offer TTS
            model_msg_id = f"live_model_{len(st.session_state.hist_exibir)}_{st.session_state.session_id}"
            tts_live_btn_key = f"tts_btn_{model_msg_id}"
            if resposta and not resposta.startswith("Desculpe") and not resposta.startswith("Ocorreu um erro"):
                if st.button("🔊", key=tts_live_btn_key, help="Ouvir esta resposta"):
                    st.session_state.tts_request_id = model_msg_id
                    # Rerun to make the audio player appear for this live message
                    st.rerun()

            # Conditional audio playback for the live message
            if st.session_state.tts_request_id == model_msg_id:
                with st.spinner("Gerando áudio..."):
                    audio_bytes = generate_tts_bytes(resposta)
                    if audio_bytes:
                        st.audio(audio_bytes, format="audio/mp3", start_time=0)
                st.session_state.tts_request_id = None # Reset

        # Add to histories
        st.session_state.hist.append({"role": "model", "parts": [resposta]})
        # Use the same model_msg_id for hist_exibir so history loop can also handle it
        st.session_state.hist_exibir.append({"role": "model", "parts": [resposta], "id": model_msg_id})

        # Logging
        try:
            # ... (logging code remains the same) ...
            resposta_log = str(resposta)
            descricao_match_str = "N/A"
            if descricao_match and descricao_match != "N/A":
                descricao_match_str = str(descricao_match)
                descricao_match_str = unicodedata.normalize('NFKD', descricao_match_str).encode('ascii', 'ignore').decode('utf-8')
                descricao_match_str = re.sub(r'<[^>]+>', '', descricao_match_str)
            append_to_sheet(st.session_state.git_version_str, st.session_state.session_id, prompt, resposta_log, tema_match, descricao_match_str)

        except Exception as e:
            print(f"Falha ao registrar log na planilha: {e}")

        st.rerun() # Rerun to update the history display with user prompt & new model response
else:
    st.error("API Key não configurada corretamente. Verifique as configurações.")