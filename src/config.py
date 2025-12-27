import os

# Caminhos
CSS_PATH = "static/css/style.css"

# Configurações de IA
MODELO_SEMANTICO_NOME = "models/text-embedding-004"
GEMINI_MODEL_NAME = 'gemini-flash-latest'

# Config da KB
SEMANTICA_THRESHOLD = 0.5
LIMITE_TEMAS = 10
MAX_CHUNCK = 25

# Configurações de UI
PAGE_TITLE = 'Vox AI'
PAGE_ICON = '🏳️‍🌈'

class StatusConhecimento:
    PENDENTE = -1
    REJEITADO = 0
    APROVADO = 1
