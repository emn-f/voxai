import json
import subprocess
import os

BASE_PRINCIPAL_PATH = "data/knowledge_base.json"

def data_vox(caminho=BASE_PRINCIPAL_PATH):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def buscar_tema(tema, base):
    return [
        item["descricao"]
        for item in base
        if tema.lower() in item["tema"].lower()
    ]
    
def get_current_branch():
    try:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode("utf-8").strip()
        if branch == "master":
            return "Production"
        else:
            return "Development"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "dev"

def git_version():
    try:
        if get_current_branch() == "Production":
            tag_pattern = "v*"
        else:
            if get_current_branch() == "Development":
                tag_pattern = "dev-v*"
        last_tag = subprocess.check_output(["git", "tag", "--list", tag_pattern, "--sort=-v:refname"]).decode("utf-8").splitlines()
        last_tag = last_tag[0] if last_tag else ""
    except subprocess.CalledProcessError:
        last_tag = "'-'"
    return f"{last_tag}"
