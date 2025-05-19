import json
import subprocess
import os

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
        # Descobre a branch atual
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"]
        ).decode("utf-8").strip()
        # Define o padrão da tag conforme a branch
        if branch == "master":
            tag_pattern = "v"
        else:
            tag_pattern = "dev-v"
        last_tag = subprocess.check_output(
            ["git", "tag", "--list", tag_pattern, "--sort=-v:refname"]
        ).decode("utf-8").splitlines()
        last_tag = last_tag[0] if last_tag else ""
    except subprocess.CalledProcessError:
        last_tag = ""
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"]
        ).decode("utf-8").strip()
    except subprocess.CalledProcessError:
        commit = "'-'"
    return f"{last_tag} ({commit})"