import json

def data_vox(caminho="data/dados_vox.json"):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def buscar_tema(tema, base):
    return [
        item["descricao"]
        for item in base
        if tema.lower() in item["tema"].lower()
    ]
