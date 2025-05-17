# Vox 🌈

**Vox** é um assistente de apoio e informação LGBTQIA+ desenvolvido como projeto de extensão universitária. Ele utiliza inteligência artificial para oferecer acolhimento, informações confiáveis e recursos úteis para a comunidade LGBTQIA+.


## 💡 Sobre o Projeto

O Vox foi criado por estudantes de diferentes áreas, com o objetivo de facilitar o acesso a informações, direitos e acolhimento para pessoas LGBTQIA+. O projeto também se baseia em uma pesquisa de extensão realizada com a comunidade, cujos resultados embasam as respostas do assistente.

## 🚀 Como usar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/vox.git
   cd vox
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure a chave da API Gemini:**
   Crie um arquivo `.streamlit/secrets.toml` com o conteúdo:
     ```
     GEMINI_API_KEY = "sua-chave-aqui"
     ```

4. **Execute o projeto:**
   ```bash
   streamlit run vox_ai.py
   ```

## 🏗️ Estrutura do Projeto

```
.
├── data/
│   ├── base.json
│   ├── info.py
│   ├── instrucoes.py
│   └── saudacao.py
├── src/
│   ├── persona.py
│   └── utils.py
├── .streamlit/
│   └── secrets.toml
├── requirements.txt
└── vox_ai.py
```

## 👥 Equipe

- 👑 Emanuel Arlan Sousa Silva Ferreira — Engenharia de Software (Líder)
- Alicia Santos Silva Batista — Direito
- Brenda Moreira Lobo Pires — Direito
- Fernanda Carvalho do Souza — Biomedicina
- Kauã Araujo Santos — Engenharia de Software
- Lucca Rievers Pertigas — Engenharia de Software
- Marcio Claudio Ventura Ferreira — Engenharia de Software

## 📬 Contato

Dúvidas, sugestões ou feedback?  
Entre em contato pelo e-mail: [assistentedeapoiolgbtvox@gmail.com](mailto:seu-email@exemplo.com)