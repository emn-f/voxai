import streamlit as st
import google.generativeai as genai
import os
from src.app.ui import stream_resposta
from data.prompts.system_prompt import INSTRUCOES
from src.config import GEMINI_MODEL_NAME

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
    if 'hist_exibir' not in st.session_state:
        st.session_state.hist_exibir = []
        
    modelo = genai.GenerativeModel(GEMINI_MODEL_NAME)
    chat = modelo.start_chat(history=st.session_state.hist)
    return chat

def gerar_resposta(chat, prompt, info_adicional):
    msg_placeholder = st.empty()
    with st.spinner("🧠 Thinking about it..."):
        try:
            full_prompt_for_model = prompt
            if info_adicional:
                full_prompt_for_model = f"Prompt do Usuário: {prompt}\n\nContexto interno da sua base de conhecimento, que o usuário NÃO forneceu (use para embasar sua resposta): {info_adicional}\n\nResponda à pergunta do usuário com base no contexto fornecido."
            resposta = ''
            for chunk in chat.send_message(full_prompt_for_model, stream=True):
                resposta += chunk.text
            msg_placeholder.write_stream(stream_resposta(resposta))
            return resposta
        except genai.types.generation_types.BlockedPromptException as e:
            msg_placeholder.empty()
            st.error("⚠️ Essa pergunta não pode ser respondida pelo Vox.")
            st.exception(e)
            return "Desculpe, não posso responder isso."
        except Exception as e:
            msg_placeholder.empty()
            st.error("❌ Ocorreu um erro inesperado na comunicação com a IA.")
            print(st.exception(e))
            return "❌ Ocorreu um erro, tente novamente."

def transcrever_audio(audio_file):
    """
    Envia o áudio para o Gemini e pede a transcrição em texto.
    """
    try:
        model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        response = model.generate_content([
            "Transcreva este áudio para português do Brasil. Retorne apenas o texto transcrito, sem comentários adicionais.",
            {"mime_type": "audio/mp3", "data": audio_file.read()}
        ])
        
        return response.text
    except Exception as e:
        st.error(f"Erro na transcrição: {e}")
        return None