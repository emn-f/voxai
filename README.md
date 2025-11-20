---
title: VoxAI
emoji: 🌈
colorFrom: purple
colorTo: blue
sdk: streamlit
sdk_version: 1.35.0
app_file: vox_ai.py
pinned: false
license: mit
---

# 🌈 VoxAI: Assistente de Apoio e Informação LGBTQIA+

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Gemini](https://img.shields.io/badge/Gemini-8E75B8?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev/)
[![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=flat-square&logo=googlecloud&logoColor=white)](https://cloud.google.com/)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=flat-square&logo=huggingface&logoColor=black)](https://huggingface.co/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Git](https://img.shields.io/badge/GIT-E44C30?style=flat-square&logo=git&logoColor=white)](https://git-scm.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)](https://docs.github.com/en/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

Projeto de extensão universitária que une Inteligência Artificial e acolhimento para a comunidade LGBTQIA+.

### 👉 [**Acesse aqui o VoxAI e comece a conversar!**](https://assistentevox.streamlit.app/) 👈

---

## 📋 Sumário
* [💡 Sobre o Projeto](#-sobre-o-projeto)
* [✨ Funcionalidades](#-funcionalidades)
* [💻 Tecnologias Utilizadas](#-tecnologias-utilizadas)
* [🤝 Nossa Parceria: Casa Marielle Franco](#-nossa-parceria-casa-marielle-franco)
* [🚀 Rodando o Projeto Localmente](#-rodando-o-projeto-localmente)
* [🤝 Como Contribuir](#-como-contribuir)
* [🤖 Automação e CI/CD](#-automação-e-cicd)
* [🔒 Privacidade](#-privacidade)
* [📝 Licença](#-licença)
* [👥 Equipe](#-equipe)
* [📬 Contato](#-contato)
* [📝 Changelog](#-changelog)

## 💡 Sobre o Projeto
O **VoxAI** é um assistente de apoio e informação LGBTQIA+ desenvolvido como parte do projeto de extensão universitária **"Vox: Inteligência Artificial para Inclusão e Cidadania"** da Universidade Católica do Salvador (UCSal). Liderado por Emanuel Ferreira, estudante de Engenharia de Software, o projeto tem como principal público a comunidade LGBTQIA+ da cidade de Salvador, Bahia, Brasil.

### Missão e Propósito
Nossa missão é ser um ponto de apoio digital seguro para pessoas LGBTQIA+, oferecendo informações confiáveis, orientação e acolhimento. Pessoas LGBTQIA+, especialmente jovens e em situação de vulnerabilidade, frequentemente enfrentam barreiras para acessar informações sobre seus direitos, saúde e serviços de apoio, além de sofrerem com a discriminação. O VoxAI nasce para mitigar esse problema, usando a tecnologia para promover cidadania, respeito e dignidade.

## ✨ Funcionalidades

O VoxAI oferece uma experiência de conversação intuitiva, segura e informativa:

* **Interface Amigável:** Desenvolvido com Streamlit, o chat é intuitivo e responsivo, com animação de digitação para uma interação mais dinâmica.
* **Busca Semântica Inteligente:** Antes de responder, o VoxAI analisa sua pergunta e busca em nossa base de conhecimento curada por informações relevantes para complementar a resposta. Utilizamos um modelo `paraphrase-multilingual-MiniLM-L12-v2` para essa tarefa.
* **IA Generativa com Gemini:** As respostas são geradas pelo modelo `gemini-2.0-flash` da Google, instruído para ser empático, acolhedor e jamais inventar dados sem fontes.
* **Base de Conhecimento Confiável:** Nossa base de dados é curada com informações de fontes acadêmicas, documentos oficiais, e relatos da comunidade, cobrindo temas como saúde, direitos, cultura e locais de acolhimento.
* **Dashboard de Transparência:** Um portal dedicado para acompanhar o status da base de conhecimento, changelogs e informações institucionais em tempo real.
* **Registro Anônimo para Melhoria:** As conversas são salvas de forma anônima em uma planilha do Google Sheets para que nossa equipe possa identificar pontos de melhoria e corrigir imprecisões.

## 💻 Tecnologias Utilizadas

Este projeto é construído com as seguintes tecnologias e bibliotecas principais:

* **Frontend:**
    * [**Streamlit**](https://streamlit.io/): Para a criação da interface de chat interativa.
    * **HTML5/CSS3/JS**: Para o Dashboard e customizações visuais.
* **IA e Machine Learning:**
    * [**Google Generative AI (Gemini)**](https://ai.google.dev/): Modelo de linguagem para geração das respostas.
    * [**Sentence-Transformers**](https://www.sbert.net/): Para a busca semântica e ranqueamento de similaridade.
    * [**Hugging Face Hub**](https://huggingface.co/): Para hospedagem de modelos e deploy secundário.
* **Integração e Dados:**
    * [**gspread**](https://docs.gspread.org/): Para integração e registro de logs no Google Sheets.
    * **JSON**: Estrutura local da base de conhecimento.
* **Automação e Ferramentas:**
    * [**GitHub Actions**](https://github.com/features/actions): Pipelines de CI/CD.
    * [**Git Cliff**](https://git-cliff.org/): Geração automática de changelogs.

## 🤝 Nossa Parceria: Casa Marielle Franco

O Projeto VoxAI tem uma parceria oficial com a **Casa Marielle Franco**, uma instituição de acolhimento independente em Salvador (BA), coordenada por Sandra Muñoz. A Casa é referenciada dentro do VoxAI como um espaço seguro e atua como ponto de escuta e validação de conteúdos, reforçando nosso compromisso com a realidade local e o cuidado humano.

## 🚀 Rodando o Projeto Localmente

Quer contribuir ou testar o VoxAI na sua máquina? Siga os passos:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/emn-f/vox-ai.git](https://github.com/emn-f/vox-ai.git)
    cd vox-ai
    ```

2.  **Crie um ambiente virtual e instale as dependências:**
    ```bash
    python -m venv .venv
    ```
    * No Windows:
      ```bash
      .venv\Scripts\activate
      ```
    * No macOS/Linux:
      ```bash
      source .venv/bin/activate
      ```
    Em seguida, instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure as variáveis de ambiente:**
    Você precisará de uma chave de API do Google Gemini. Crie um arquivo `.streamlit/secrets.toml` na raiz do projeto com o seguinte conteúdo:
    ```toml
    GEMINI_API_KEY = "SUA_CHAVE_DE_API_AQUI"
    # Opcional: Credenciais do GCP para logs (se for utilizar integração com Sheets)
    ```
4.  **Execute a aplicação:**
    ```bash
    streamlit run vox_ai.py
    ```

## 🤝 Como Contribuir

Suas contribuições são muito bem-vindas! Adotamos o padrão **Conventional Commits** para manter nosso histórico organizado.

* **Reportando Bugs:** Encontrou algum problema? Abra uma [issue](https://github.com/emn-f/vox-ai/issues).
* **Enviando Pull Requests:**
    1.  Faça um Fork do projeto.
    2.  Crie uma branch (`git checkout -b feature/MinhaNovaFeature`).
    3.  Faça o commit (`git commit -m 'feat: adiciona nova funcionalidade X'`). Confira nosso [guia de commits](conventional_commits.md).
    4.  Faça o push (`git push origin feature/MinhaNovaFeature`).
    5.  Abra um PR.

## 🤖 Automação e CI/CD

O projeto utiliza **GitHub Actions** para manter tudo sincronizado e versionado:

* **Versionamento Automático:** Tags são geradas automaticamente (`dev-v*` e `v*`) ao realizar push nas branches principais.
* **Changelog Dinâmico:** Utilizamos **Git Cliff** para gerar o arquivo `CHANGELOG.md` automaticamente com base nos commits.
* **Sincronização de KB:** Um workflow diário sincroniza novos dados cadastrados na planilha do Google Sheets diretamente para o `knowledge_base.json` do repositório.
* **Deploy Hugging Face:** Push automático para o Space no Hugging Face em atualizações de desenvolvimento.

## 🔒 Privacidade

Sua privacidade é nossa prioridade. **Nós não coletamos dados pessoais** como nome, IP ou localização. A interação é 100% anônima. Para saber mais, leia nossa [**Política de Privacidade**](PRIVACY_POLICY.md).

## 📝 Licença

Este projeto é licenciado sob a **Licença MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Equipe

**Coordenação e Desenvolvimento:**
* **Emanuel Ferreira** (Líder Técnico / Diretor do Vox)

**Colaboradores (Base de Dados Inicial):**
Agradecemos aos estudantes que contribuíram na curadoria da primeira versão da nossa base de conhecimento:
* Alicia Batista
* Brenda Pires
* Fernanda Souza
* Kauã Araujo
* Lucca Pertigas
* Marcio Ventura

## 📬 Contato

Dúvidas, sugestões ou feedback? Fique à vontade para entrar em contato!

* **E-mail:** [assistentedeapoiolgbtvox@gmail.com](mailto:assistentedeapoiolgbtvox@gmail.com)
* **Instagram:** [@projetovoxai](https://www.instagram.com/projetovoxai/)
* **LinkedIn:** [Projeto Vox](https://www.linkedin.com/company/assistentevox/)

## 📝 Changelog

Para acompanhar todas as mudanças e atualizações do projeto, consulte o nosso [**CHANGELOG.md**](CHANGELOG.md).
