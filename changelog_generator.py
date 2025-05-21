# TESTAR FUNCIONAMENTO DEPOIS

# python update_changelog.py

import subprocess
from datetime import datetime
import re
from collections import defaultdict

def get_tags_with_dates():
    """Retorna um dicionário com as tags e suas datas."""
    tags = {}
    try:
        # Lista todas as tags ordenadas por data
        cmd = ['git', 'for-each-ref', '--sort=-creatordate', '--format=%(refname:short)|%(creatordate:short)', 'refs/tags/v*']
        output = subprocess.check_output(cmd).decode('utf-8').strip()
        
        for line in output.split('\n'):
            if line:
                tag, date = line.split('|')
                if not tag.startswith('dev-'):  # Ignora tags dev
                    tags[tag] = date
    except subprocess.CalledProcessError:
        pass
    return tags

def get_commits_between_tags(start_tag=None, end_tag=None):
    """Obtém commits entre duas tags."""
    try:
        if start_tag and end_tag:
            cmd = ['git', 'log', '--format=%H|%s', f'{start_tag}..{end_tag}']
        elif start_tag:
            cmd = ['git', 'log', '--format=%H|%s', f'{start_tag}..HEAD']
        else:
            cmd = ['git', 'log', '--format=%H|%s']
        
        output = subprocess.check_output(cmd).decode('utf-8').strip()
        commits = []
        for line in output.split('\n'):
            if line:
                hash_id, message = line.split('|', 1)
                commits.append((hash_id, message.strip()))
        return commits
    except subprocess.CalledProcessError:
        return []

def categorize_commit(message):
    """Categoriza o commit com base na mensagem."""
    message = message.lower()
    if any(word in message for word in ['adiciona', 'nova', 'novo', 'criação']):
        return 'Adicionado'
    elif any(word in message for word in ['corrige', 'correção', 'fix']):
        return 'Corrigido'
    elif any(word in message for word in ['melhora', 'atualiza', 'refatora']):
        return 'Alterado'
    return 'Alterado'  # categoria padrão

def generate_changelog():
    """Gera o conteúdo do CHANGELOG.md"""
    tags = get_tags_with_dates()
    tags_ordered = sorted(tags.items(), key=lambda x: x[1], reverse=True)
    
    changelog = ["# Changelog\n",
                "\nTodas as mudanças importantes deste projeto serão documentadas aqui.\n",
                "\nO formato segue o padrão [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/)",
                "e este projeto utiliza [Versionamento Semântico](https://semver.org/lang/pt-BR/).\n"]
    
    # Unreleased changes
    unreleased_commits = get_commits_between_tags(tags_ordered[0][0] if tags_ordered else None)
    if unreleased_commits:
        changelog.append("\n## [Unreleased]")
        changes = defaultdict(list)
        for _, message in unreleased_commits:
            category = categorize_commit(message)
            changes[category].append(message)
        
        for category in sorted(changes.keys()):
            changelog.append(f"\n### {category}")
            for message in changes[category]:
                changelog.append(f"- {message}")
    
    # Released versions
    for i in range(len(tags_ordered)):
        current_tag, current_date = tags_ordered[i]
        prev_tag = tags_ordered[i+1][0] if i+1 < len(tags_ordered) else None
        
        commits = get_commits_between_tags(prev_tag, current_tag)
        if commits:
            changelog.append(f"\n## [{current_tag}] - {current_date}")
            changes = defaultdict(list)
            for _, message in commits:
                category = categorize_commit(message)
                changes[category].append(message)
            
            for category in sorted(changes.keys()):
                changelog.append(f"\n### {category}")
                for message in changes[category]:
                    changelog.append(f"- {message}")
    
    return '\n'.join(changelog)

def update_changelog():
    """Atualiza o arquivo CHANGELOG.md"""
    content = generate_changelog()
    with open('CHANGELOG.md', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    update_changelog()