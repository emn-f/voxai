import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyBdY7GDRfqrZ4ucBPwCXBTetpagiIuW7i4"

genai.configure(api_key=GEMINI_API_KEY)

print("Listando modelos disponíveis...")

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)