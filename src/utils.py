import json
import subprocess

def data_vox(caminho="data/dados_vox.json"):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def buscar_tema(tema, base):
    return [
        item["descricao"]
        for item in base
        if tema.lower() in item["tema"].lower()
    ]

def git_version():
    try:
        # pega a última tag da árvore (mais próxima)
        last_tag = subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"],
            stderr=subprocess.STDOUT
        ).decode("utf-8").strip()
    except subprocess.CalledProcessError:
        last_tag = "sem tags"

    try:
        # pega o hash curto do commit atual
        commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"]
        ).decode("utf-8").strip()
    except subprocess.CalledProcessError:
        commit = "hash indisponível"

    return f"{last_tag} ({commit})"