"""
Atualiza (ou adiciona) o footer padrão do Vox AI em todos os arquivos .md do projeto.

Uso:
    1. Edite a constante SLOGAN abaixo com o novo texto.
    2. Execute: python scripts/update_slogan.py

O script busca o bloco existente e o substitui.
Se o arquivo não tiver o footer, ele é adicionado ao final.
"""

from pathlib import Path
from datetime import datetime
import re
import subprocess

ANO_ATUAL = datetime.today().year

SLOGAN = f"Copyright © {ANO_ATUAL} Vox AI: Segurança para ser quem você é! 🏳️‍🌈"

FOOTER = f'\n---\n\n<div align="left">\n    <p>{SLOGAN}</p>\n</div>'

FOOTER_PATTERN = re.compile(
    r'(?:\n+---\s*\n+)?(?:<div align="left">\s*<p>[^<>\n]+</p>\s*</div>s?|© \d{4} Projeto Vox)\s*$',
    re.IGNORECASE
)

# Arquivos que não devem receber o footer (ex: CHANGELOG gera automaticamente)
IGNORAR = {"CHANGELOG.md"}


def get_tracked_md_files(root: Path) -> list[Path]:
    """Obtém a lista de arquivos .md rastreados no Git."""
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True
        )
        files = []
        for line in result.stdout.splitlines():
            if line.endswith(".md"):
                path = root / line
                if path.name not in IGNORAR:
                    files.append(path)
        return files
    except Exception as e:
        print(f"Erro ao listar arquivos do git ({e}). Usando busca clássica...")
        IGNORAR_DIRS = {".venv", "venv", "node_modules", ".git"}
        return [
            f for f in root.rglob("*.md")
            if f.name not in IGNORAR
            and not any(part in IGNORAR_DIRS for part in f.parts)
        ]


def update_md_files(root: Path = Path(__file__).resolve().parent.parent) -> None:
    md_files = get_tracked_md_files(root)

    adicionados, atualizados, sem_mudanca = [], [], []

    for f in md_files:
        content = f.read_text(encoding="utf-8")

        # Verifica se existe algum footer no arquivo
        match = FOOTER_PATTERN.search(content)
        if match:
            # Se encontrou o footer, substitui pelo novo
            new_content = FOOTER_PATTERN.sub(FOOTER, content)
            if new_content != content:
                f.write_text(new_content, encoding="utf-8")
                atualizados.append(f)
            else:
                sem_mudanca.append(f)
        else:
            # Se não encontrou nenhum footer, adiciona ao final
            f.write_text(content + FOOTER, encoding="utf-8")
            adicionados.append(f)

    print(f"✅ Footer adicionado ({len(adicionados)}):")
    for f in adicionados:
        print(f"   + {f.relative_to(root) if f.is_relative_to(root) else f}")

    print(f"\n✏️  Footer atualizado ({len(atualizados)}):")
    for f in atualizados:
        print(f"   ~ {f.relative_to(root) if f.is_relative_to(root) else f}")

    print(f"\n⏭️  Sem mudança ({len(sem_mudanca)}):")
    for f in sem_mudanca:
        print(f"   = {f.relative_to(root) if f.is_relative_to(root) else f}")


if __name__ == "__main__":
    update_md_files()