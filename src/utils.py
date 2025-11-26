import json
import subprocess
import os
import re
import streamlit as st
from src.config import BASE_PRINCIPAL_PATH

@st.cache_data
def data_vox(caminho=BASE_PRINCIPAL_PATH):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            full_data = json.load(f)
            return full_data.get("data", []), full_data.get("kb_version", "N/A")
    except FileNotFoundError:
        print(f"Arquivo da base de conhecimento não encontrado em: {caminho}")
        return [], "N/A"
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON da base de conhecimento em: {caminho}")
        return [], "N/A"


def get_current_branch():
    try:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode("utf-8").strip()
        
        if branch in ["master", "main"]:
            return "Production"
        else:
            return "Development"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "Development"

def get_version_from_changelog():
    """Lê a versão mais recente do arquivo CHANGELOG.md."""
    try:
        changelog_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "CHANGELOG.md")
        with open(changelog_path, "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r"## \[([\d\.]+)\]", content)
            if match:
                return f"v{match.group(1)}"
    except Exception as e:
        print(f"Erro ao ler CHANGELOG.md: {e}")
    return ""

def git_version():
    try:
        if get_current_branch() == "Production":
            tag_pattern = "v*"
        else:
            tag_pattern = "dev-v*"
            
        last_tag = subprocess.check_output(["git", "tag", "--list", tag_pattern, "--sort=-v:refname"]).decode("utf-8").splitlines()
        last_tag = last_tag[0] if last_tag else ""
    except subprocess.CalledProcessError:
        last_tag = ""
    
    if not last_tag:
        last_tag = get_version_from_changelog()
    
    return f"{last_tag}"