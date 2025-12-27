
import streamlit as st
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import buscar_referencias_db
import google.generativeai as genai
from src.config import MODELO_SEMANTICO_NOME

def run_debug_semantic():
    st.write("## Debug Semantic Search Output")
    
    # Configure API key from secrets (mock check)
    if not st.secrets.get("GEMINI_API_KEY"):
         st.error("Missing GEMINI_API_KEY")
         return
    
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    prompt = "transsexuais hormonoterapia"
    st.write(f"Generating embedding for: '{prompt}'")
    
    try:
        result = genai.embed_content(
            model=MODELO_SEMANTICO_NOME, 
            content=prompt, 
            task_type="retrieval_query"
        )
        vetor = result["embedding"]
        st.write(f"Embedding generated. Length: {len(vetor)}")
        
        st.write("Calling buscar_referencias_db...")
        results = buscar_referencias_db(vetor)
        
        st.write(f"Results found: {len(results)}")
        if results:
            # Check available keys
            if results:
                st.write("First item keys:", list(results[0].keys()))
                print(f"DEBUG KEYS: {list(results[0].keys())}")
                print(f"DEBUG SAMPLE: {results[0]}")
                st.write("First item sample:", results[0])
            
            # Check for kb_id specifically
            kb_ids = [r.get("kb_id") or r.get("id") for r in results]
            st.write("Extracted KB IDs (Corrected logic):", kb_ids)
            print(f"DEBUG RESULTS: {results}")
            print(f"DEBUG KB_IDS: {kb_ids}")
            
            if None in kb_ids:
                st.error("Found None in KB IDs! The key 'kb_id' might be missing or explicitly null.")
            
    except Exception as e:
        st.error(f"Error: {e}")
        import traceback
        st.text(traceback.format_exc())

if __name__ == "__main__":
    run_debug_semantic()
