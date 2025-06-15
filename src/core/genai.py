import streamlit as st
import google.generativeai as genai
import os
from src.app.ui import stream_resposta
from data.prompts.system_prompt import INSTRUCOES

def configurar_api_gemini():
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "") or os.environ.get("GEMINI_API_KEY", "")
        if not api_key:
            st.error("Chave da API não localizada. Verifique as configurações do Streamlit ou as variáveis de ambiente.")
            st.stop()
        else:
            genai.configure(api_key=api_key)
        return api_key
    except Exception as e:
        st.error(f"Erro ao configurar a API do Gemini: {e}")
        st.stop()
        return None

def inicializar_chat_modelo():
    if 'hist' not in st.session_state:
        st.session_state.hist = [{"role": "user", "parts": [INSTRUCOES]}]

    modelo = genai.GenerativeModel('gemini-2.0-flash') # Matching the first read_files output
    chat = modelo.start_chat(history=st.session_state.hist)
    return chat

def gerar_resposta(chat, prompt, info_adicional):
    msg_placeholder = st.empty() # msg_placeholder was used in the original
    with st.spinner("🧠 Thinking about it..."): # Original spinner text
        try:
            full_prompt_for_model = prompt
            if info_adicional: # Original check was simpler
                full_prompt_for_model = f"{prompt}\n\nConsidere a seguinte informação complementar para sua resposta: {info_adicional}"

            resposta = '' # Original variable name
            # Stream the response directly from the chat object
            # The original code directly built the 'resposta' string from chunks.
            for chunk in chat.send_message(full_prompt_for_model, stream=True):
                resposta += chunk.text

            # Then, it used stream_resposta to display it via the placeholder
            msg_placeholder.write_stream(stream_resposta(resposta))
            return resposta # Returns the full 'resposta' string
        except genai.types.generation_types.BlockedPromptException as e:
            msg_placeholder.empty()
            st.error("⚠️ Essa pergunta não pode ser respondida pelo Vox.")
            st.exception(e) # Original showed exception for more details
            return "Desculpe, não posso responder isso." # Original return message
        except Exception as e:
            msg_placeholder.empty()
            st.error("❌ Ocorreu um erro inesperado na comunicação com a IA.")
            st.exception(e) # Original showed exception
            return "❌ Ocorreu um erro, tente novamente." # Original return message