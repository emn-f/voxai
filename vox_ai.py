import streamlit as st
import uuid
import unicodedata
import re
import io
import base64

from gtts import gTTS

# Assuming these paths are correct relative to where the script is run
from data.prompts.ui_content import SAUDACAO, SIDEBAR
from src.app.ui import configurar_pagina, carregar_css, carregar_sidebar, stream_resposta
from src.core.genai import configurar_api_gemini, inicializar_chat_modelo, gerar_resposta
from src.core.semantica import semantica
from src.core.sheets_integration import append_to_sheet
from src.utils import BASE_PRINCIPAL_PATH, data_vox, buscar_tema, git_version

# --- Initializations ---
base_vox_items, kb_version_str = data_vox(BASE_PRINCIPAL_PATH)
    
configurar_pagina()
carregar_css()

# --- Session State Management ---
if 'kb_version_str' not in st.session_state:
    st.session_state.kb_version_str = kb_version_str
if 'git_version_str' not in st.session_state:
    st.session_state.git_version_str = git_version()
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# hist_exibir is for UI display. `st.session_state.hist` (for GenAI model context) is managed by genai.py
if "hist_exibir" not in st.session_state:
    st.session_state.hist_exibir = []

carregar_sidebar(SIDEBAR, st.session_state.git_version_str, st.session_state.kb_version_str)

# --- API and Chat Model Initialization ---
if 'gemini_api_configured' not in st.session_state or not st.session_state.gemini_api_configured:
    configurar_api_gemini() # Sets st.session_state.gemini_api_configured

if st.session_state.get('gemini_api_configured', False):
    inicializar_chat_modelo() # Ensures chat_session and hist are set up in st.session_state
else:
    st.error("API Key do Gemini não configurada ou inválida. Verifique as configurações e recarregue a página.")
    st.stop()

# --- Handle Welcome Message (SAUDACAO) for UI ---
if 'primeira_vez_exibida' not in st.session_state:
    # SAUDACAO is the first message shown to the user in the UI
    # It's not added to st.session_state.hist (model's direct history) unless desired
    # The model's history (st.session_state.hist) starts with INSTRUCOES and its own opening via genai.py
    if not any(m["role"] == "model" and m["parts"][0] == SAUDACAO for m in st.session_state.hist_exibir):
        st.session_state.hist_exibir.append({"role": "model", "parts": [SAUDACAO]})
    st.session_state.primeira_vez_exibida = True

# --- Display Chat History (from hist_exibir) ---
for msg_index, msg in enumerate(st.session_state.hist_exibir):
    avatar = "🤖" if msg["role"] == "model" else "🧑‍💻"
    with st.chat_message(msg["role"], avatar=avatar):
        message_text = msg["parts"][0]
        
        is_welcome_message_first_stream = (
            msg["role"] == "model"
            and message_text == SAUDACAO
            and f"welcome_SAUDACAO_streamed_{st.session_state.session_id}" not in st.session_state
        )

        if is_welcome_message_first_stream:
            msg_placeholder = st.empty()
            msg_placeholder.write_stream(stream_resposta(message_text))
            st.session_state[f"welcome_SAUDACAO_streamed_{st.session_state.session_id}"] = True
        else:
            st.markdown(message_text, unsafe_allow_html=True)

        if msg["role"] == "model":
            tts_button_key = f"tts_hist_{msg_index}_{st.session_state.session_id}"
            # Add help text for accessibility, aria-label will be reviewed in next step
            if st.button("🔊", key=tts_button_key, help="Ouvir esta resposta da assistente"):
                try:
                    tts = gTTS(text=message_text, lang='pt-br')
                    audio_fp = io.BytesIO()
                    tts.write_to_fp(audio_fp)
                    audio_fp.seek(0)
                    audio_b64 = base64.b64encode(audio_fp.read()).decode()
                    audio_player_id = f"audio_player_{msg_index}_{st.session_state.session_id}"
                    audio_html = f'<audio id="{audio_player_id}" autoplay="true"><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mpeg">Seu navegador não suporta o elemento de áudio.</audio>'
                    st.markdown(audio_html, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Erro ao gerar áudio: {e}")
                    st.warning("Verifique sua conexão com a internet (TTS) e se a mensagem não é muito longa.")

# --- Chat Input and Processing ---
with open("static/js/focus_input.js") as f: # JS for input focus
    js_code = f.read()
    st.components.v1.html(f"<script>{js_code}</script>", height=0, scrolling=False)

prompt = st.chat_input("Digite aqui...")

if prompt:
    # Add user's prompt to UI history and model's history
    st.session_state.hist_exibir.append({"role": "user", "parts": [prompt]})
    st.session_state.hist.append({"role": "user", "parts": [prompt]}) # Add to model's history via session_state.hist

    # Semantic search (if any)
    tema_match, descricao_match = semantica(prompt, base_vox_items)
    resultados = buscar_tema(tema_match, base_vox_items) if tema_match else None
    if not tema_match: descricao_match = "N/A"

    # Generate model's response using the refactored genai.py function
    if 'chat_session' in st.session_state: # Ensure chat session is ready
        resposta_gerada = gerar_resposta(prompt, resultados) # No chat_model passed!

        # Add model's response to UI history and model's history
        st.session_state.hist_exibir.append({"role": "model", "parts": [resposta_gerada]})
        st.session_state.hist.append({"role": "model", "parts": [resposta_gerada]}) # Add to model's history

        # Log the interaction
        try:
            resposta_log = " ".join(resposta_gerada) if isinstance(resposta_gerada, list) else str(resposta_gerada)
            descricao_match_str = "N/A"
            if descricao_match and descricao_match != "N/A":
                # Basic normalization, ensure it's robust for various inputs
                descricao_match_str = unicodedata.normalize('NFKD', str(descricao_match)).encode('ascii', 'ignore').decode('utf-8', 'ignore')
                descricao_match_str = re.sub(r'<[^>]+>', '', descricao_match_str)
            append_to_sheet(st.session_state.git_version_str, st.session_state.session_id, prompt, resposta_log, tema_match, descricao_match_str)
        except Exception as e:
            st.warning(f"Falha ao registrar log na planilha: {e}")
    
        st.rerun() # Rerun to display new messages and TTS buttons correctly
    else:
        st.error("Sessão de chat não está ativa. Não foi possível gerar resposta. Por favor, recarregue.")