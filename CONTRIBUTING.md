# Guia de Contribuição do Vox AI 🏳️‍🌈

Primeiramente, **obrigado** por seu interesse em contribuir com o Vox AI! 🎉

Somos um projeto de código aberto focado em tecnologia social e inclusão. Seja corrigindo um bug, melhorando a documentação, aprimorando nossa base de conhecimento ou propondo novas features, sua ajuda é essencial para tornarmos este assistente cada vez mais seguro e útil para a comunidade LGBTQIA+.

Este documento é um guia para ajudá-lo a contribuir da melhor forma possível.

## 📚 Índice

1.  [Código de Conduta](#-código-de-conduta)
2.  [Como Começar](#-como-começar)
3.  [Fluxo de Desenvolvimento](#-fluxo-de-desenvolvimento)
4.  [Padrões de Commit (Importante!)](#-padrões-de-commit)
5.  [Base de Conhecimento (RAG)](#-base-de-conhecimento-rag)
6.  [Abrindo um Pull Request](#-abrindo-um-pull-request)

---

## 🤝 Código de Conduta

Este projeto e todos os seus participantes estão sob o nosso [Código de Conduta](CODE_OF_CONDUCT.md). Ao participar, espera-se que você mantenha este código. Por favor, reporte comportamentos inaceitáveis para `assistentedeapoiolgbtvox@gmail.com`.

---

## 🚀 Como Começar

Se você quer rodar o projeto localmente para testar mudanças:

1.  **Fork** este repositório.
2.  **Clone** o seu fork:
    ```bash
    git clone [https://github.com/SEU-USUARIO/vox-ai.git](https://github.com/SEU-USUARIO/vox-ai.git)
    cd vox-ai
    ```
3.  **Crie um ambiente virtual** (Recomendado Python 3.11+):
    ```bash
    python -m venv .venv
    .venv\Scripts\activate     # Windows
    # ou
    source .venv/bin/activate  # Linux/Mac
    ```
4.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Configure as Variáveis de Ambiente:**
    Crie um arquivo `.streamlit/secrets.toml` na raiz do projeto. Você precisará apenas da chave da API do **Google Gemini** para o chat funcionar.

    O arquivo deve seguir este formato:

    ```toml
    GEMINI_API_KEY = "SUA_CHAVE_AQUI"
    ```

    > **⚠️ Nota sobre Logs:**
    > Ao rodar o projeto sem as credenciais administrativas do Google Cloud (que são de uso interno da equipe), você verá o seguinte aviso no terminal a cada mensagem:
    >
    > `⚠️ Falha silenciosa ao registrar log de conversa: ...`
    >
    > **Não se preocupe, isso é normal.** O assistente foi projetado para funcionar perfeitamente mesmo sem essa integração. O aviso apenas indica que a conversa não está sendo salva na planilha da equipe core. Saiba mais sobre o registro de logs em [PRIVACY_POLICY](PRIVACY_POLICY).
6.  **Execute o projeto:**
    ```bash
    streamlit run vox_ai.py
    ```

---

## 🔄 Fluxo de Desenvolvimento

Utilizamos um fluxo simples baseado em branches:

* **`master`**: Código em produção (estável). Não comite diretamente aqui.
* **`dev`**: Branch principal de desenvolvimento. Seus PRs devem apontar para cá.

**Para nova feature ou correção:**
1.  Crie uma branch a partir de `dev`:
    ```bash
    git checkout -b feat/minha-nova-feature
    ```

---

## 📝 Padrões de Commit

Utilizamos a especificação **[Conventional Commits](https://www.conventionalcommits.org/)**. Isso é **obrigatório**, pois nosso Changelog é gerado automaticamente com base nessas mensagens.

A estrutura da mensagem deve ser:
`tipo: descrição curta e imperativa`

**Tipos aceitos:**

| Tipo | Descrição | Exemplo |
| :--- | :--- | :--- |
| **feat** | Nova funcionalidade para o usuário | `feat: adiciona botão de feedback` |
| **fix** | Correção de bug | `fix: corrige erro na sidebar mobile` |
| **docs** | Mudanças apenas na documentação | `docs: atualiza README com instruções de setup` |
| **style** | Formatação, CSS, espaços em branco (sem mudar lógica) | `style: melhora contraste do botão dark mode` |
| **refactor** | Refatoração de código (sem mudar funcionalidade) | `refactor: simplifica função de busca semântica` |
| **perf** | Melhoria de performance | `perf: otimiza carregamento do JSON` |
| **test** | Adição ou correção de testes | `test: adiciona teste unitário para utils.py` |
| **chore** | Tarefas de build, configs, auxiliares | `chore: atualiza dependências do requirements.txt` |
| **ci** | Alterações em arquivos de CI/CD (GitHub Actions) | `ci: ajusta workflow de deploy no hugging face` |

---

## 🧠 Base de Conhecimento (RAG)

O Vox utiliza uma arquitetura RAG (Retrieval-Augmented Generation). Os dados ficam em `data/knowledge_base.json`.

⚠️ **Atenção:**
Nossa base de conhecimento é sincronizada automaticamente a partir de uma planilha do Google Sheets curada pela equipe do projeto.
* **Não edite manualmente** o arquivo `data/knowledge_base.json` para adicionar conteúdo, pois suas alterações serão sobrescritas na próxima sincronização.
* Se você encontrou um erro de informação ou quer sugerir um novo tema, por favor, **abra uma Issue** com a sugestão.

---

## 📥 Abrindo um Pull Request

1.  Certifique-se de que seu código está rodando sem erros.
2.  Faça o Push da sua branch para o seu fork.
3.  Abra um Pull Request para a branch **`dev`** do repositório original.
4.  Na descrição do PR, explique o que foi feito e vincule a Issue relacionada (se houver).
5.  Aguarde a revisão da equipe! 💜

---

Dúvidas? Entre em contato através das Issues ou pelo [e-mail oficial](mailto:assistentedeapoiolgbtvox@gmail.com).