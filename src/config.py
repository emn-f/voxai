import os

# Caminhos
CSS_PATH = "static/css/style.css"

# Configurações de IA
MODELO_SEMANTICO_NOME = 'paraphrase-multilingual-MiniLM-L12-v2'
SEMANTICA_THRESHOLD = 0.4
GEMINI_MODEL_NAME = 'gemini-flash-latest'

# Configurações de UI
PAGE_TITLE = 'VoxAI'
PAGE_ICON = '🏳️‍🌈'

class StatusConhecimento:
    PENDENTE = -1
    REJEITADO = 0
    APROVADO = 1