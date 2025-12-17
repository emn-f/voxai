document.addEventListener('DOMContentLoaded', function () {

    const SUPABASE_URL = "__SUPABASE_URL__"; 
    const SUPABASE_KEY = "__SUPABASE_KEY__";

    const headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': `Bearer ${SUPABASE_KEY}`,
        'Content-Type': 'application/json'
    };

    fetch(`${SUPABASE_URL}/rest/v1/knowledge_base?select=id`, {
        method: 'GET',
        headers: { ...headers, 'Prefer': 'count=exact, head=true' }
    })
        .then(response => {
            if (!response.ok) throw new Error('Erro ao conectar com Supabase');

            const contentRange = response.headers.get('Content-Range');
            if (contentRange) {
                const total = contentRange.split('/')[1];
                document.getElementById('kb-count').textContent = total;
            } else {
                document.getElementById('kb-count').textContent = "0";
            }
        })
        .catch(error => {
            console.error("Erro KB Count:", error);
            document.getElementById('kb-count').textContent = '-';
    });
    fetch(`${SUPABASE_URL}/rest/v1/knowledge_base?select=modificado_em&order=modificado_em.desc&limit=1`, {
        method: 'GET',
        headers: headers
    })
        .then(response => response.json())
        .then(data => {
            if (data && data.length > 0) {
                const lastDate = new Date(data[0].modificado_em);
            const versionString = `v${lastDate.getFullYear()}.${(lastDate.getMonth() + 1).toString().padStart(2, '0')}.${lastDate.getDate().toString().padStart(2, '0')}`;
            document.getElementById('kb-version').textContent = versionString;
        } else {
            document.getElementById('kb-version').textContent = "v3.1";
        }
    })
        .catch(error => {
            console.error("Erro KB Version:", error);
            document.getElementById('kb-version').textContent = 'Online';
        });


    fetch('CHANGELOG.md', { headers: { 'Cache-Control': 'max-age=300' } })
        .then(response => response.ok ? response.text() : Promise.reject('Erro ao buscar CHANGELOG.md.'))
        .then(markdown => {
            const start = markdown.indexOf('## [');
            if (start !== -1) {
                let end = start;
                for (let i = 0; i < 5; i++) {
                    const next = markdown.indexOf('\n## [', end + 1);
                    if (next === -1) {
                        end = markdown.length;
                        break;
                    }
                    end = next;
                }
                const entryMarkdown = markdown.substring(start, end);

                document.getElementById('latest-changelog').innerHTML = marked.parse(entryMarkdown);
            }
        })
        .catch(error => {
            console.error(error);
            document.getElementById('latest-changelog').innerHTML = '<p style="color: #f85149;">Erro ao carregar histórico.</p>';
        });
});