import streamlit as st
import google.generativeai as genai
import os
from src.app.ui import stream_resposta # Assuming this is correctly located
from data.prompts.system_prompt import INSTRUCOES # Assuming this is correctly located

def configurar_api_gemini():
    try:
        # Try to get API key from Streamlit secrets first, then environment variables
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key:
            api_key = os.environ.get("GEMINI_API_KEY")

        if not api_key:
            st.error("Chave da API Gemini não localizada. Configure-a em .streamlit/secrets.toml ou como variável de ambiente GEMINI_API_KEY.")
            st.stop()

        genai.configure(api_key=api_key)
        # Store a flag or the key itself in session state if needed by other parts, but configure is global.
        st.session_state.gemini_api_configured = True
        return api_key # Or True, to indicate success
    except Exception as e:
        st.error(f"Erro ao configurar a API do Gemini: {e}")
        st.session_state.gemini_api_configured = False
        st.stop()
        return None # Or False

def inicializar_chat_modelo():
    # Ensure history is initialized in session state
    if 'hist' not in st.session_state:
        # Initialize with system prompt and a default first model response
        st.session_state.hist = [
            {"role": "user", "parts": [INSTRUCOES]},
            {"role": "model", "parts": ["Entendido. Sou Vox AI, sua assistente LGBTQIA+ para informações e apoio. Como posso ajudar hoje?"]}
        ]

    # Initialize model and chat session in session_state if they don't exist
    if 'gemini_model' not in st.session_state:
        # Consider making the model name a configurable variable
        st.session_state.gemini_model = genai.GenerativeModel('gemini-1.0-pro')

    if 'chat_session' not in st.session_state:
        # Start chat with the existing history from st.session_state.hist
        # This history should contain the system prompt and the initial model response
        st.session_state.chat_session = st.session_state.gemini_model.start_chat(history=st.session_state.hist)

    return st.session_state.chat_session

def gerar_resposta(prompt, info_adicional): # Removed 'chat' parameter
    msg_placeholder = st.empty() # For streaming output

    # Retrieve the chat session from session state
    if 'chat_session' not in st.session_state:
        st.error("Sessão de chat não inicializada. Por favor, recarregue a página.")
        return "Erro: Sessão de chat não encontrada."

    chat = st.session_state.chat_session

    with st.spinner("Pensando..."):
        try:
            full_prompt_for_model = prompt
            if info_adicional and str(info_adicional).strip():
                full_prompt_for_model = f"{prompt}\n\nConsidere a seguinte informação complementar para sua resposta: {info_adicional}"

            response_stream = chat.send_message(full_prompt_for_model, stream=True)

            resposta_completa = ""
            collected_chunks = []
            for chunk in response_stream:
                if hasattr(chunk, 'text') and chunk.text:
                    collected_chunks.append(chunk.text)

            if not collected_chunks: # Handle cases where the stream might be empty or not as expected
                # This could be due to content filtering at the API level or other issues
                st.warning("A IA não forneceu uma resposta para esta pergunta. Isso pode ocorrer devido a filtros de conteúdo ou outras restrições.")
                return "Não foi possível obter uma resposta da IA para esta pergunta."

            resposta_completa = "".join(collected_chunks)

            # Update placeholder with the full response using the stream_resposta utility
            # Ensure stream_resposta can handle a complete string if that's what it expects
            msg_placeholder.write_stream(stream_resposta(resposta_completa))

            return resposta_completa

        except genai.types.generation_types.BlockedPromptException:
            msg_placeholder.empty()
            st.error("⚠️ Esta pergunta não pode ser respondida pelo Vox devido a restrições de conteúdo.")
            return "Desculpe, não posso responder a esta pergunta."
        except Exception as e:
            msg_placeholder.empty()
            st.error(f"❌ Ocorreu um erro inesperado na comunicação com a IA: {e}")
            return "Ocorreu um erro ao tentar gerar uma resposta. Por favor, tente novamente."