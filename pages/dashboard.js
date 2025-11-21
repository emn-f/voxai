document.addEventListener('DOMContentLoaded', function () {

    const options = {
        headers: {
            'Cache-Control': 'max-age=300' 
        }
    };

    fetch('data/knowledge_base.json', options)
        .then(response => response.ok ? response.json() : Promise.reject('Erro ao buscar knowledge_base.json.'))
        .then(kb_data => {
            const count = kb_data.data ? kb_data.data.length : 0;
            document.getElementById('kb-count').textContent = count;
            const version = kb_data.kb_version || 'N/A';
            document.getElementById('kb-version').textContent = `v${version}`;
        })
        .catch(error => {
            console.error(error);
            document.getElementById('kb-count').textContent = 'Erro';
            document.getElementById('kb-version').textContent = 'Erro';
        });

    fetch('CHANGELOG.md', options)
        .then(response => response.ok ? response.text() : Promise.reject('Erro ao buscar CHANGELOG.md.'))
        .then(markdown => {
            const start = markdown.indexOf('## [');
            if (start !== -1) {
                const nextStart = markdown.indexOf('\n## [', start + 1);
                let entryMarkdown;
                if (nextStart !== -1) {
                    entryMarkdown = markdown.substring(start, nextStart);
                } else {
                    entryMarkdown = markdown.substring(start);
                }
                document.getElementById('latest-changelog').innerHTML = marked.parse(entryMarkdown);
            } else {
                throw new Error('Formato do CHANGELOG não reconhecido.');
            }
        })
        .catch(error => {
            console.error(error);
            document.getElementById('latest-changelog').innerHTML = '<p style="color: #f85149;">Erro: Não foi possível carregar o CHANGELOG.md.</p>';
        });

});