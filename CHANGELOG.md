## [1.0.25] - 2025-11-14
### Adicionado
* Adiciona dashboard (Git Pages).

## [1.0.23] - 2025-11-13
### Melhorias
* Ajustes no CSS principal.

## [1.0.22] - 2025-11-12
### Adicionado
* Adiciona cache.

## [1.0.19] - 2025-11-08
### Melhorias
* Melhora o sinc_kb.py.

## [1.0.18] - 2025-11-07
### Melhorias
* Melhora o design da UI (sidebar).

## [1.0.17] - 2025-05-20
### Adicionado
* Nova fonte de dados.
* Adoção da função nativa do Streamlit para exibição de texto em streaming.

## [1.0.16] - 2025-05-20
### Melhorias
* Melhorias na personalidade do Vox (v3).

### Corrigido
* Correção da quebra do Markdown da mensagem de boas-vindas.
* Remoção de importações e comentários desnecessários.
* Adição de arquivos internos do Python.

## [1.0.15] - 2025-05-19
### Alterado
* Atualização do `.gitignore`.
* Atualização do `sobre.py`.

### Melhorias
* Melhorias na sidebar.

## [1.0.11] - 2025-05-19
### Melhorias
* Atualização na personalidade do Vox.

## [1.0.10] - 2025-05-19
### Alterado
* Atualização do `README.MD`.

## [1.0.9] - 2025-05-19
### Melhorias
* Modularização de funções e melhorias na UI do VoxAI (PR #4).

## [1.0.8] - 2025-05-19
### Alterado
* Ajusta o padrão da tag na função `git_version`.

## [1.0.7] - 2025-05-19
### Corrigido
* Exibição correta da versão em produção.

## [1.0.6] - 2025-05-19
### Alterado
* Melhora na estrutura do código e adição de comentários explicativos para facilitar a compreensão do fluxo do chat e do tratamento de erros.

## [1.0.5] - 2025-05-19
### Corrigido
* Merge da branch dev na master.

## [1.0.4] - 2025-05-19
### Corrigido
* Testes e correções no workflow de tagueamento automático.
* Mudança na cor da versão.
* Tema dark definido como padrão.

## [1.0.2] - 2025-05-19
### Corrigido
* Adiciona tratamento de exceção para a obtenção do hash do commit na função `git_version`.

## [1.0.1] - 2025-05-19
### Corrigido
* Remoção de comentários no `git_version`.

## [1.0.0] - 2025-05-18
### Adicionado
* Primeira versão estável
* Integração com Gemini API
* Interface de chat com Streamlit
* Animação de digitação nas respostas do assistente
* Workflow de versionamento automático (tags dev/prod)
* Customização visual com CSS e spinner personalizado
* Inclusão do `huggingface_hub` para melhorias de desempenho.
* Exibe versão e hash do commit na sidebar.

### Alterado
* Limiar de similaridade reduzido para 0.4 na função semântica.
* Diversas melhorias de interface e organização do código.
* Adição de instruções de contexto.
* Revisão do `.gitignore`.
* Refatorações para "vox_ai".
* Adição de informações relacionadas ao projeto.
* Ajustes organizacionais.
* Novo arquivo de instruções.
* Melhorias no contexto.
* Melhorias de UI.
* Ajustes relacionados à API.
* Adição do arquivo de `requirements.txt` e melhorias de segurança.

## [dev-v0.0.1] - 2025-05-17
### Adicionado
* Nascimento do VoxAI (16/05/2025 23:02 `6e6ce0a3`)
* Estrutura inicial do projeto.
* MVP funcional com interface.
* Scripts e workflows para automação.
* Primeiras versões do README, temas e JSON.
* Configuração inicial da API e chamadas.
* Organização da base de dados e lógica de contexto.
* Adição de personalidade ao chatbot.
* Saudação transferida para arquivo separado.
* Iniciando preparação da base de dados.
* Exibição da última interação do usuário.
* Melhorias de interface.
* Adição de informações relacionadas ao projeto.
* Refatorações para "vox_ai".
* Configuração da API no GenAI.
* Exibição e alerta de status da API.


### Alterado
* Ajustes organizacionais.
* Revisão do `.gitignore`.
* Melhorias no contexto.
* Melhorias de UI.
