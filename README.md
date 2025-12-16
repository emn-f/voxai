---
title: VoxAI
emoji: 🏳️‍🌈
colorFrom: purple
colorTo: blue
sdk: streamlit
sdk_version: 1.52.1
python_version: 3.11
app_file: vox_ai.py
pinned: false
license: mit
---

# 🏳️‍🌈 Projeto Vox AI: Assistente de Apoio e Informação LGBTQIA+

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Gemini](https://img.shields.io/badge/Gemini-8E75B8?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev/)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=flat-square&logo=huggingface&logoColor=black)](https://huggingface.co/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)](https://docs.github.com/en/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

> **Projeto de extensão universitária que une Inteligência Artificial e acolhimento para a comunidade LGBTQIA+.**

### 🚀 [Acesse o VoxAI](https://assistentevox.streamlit.app/) | 📊 [Ver Dashboard no GitPages](https://emn-f.github.io/vox-ai/)

---

## 📋 Sumário
* [💡 Sobre o Projeto](#-sobre-o-projeto)
* [✨ Funcionalidades](#-funcionalidades)
* [💻 Tecnologias Utilizadas](#-tecnologias-utilizadas)
* [🤝 Nossa Parceria: Casa Marielle Franco](#-nossa-parceria-casa-marielle-franco)
* [🚀 Rodando o Projeto Localmente](#-rodando-o-projeto-localmente)
* [🤝 Como Contribuir](#-como-contribuir)
* [🤖 Automação e CI/CD](#-automação-e-cicd)
* [⚖️ Governança e Ética](#️-governança-e-ética)
* [📝 Licença](#-licença)
* [👥 Equipe](#-equipe)
* [📬 Contato](#-contato)

## 💡 Sobre o Projeto
O **VoxAI** é um assistente de apoio e informação LGBTQIA+ desenvolvido como parte do projeto de extensão universitária **"Vox: Inteligência Artificial para Inclusão e Cidadania"** da Universidade Católica do Salvador (UCSal). Liderado por Emanuel Ferreira, estudante de Engenharia de Software, o projeto tem como principal público a comunidade LGBTQIA+ de Salvador, Bahia.

### Missão
Ser um ponto de apoio digital seguro, oferecendo informações confiáveis, orientação e acolhimento. O VoxAI usa tecnologia para combater a desinformação e promover cidadania, respeito e dignidade.

## ✨ Funcionalidades

* **Interface Acolhedora:** Chatbot intuitivo desenvolvido com Streamlit, focado na experiência do usuário.
* **Busca Semântica (RAG):** Respostas embasadas em uma base de conhecimento curada, utilizando `SentenceTransformers` para garantir precisão e evitar alucinações.
* **IA Generativa Responsável:** Integração com Google Gemini, instruído para atuar com empatia e segurança.
* **Feedback Loop:** Mecanismo de avaliação integrado para melhoria contínua baseada na opinião da comunidade.
* **Portal de Transparência:** Um [Dashboard](https://emn-f.github.io/vox-ai/) público para acompanhar changelogs, status da base de dados e métricas do projeto.

## 💻 Tecnologias Utilizadas

* **Core:** Python 3.11+, Streamlit.
* **IA:** Google Gemini 1.5 Flash (via `gemini-flash-latest`), Sentence-Transformers (RAG).
* **Dados:** Supabase (Banco Vetorial e Logs), Google Sheets (Curadoria).
* **DevOps:** GitHub Actions (CI/CD), Git Cliff (Changelog), Hugging Face (Deploy).

## 🤝 Nossa Parceria: Casa Marielle Franco

O Projeto VoxAI tem uma parceria oficial com a **Casa Marielle Franco**, instituição de acolhimento independente em Salvador (BA). A Casa atua como ponto de escuta e validação de nossos conteúdos, garantindo que a tecnologia esteja alinhada com as reais necessidades da comunidade.

## 🚀 Rodando o Projeto Localmente

Para contribuir ou testar:

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/emn-f/vox-ai.git
    cd vox-ai
    ```
2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure:** Crie um arquivo `.streamlit/secrets.toml` com sua chave da API do Gemini:
    ```toml
    GEMINI_API_KEY = "SUA_CHAVE_AQUI"
    
    [supabase]
    url = "SUA_URL_SUPABASE"
    key = "SUA_CHAVE_ANON_SUPABASE"
    ```
    > **🔒 Acesso ao Banco de Dados (Supabase):**
    > As credenciais do Supabase são internas da equipe Vox AI.
    > * **Para rodar:** O projeto funciona **sem** elas (apenas sem histórico e busca na base de conhecimento). Basta configurar a `GEMINI_API_KEY`.
    > * **Para desenvolver:** Se sua nova feature **exige** integração com o banco de dados, entre em contato com a equipe (`assistentedeapoiolgbtvox@gmail.com`) explicando sua proposta para avaliarmos o fornecimento de credenciais de teste.
    ```
4.  **Execute:**
    ```bash
    streamlit run vox_ai.py
    ```

## 🤝 Como Contribuir

Contribuições são bem-vindas! Consulte nosso [**Guia de Contribuição**](CONTRIBUTING.md) para detalhes sobre padrões de commit, setup e fluxo de desenvolvimento.

## 🤖 Automação e CI/CD

* **Versionamento Semântico:** Tags geradas automaticamente em releases.
* **Changelog Automático:** Gerado via Git Cliff a cada atualização.
* **Sync de Dados:** Sincronização automática entre Google Sheets e JSON.
* **Deploy Contínuo:** Espelhamento automático para o Hugging Face Spaces.

## ⚖️ Governança e Ética

Segurança e respeito são pilares do Vox. Consulte nossos documentos oficiais:

* [**Código de Conduta**](CODE_OF_CONDUCT.md): Nossos pactos de convivência.
* [**Política de Privacidade**](PRIVACY_POLICY.md): Como tratamos dados (100% anônimos).
* [**Política de Segurança**](SECURITY.md): Como reportar vulnerabilidades.

## 📝 Licença

Licenciado sob a **Licença MIT**. Veja o arquivo [LICENSE](LICENSE).

## 👥 Equipe

**Liderança Técnica:** [Emanuel Ferreira](https://github.com/emn-f)

**Colaboradores (Curadoria):** Alicia Batista, Brenda Pires, Fernanda Souza, [Kauã Araujo](https://github.com/Kauagit99), Lucca Pertigas, [Marcio Ventura](https://github.com/cau-r).

## 📬 Contato

* **E-mail:** [assistentedeapoiolgbtvox@gmail.com](mailto:assistentedeapoiolgbtvox@gmail.com)
* **Instagram:** [@projetovoxai](https://www.instagram.com/projetovoxai/)
* **Linktree:** [linktr.ee/vox_ai](https://linktr.ee/vox_ai)