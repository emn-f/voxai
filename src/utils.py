import json

def carregar_base_vox(caminho="data/dados_vox.json"):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def buscar_por_tema(tema, base):
    return [
        item["descricao"]
        for item in base
        if tema.lower() in item["tema"].lower()
    ]
