## [3.1.2] - 2025-12-16

### 📚 Documentação
- Documentações atualizadas para refletir implementação do Supabase.
- Criação de `SUPPORT.md`.

## [3.1.1] - 2025-12-16

### 🔧 Tarefas Internas
- Sincronização do Changelog entre branchs agora é feita de forma automática e imediata.

## [3.1.0] - 2025-12-16

### ♻️ Refatoração & Melhorias
- Dashboard puxa métricas direto do Supabase.

### ✨ Funcionalidades
- Adição de botão para contribuir com a base de conhecimento.

### ⚡ Performance
- *(database)* [**breaking**] Migra arquitetura de dados e rag para Supabase.
- Vox agora utiliza o modelo mais recente disponível do Gemini Flash.

### 📦 Build & Dependências
- Remoção de scripts que não são mais necessários pra comunicação com a base de conhecimento.

## [3.0.1] - 2025-12-06

### 🤖 CI/CD & Automação
- Correção na `Sync Changelog from Master to Dev`.

## [3.0.0] - 2025-12-06

### ✨ Funcionalidades
- Adição de botão que permite reportar comportamento inadequado do Vox.

### 🎨 Estilo e Formatação
- Dashboard do GitPages exibe até 10 atualizações recentes.

### 🤖 CI/CD & Automação
- Ajuste no comando de push para `master` na action `tag_prod.yml`.
- Criada action para incremento manual de tags.
- Correção de bug da `sync_changelog`.

## [2.8.4] - 2025-12-04

### 📦 Build & Dependências
- Versão mínima do Streamlit especificada para funcionamento do Vox no Hugging Face.

## [2.8.3] - 2025-12-04

### 🐛 Correções
- Atualiza config do Hugging Face Space para Python 3.11 (resolve FutureWarning de google.api_core).

## [2.8.2] - 2025-12-03

### ✨ Funcionalidades
- Adição de função "texto pra voz" que permite escutar a resposta do Vox em voz alta. #66
- Implementação de função que permite que usuário converse com o Vox por áudio.

## [2.8.1] - 2025-11-26

### ✨ Funcionalidades
- Adiciona Issue Templates para bug reports, feature requests e outras tarefas.

### 📚 Documentação
- Update `CHANGELOG.md`.
- Ajustes no `CONTRIBUTING.md`.

### 🤖 CI/CD & Automação
- Adição de action para sinc do `CHANGELOG.md` da branch `master` para a `dev`.

## [2.7.7] - 2025-11-26

### 🎨 Estilo e Formatação
- Melhorias gerais no GitPages #90.

### 🐛 Correções
- Versão do Vox não era exibida no Hugging Face.

### 🤖 CI/CD & Automação
- Alteração do nome da action do HF.
- Criada Action para controle de deploy do Git Pages.

## [2.7.6] - 2025-11-24

### ✨ Funcionalidades
- Correção do link de deploy no GitPages.

## [2.7.5] - 2025-11-23

### ♻️ Refatoração & Melhorias
- Remoção de comentários.

### ✨ Funcionalidades
- Links externos centralizados em `src/external_links.py`,

### 📚 Documentação
- Criação de `ASSETS.md` com todos os links e ativos digitais do Vox.
- Criação de Guia de Contribuição para o Vox.
- Atualização do `PRIVACY_POLICY.md`.
- Atualização do `README.md`.

## [2.7.4] - 2025-11-23

### ⚡ Performance
- Add caching and create `config.py`.

## [2.7.3] - 2025-11-21

