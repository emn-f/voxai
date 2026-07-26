# Plano de Melhoria de Arquitetura e Engenharia: Vox AI

Este documento detalha o planejamento técnico para corrigir os pontos críticos de arquitetura e engenharia identificados no Vox AI, visando escalabilidade, testabilidade e alto desempenho.

---

## 1. Desacoplamento da Lógica de Negócios da Interface (UI)
* **Objetivo:** Adotar os princípios de *Clean Architecture* ou Arquitetura Hexagonal (Ports and Adapters) para separar totalmente o framework Streamlit da lógica interna.
* **Ações:**
  1. **Remover st das Camadas Core:** Eliminar todas as referências diretas a `streamlit`, `st.session_state`, `st.cache_resource` e `st.error` dos arquivos dentro de `src/core/`.
  2. **Inversão de Dependências:** Criar interfaces claras para o cliente do banco de dados e o cliente da IA. O Streamlit (em `vox_ai.py`) deve atuar apenas como o "orquestrador de entrada/saída", instanciando e injetando dependências.
  3. **Tratamento de Erros:** As funções core devem lançar exceções customizadas (ex: `DatabaseConnectionError`, `GenAPIQuotaError`) em vez de travar o fluxo com `st.stop()` ou desenhar alertas na tela diretamente. A camada do Streamlit captura essas exceções e decide como exibir o erro amigável ao usuário.

---

## 2. Otimização de Latência e Desempenho
* **Objetivo:** Reduzir o tempo médio de resposta de ~17 segundos para patamares abaixo de 3 segundos na primeira resposta.
* **Ações:**
  1. **Cache Semântico (Semantic Caching):** Implementar um banco de dados de cache rápido (ex: Redis ou tabela indexada no Supabase). Antes de realizar a busca no RAG e chamar a API do Gemini, o sistema busca o embedding da pergunta no cache semântico. Se houver uma similaridade maior que 0.96 com uma consulta anterior, a resposta já gravada é retornada instantaneamente.
  2. **Conexões em Pool:** Ativar o Supavisor do Supabase na porta de pooling de conexões (porta 6543) para mitigar a latência de abertura de sockets a cada requisição de banco de dados.
  3. **Geração Assíncrona e Stream Real:** Garantir a entrega imediata das respostas utilizando o processamento assíncrono nativo (`asyncio` em Python) para realizar chamadas simultâneas de log e auditoria em segundo plano, liberando o fluxo de texto para o usuário mais rapidamente.

---

## 3. Mitigação do Inchaço de Prompt (Prompt Bloating)
* **Objetivo:** Reduzir o volume de tokens redundantes injetados nos prompts e diminuir a latência do LLM.
* **Ações:**
  1. **Algoritmo de Re-ranking:** Introduzir um modelo de re-ranker (ex: Cohere Rerank ou modelo cross-encoder leve rodando localmente). A busca inicial vetorial recupera 15-20 chunks, o re-ranker reordena e seleciona apenas os 3 a 5 mais semanticamente adequados à pergunta do usuário, descartando dados redundantes.
  2. **Limitação Estrita do Contexto Adaptativo:** Ajustar o gatilho de "Contexto Expandido". Em vez de recuperar todos os chunks de um tópico vencedor indiscriminadamente até `MAX_CHUNCK=25` (o que inunda o prompt), estabelecer um teto rígido de, no máximo, 6 chunks, mantendo a coesão sem sobrecarregar a janela de contexto.

---

## 4. Segurança em Camadas (Defense-in-Depth)
* **Objetivo:** Blindar o sistema contra técnicas avançadas de *jailbreak* e tentativas de contornar as diretrizes de segurança.
* **Ações:**
  1. **Gateway de Entrada (Input Firewall):** Implementar um classificador rápido (utilizando um modelo menor e econômico como o `gemini-3.1-flash-lite` ou uma rede neural de classificação local) rodando *antes* do pipeline de RAG. Esse gateway analisa se o input do usuário viola as políticas de segurança ou foge do escopo do projeto, bloqueando o ataque imediatamente sem gastar processamento no banco ou no LLM principal.
  2. **Validação de Saída (Output Guardrails):** Implementar um validador de saída simples para garantir que a resposta gerada não contenha informações de dados pessoais (PII) vazadas por falha ou alucinação do modelo, garantindo conformidade rigorosa com a LGPD.
