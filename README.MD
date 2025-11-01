# 🌈 VoxAI: Assistente de Apoio e Informação LGBTQIA+

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=flat-square&logo=huggingface&logoColor=black)](https://huggingface.co/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Gemini](https://img.shields.io/badge/Gemini-8E75B8?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev/)
[![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=flat-square&logo=googlecloud&logoColor=white)](https://cloud.google.com/)
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
* [🤖 Automação de Versionamento](#-automação-de-versionamento)
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
* **Registro Anônimo para Melhoria:** As conversas são salvas de forma anônima em uma planilha do Google Sheets para que nossa equipe possa identificar pontos de melhoria e corrigir imprecisões.

## 💻 Tecnologias Utilizadas

Este projeto é construído com as seguintes tecnologias e bibliotecas principais, conforme nosso arquivo `requirements.txt`:

* **Frontend:**
    * [**Streamlit**](https://streamlit.io/): Para a criação da interface de chat interativa.
* **IA e Machine Learning:**
    * [**Google Generative AI (Gemini)**](https://ai.google.dev/): Modelo de linguagem para geração das respostas.
    * [**Sentence-Transformers**](https://www.sbert.net/): Para a busca semântica e ranqueamento de similaridade.
    * [**Hugging Face Hub**](https://huggingface.co/): Para download e cache de modelos de ML.
* **Integração e Dados (API):**
    * [**gspread**](https://docs.gspread.org/): Para integração e registro de logs no Google Sheets.
    * [**google-auth-oauthlib**](https://pypi.org/project/google-auth-oauthlib/): Para autenticação com as APIs do Google.
* **Automação (CI/CD):**
    * [**GitHub Actions**](https://github.com/features/actions): Para automação do versionamento com tags nas branches `dev` e `master`.

### Outras Ferramentas e Tecnologias de Apoio

Além das bibliotecas principais, o projeto também depende de:

* **Git:** Utilizado para o controle de versão e para exibir dinamicamente a versão do projeto na interface.
* **JSON:** Formato de arquivo para a estruturação da nossa base de conhecimento (`knowledge_base.json`).
* **HTML/CSS/JS:** Usados para estilização e melhorias pontuais de usabilidade na interface do Streamlit.
* **YAML:** Linguagem para a definição dos workflows de automação no GitHub Actions.

## 🤝 Nossa Parceria: Casa Marielle Franco

O Projeto VoxAI tem uma parceria oficial com a **Casa Marielle Franco**, uma instituição de acolhimento independente em Salvador (BA), coordenada por Sandra Muñoz. A Casa é referenciada dentro do VoxAI como um espaço seguro e atua como ponto de escuta e validação de conteúdos, reforçando nosso compromisso com a realidade local e o cuidado humano.

## 🚀 Rodando o Projeto Localmente

Quer contribuir ou testar o VoxAI na sua máquina? Siga os passos:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/emn-f/voxai.git](https://github.com/emn-f/voxai.git)
    cd voxai
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
    ```
4.  **Execute a aplicação:**
    ```bash
    streamlit run vox_ai.py
    ```

## 🤝 Como Contribuir

Suas contribuições são muito bem-vindas e nos ajudam a tornar o VoxAI ainda melhor! Existem várias formas de colaborar:

* **Reportando Bugs:** Encontrou algum problema? Abra uma [issue](https://github.com/emn-f/voxai/issues) detalhando o erro.
* **Sugerindo Melhorias:** Tem ideias para novas funcionalidades ou aperfeiçoamentos? Abra uma [issue](https://github.com/emn-f/voxai/issues) para discussão.
* **Enviando Pull Requests:**
    1.  Faça um Fork do projeto.
    2.  Crie uma branch para sua modificação (`git checkout -b feature/MinhaNovaFeature`).
    3.  Faça o commit das suas alterações (`git commit -m 'Adiciona MinhaNovaFeature'`).
    4.  Faça o push para a sua branch (`git push origin feature/MinhaNovaFeature`).
    5.  Abra um [Pull Request](https://github.com/emn-f/voxai/pulls).

Considere também dar uma ⭐ ao projeto se você gostou da iniciativa!

## 🤖 Automação de Versionamento

O projeto utiliza **GitHub Actions** para automatizar o processo de criação de tags de versão.
* **Branch `dev`**: A cada `push`, uma nova tag `dev-vX.X.X` é criada, incrementando o número do patch.
* **Branch `master`**: A cada `push`, uma nova tag de produção `vX.X.X` é criada, também incrementando o patch.

Isso garante um controle de versão consistente e automatizado para os ambientes de desenvolvimento e produção.

## 🔒 Privacidade

Sua privacidade é nossa prioridade. **Nós não coletamos dados pessoais** como nome, IP ou localização. A interação é 100% anônima. Para saber mais, leia nossa [**Política de Privacidade**](PRIVACY_POLICY.md).

## 📝 Licença

Este projeto é licenciado sob a **Licença MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Equipe
O projeto VoxAI é desenvolvido por uma equipe multidisciplinar e dedicada:

* **Emanuel Ferreira** (Diretor do Vox)
* **Brenda Pires**
* **Fernanda Souza**
* **Alicia Batista**
* **Lucca Pertigas**
* **Kauã Araujo**
* **Marcio Ventura**

## 📬 Contato

Dúvidas, sugestões ou feedback? Fique à vontade para entrar em contato!

* **E-mail:** [assistentedeapoiolgbtvox@gmail.com](mailto:assistentedeapoiolgbtvox@gmail.com)
* **Instagram:** [@projetovoxai](https://www.instagram.com/projetovoxai/)
* **LinkedIn:** [Projeto Vox](https://www.linkedin.com/company/assistentevox/)
* **Linktree:** [linktr.ee/voxai](https://linktr.ee/voxai)

## 📝 Changelog

Para acompanhar todas as mudanças e atualizações do projeto, consulte o nosso [**CHANGELOG.md**](CHANGELOG.md).