### 🎨 Estilo e Formatação
- Identação no `sync_from_sheets.yml.

### 🤖 CI/CD & Automação
- Impede loop de execução ao atualizar apenas o `CHANGELOG.md`.

## [2.7.1] - 2025-11-21

### ✨ Funcionalidades
- Vox leva em consideração o código de conduta interno.
- Adição de form de avaliação na sidebar.

### 🎨 Estilo e Formatação
- Melhorias no visual da sidebar.
- Remoção de comentários.
- Redesign completo do GitPages com efeito glassmorphism e responsividade.

### 🐛 Correções
- Versão do Vox agora é exibida corretamente no Hugging Face.

## [2.6.4] - 2025-11-21

### ✨ Funcionalidades
- Erros no Vox serão salvos em planilha para análise posterior.

### 📚 Documentação
- Criação de Código de Conduta do Projeto Vox (`CODE_OF_CONDUCT.md`).

## [2.6.3] - 2025-11-21

### 🤖 CI/CD & Automação
- O deploy no Hugging Face olha para a branch `master`.

## [2.6.1] - 2025-11-21

### 📚 Documentação
- Revisão da Política de Segurança (`SECURITY.md`).

### 🤖 CI/CD & Automação
- Correções na action geradora do `CHANGELOG.md`.
- O deploy no Hugging Face olha para a branch `master`.

## [1.0.25] - 2025-11-14

### ✨ Funcionalidades
* Adiciona dashboard no Git Pages.

## [1.0.23] - 2025-11-13

### ♻️ Refatoração & Melhorias
* Ajustes no CSS principal.

## [1.0.22] - 2025-11-12

### ✨ Funcionalidades
* Adiciona cache.

## [1.0.19] - 2025-11-08

### ♻️ Refatoração & Melhorias
* Melhora o `sinc_kb.py`.

## [1.0.18] - 2025-11-07

### ♻️ Refatoração & Melhorias
* Melhora o design da UI (sidebar).

## [1.0.17] - 2025-05-20

### ✨ Funcionalidades
* Nova fonte de dados.
* Adoção da função nativa do Streamlit para exibição de texto em streaming.

## [1.0.16] - 2025-05-20

### ♻️ Refatoração & Melhorias
* Melhorias na personalidade do Vox.

### 🐛 Correções
* Correção da quebra do Markdown da mensagem de boas-vindas.
* Remoção de importações e comentários desnecessários.
* Adição de arquivos internos do Python.

## [1.0.15] - 2025-05-19

### ♻️ Refatoração & Melhorias
* Atualização do `.gitignore`.
* Atualização do `sobre.py`.
* Melhorias na sidebar.

## [1.0.11] - 2025-05-19

### ♻️ Refatoração & Melhorias
* Atualização na personalidade do Vox.

## [1.0.10] - 2025-05-19

### ♻️ Refatoração & Melhorias
* Atualização do `README.MD`.

## [1.0.9] - 2025-05-19

### ♻️ Refatoração & Melhorias
* Modularização de funções e melhorias na UI do Vox AI (PR #4).

## [1.0.8] - 2025-05-19

### ♻️ Refatoração & Melhorias
* Ajusta o padrão da tag na função `git_version`.

## [1.0.7] - 2025-05-19

### 🐛 Correções
* Exibição correta da versão em produção.

## [1.0.6] - 2025-05-19

### ♻️ Refatoração & Melhorias
* Melhora na estrutura do código e adição de comentários explicativos para facilitar a compreensão do fluxo do chat e do tratamento de erros.

## [1.0.4] - 2025-05-19

### 🐛 Correções
* Testes e correções no workflow de tagueamento automático.
* Mudança na cor da versão.

### ♻️ Refatoração & Melhorias
* Tema dark definido como padrão no Streamlit.

## [1.0.2] - 2025-05-19

### 🐛 Correções
* Adiciona tratamento de exceção para a obtenção do hash do commit na função `git_version`.

## [1.0.1] - 2025-05-19

### ♻️ Refatoração & Melhorias
* Remoção de comentários no `git_version`.

## 🚀 Lançamento da primeira versão estável do Vox AI | [1.0.0] - 2025-05-18

### ✨ Funcionalidades
* Primeira versão estável.
* Integração com Gemini API.
* Interface de chat com Streamlit.
* Animação de digitação nas respostas do assistente.
* Workflow de versionamento automático.
* Customização visual com CSS e spinner personalizado.
* Inclusão do `huggingface_hub` para melhorias de desempenho.
* Exibe versão e hash do commit na sideba

### ♻️ Refatoração & Melhorias
* Limiar de similaridade reduzido para 0.4 na função semântica.
* Diversas melhorias de interface e organização do código.
* Adição de instruções de contexto.
* Revisão do `.gitignore`.
* Adição de informações relacionadas ao projeto.
* Ajustes organizacionais.
* Novo arquivo de instruções.
* Melhorias no contexto.
* Melhorias de UI.
* Ajustes relacionados à API.
* Adição do arquivo de `requirements.txt` e melhorias de segurança.

## 🚧 first commit | [dev-v0.0.1] - 2025-05-17
* Nascimento do Vox AI.
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
* Adição de informações relacionadas ao projeto.
* Configuração da API no GenAI.
* Exibição e alerta de status da API.
