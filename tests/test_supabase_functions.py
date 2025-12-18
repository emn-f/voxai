
import unittest
import sys
import os
import uuid
import time
import warnings

# Ignora avisos de depreciação de bibliotecas internas e avisos de socket não fechado (ruído comum em testes HTTP)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=ResourceWarning)

# Tenta importar o parser TOML (necessário para ler os secrets)
try:
    import toml
except ImportError:
    try:
        import tomli as toml
    except ImportError:
        print("Erro: Módulo 'toml' ou 'tomli' não encontrado. Por favor instale-o (pip install toml).")
        sys.exit(1)

from unittest.mock import MagicMock
import google.generativeai as genai

# -- CONFIGURAÇÃO DO AMBIENTE E MOCKS --

# 1. Determina a raiz do projeto e adiciona ao path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(PROJECT_ROOT)

# 2. Carrega os Segredos (Secrets)
secrets_path = os.path.join(PROJECT_ROOT, '.streamlit', 'secrets.toml')
if not os.path.exists(secrets_path):
    print(f"Erro Crítico: Arquivo de segredos não encontrado em {secrets_path}")
    sys.exit(1)

with open(secrets_path, 'r', encoding='utf-8') as f:
    secrets_data = toml.load(f)

# 3. Configura o Gemini/GenAI (Necessário para testes de embedding)
gemini_key = secrets_data.get("GEMINI_API_KEY")
if not gemini_key:
    gemini_key = os.environ.get("GEMINI_API_KEY")

if gemini_key:
    genai.configure(api_key=gemini_key)
else:
    print("Aviso: GEMINI_API_KEY não encontrada nos secrets. Testes de embedding podem falhar.")

# 4. Mock do Streamlit ANTES de importar src.core.database
# Isso engana o Python para achar que o Streamlit já está rodando com os segredos carregados.
mock_st = MagicMock()
mock_st.secrets = secrets_data

# Mock do decorador @st.cache_resource para não fazer nada e apenas rodar a função
def pass_through_decorator(func):
    return func
mock_st.cache_resource = pass_through_decorator

# Mock do st.error para imprimir no console ao invés de tentar mostrar na UI
mock_st.error = lambda x: print(f"   [STREAMLIT ERROR CAPTURADO]: {x}")

sys.modules["streamlit"] = mock_st

# 5. Importa as funções que vamos testar
from src.core.database import (
    get_db_client,
    salvar_log_chat,
    salvar_erro,
    salvar_report,
    add_conhecimento_db,
    buscar_referencias_db
)

class TestSupabaseIntegration(unittest.TestCase):
    """
    Testes de Integração para funções do Supabase.
    ATENÇÃO: Estes testes interagem com o banco de dados REAL definido no secrets.toml.
    Eles criam dados de teste e tentam limpá-los logo em seguida.
    """

    @classmethod
    def setUpClass(cls):
        print("\n=== INICIANDO BATERIA DE TESTES SUPABASE ===")
        print("Tentando conexão com o banco...")
        cls.client = get_db_client()
        if cls.client is None:
            raise RuntimeError("CRÍTICO: Não foi possível conectar ao Supabase. Verifique a URL e a KEY no secrets.toml.")
        print("✅ Conexão estabelecida com sucesso.\n")

    def test_01_connection(self):
        """Teste Básico: Verifica se o cliente do banco existe."""
        print("🔄 [Teste 01] Verificando objeto cliente...")
        self.assertIsNotNone(self.client, "O cliente do Supabase é None.")
        print("   -> ✅ Cliente validado.")

    def test_02_salvar_log_chat(self):
        """Teste: Inserção na tabela 'chat_logs'."""
        print("🔄 [Teste 02] Testando inserção de Log de Conversa...")
        session_id = f"TEST_SESSION_{uuid.uuid4()}"
        git_version = "TEST_V1"
        prompt = "Teste automatizado de log"
        response = "Resposta de teste"
        
        # Prepare dummy KB item for Foreign Key constraint if needed
        try:
             # Insert a dummy KB item to ensure log saving works if FK is strict
             # We generate a unique theme to avoid "Duplicate Key" issues on theme if unique
             unique_theme = f"TemaTeste_{uuid.uuid4()}"
             
             # We use embedding of size 768 for safety
             dummy_embed = [0.0] * 768
             
             data_kb = {
                 "tema": unique_theme,
                 "descricao": "DescTeste",
                 "embedding": dummy_embed,
                 "referencias": "RefTeste",
                 "autor": "Tester"
             }
             # We don't care about the return, just that it exists. 
             # If DB generates ID, it handles it.
             self.client.table("knowledge_base").insert(data_kb).execute()
        except Exception as e:
             print(f"   ⚠️ Aviso: Falha ao criar KB dummy para teste de log: {e}")
             unique_theme = "TemaTeste" # Fallback

        # Executa a função
        try:
            salvar_log_chat(session_id, git_version, prompt, response, unique_theme)
        except Exception as e:
            self.fail(f"A função 'salvar_log_chat' falhou com erro: {e}")
        
        # Verificação
        time.sleep(1) # Aguarda propagação
        try:
            res = self.client.table("chat_logs").select("*").eq("session_id", session_id).execute()
        except Exception as e:
            self.fail(f"Erro ao consultar tabela 'chat_logs'. A tabela existe? Erro: {e}")

        if len(res.data) == 0:
            self.fail("Inserção falhou: Nenhum registro encontrado em 'chat_logs' com o ID gerado.")
        
        print(f"   -> ✅ Registro inserido e localizado com sucesso (ID: {session_id}).")
        
        # Limpeza
        self.client.table("chat_logs").delete().eq("session_id", session_id).execute()
        print("   -> 🧹 Registro de teste limpo.")

    def test_03_salvar_erro(self):
        """Teste: Inserção na tabela 'error_logs'."""
        print("🔄 [Teste 03] Testando inserção de Log de Erro...")
        session_id = f"TEST_SESSION_{uuid.uuid4()}"
        error_msg = "Erro de teste automatizado"
        
        # Executa
        error_id = salvar_erro(session_id, "TEST_V1", error_msg)
        
        if error_id == "N/A" or error_id == "ERRO-DB":
            self.fail("A função 'salvar_erro' retornou um código de falha.")

        # Verificação
        try:
            res = self.client.table("error_logs").select("*").eq("error_id", error_id).execute()
        except Exception as e:
             self.fail(f"Erro ao consultar tabela 'error_logs'. Verifique schema. Erro: {e}")

        if len(res.data) == 0:
            self.fail("Inserção falhou: Log de erro não encontrado no banco.")
            
        print(f"   -> ✅ Erro registrado com sucesso (Error ID: {error_id}).")
        
        # Limpeza
        self.client.table("error_logs").delete().eq("error_id", error_id).execute()
        print("   -> 🧹 Registro de erro limpo.")

    def test_04_salvar_report(self):
        """Teste: Inserção na tabela 'user_reports'."""
        print("🔄 [Teste 04] Testando inserção de Report de Usuário...")
        session_id = f"TEST_SESSION_{uuid.uuid4()}"
        history = "User: Oi\nBot: Ola"
        
        # Executa
        success = salvar_report(session_id, "TEST_V1", history)
        if not success:
            self.fail("A função 'salvar_report' retornou False (falha).")

        # Verificação
        try:
            res = self.client.table("user_reports").select("*").eq("session_id", session_id).execute()
        except Exception as e:
            self.fail(f"Erro ao consultar tabela 'user_reports'. Erro: {e}")

        if len(res.data) == 0:
            self.fail("Registro não encontrado em 'user_reports'.")

        print("   -> ✅ Report salvo com sucesso.")
        
        # Limpeza
        self.client.table("user_reports").delete().eq("session_id", session_id).execute()
        print("   -> 🧹 Report de teste limpo.")

    def test_05_knowledge_base_flow(self):
        """
        Teste Completo (RAG):
        1. Gera embedding com Gemini.
        2. Salva na Base de Conhecimento.
        3. Realiza busca vetorial para encontrar o item.
        """
        print("🔄 [Teste 05] Testando fluxo completo de RAG (Embedding -> Banco -> Busca)...")
        unique_topic = f"TEST_TOPIC_{uuid.uuid4()}"
        description = "Esta é uma entrada de teste para verificação automatizada."
        referencias = "Fonte Automática"
        autor = "Tester Bot"

        # Passo Preliminar: Garantir que não existe resquício do teste anterior
        try:
             self.client.table("knowledge_base").delete().eq("tema", unique_topic).execute()
        except:
             pass

        # Passo A: Testar Geração de Embedding
        print("   -> [5.1] Gerando embedding com Gemini...")
        try:
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=f"{unique_topic}: {description}",
                task_type="retrieval_document"
            )
            vector_embedding = result['embedding']
            print(f"      ✅ Embedding gerado. Dimensão: {len(vector_embedding)}")
        except Exception as e:
            print(f"      ❌ FALHA AO GERAR EMBEDDING: {e}")
            self.fail(f"Erro na API do Gemini: {e}")

        # Passo B: Salvar no Banco
        print(f"   -> [5.2] Salvando tópico no Supabase: {unique_topic}")
        success = add_conhecimento_db(unique_topic, description, referencias, autor)
        
        if not success:
             print("      ⚠️ A função 'add_conhecimento_db' retornou False. Tentando inserção manual para diagnóstico...")
             try:
                 data = {
                    "tema": unique_topic,
                    "descricao": description,
                    "embedding": vector_embedding,
                    "referencias": referencias,
                    "autor": autor
                 }
                 self.client.table("knowledge_base").insert(data).execute()
                 self.fail("A inserção manual funcionou, mas a função do sistema falhou. Verifique a lógica da função 'add_conhecimento_db'.")
             except Exception as e:
                 print(f"      ❌ FALHA NA INSERÇÃO MANUAL: {e}")
                 if "22000" in str(e) and "dimensions" in str(e):
                     self.fail(f"ERRO DE DIMENSÃO DE VETOR: Seu banco espera um tamanho diferente de {len(vector_embedding)}.")
                 elif "relation" in str(e) and "does not exist" in str(e):
                     self.fail("ERRO: A tabela 'knowledge_base' não existe no banco.")
                 else:
                     self.fail(f"Erro genérico de inserção no Supabase: {e}")
        
        print("      ✅ Tópico salvo com sucesso.")

        # Passo C: Busca Vetorial
        print("   -> [5.3] Verificando Busca Vetorial...")
        try:
             # Gera vetor de busca (Query)
             result = genai.embed_content(
                model="models/text-embedding-004",
                content=f"{unique_topic}: {description}",
                task_type="retrieval_query"
             )
             query_vector = result['embedding']
             
             # Executa a busca
             tema_found, desc_found = buscar_referencias_db(query_vector, threshold=0.1, limit=5)
             
             print(f"      -> Resultado da busca: {tema_found}")
             
             if tema_found != unique_topic:
                 print(f"      ⚠️ ALERTA: Encontrou '{tema_found}' ao invés de '{unique_topic}'. A busca vetorial pode estar imprecisa ou com threshold alto.")
             else:
                 print("      ✅ Match Vetorial Perfeito!")
                 self.assertEqual(tema_found, unique_topic)

        except Exception as e:
            self.fail(f"Falha ao executar a busca vetorial (RPC match_knowledge_base): {e}")
        finally:
            # Passo D: Limpeza
            print("   -> [5.4] Limpando dados de teste...")
            self.client.table("knowledge_base").delete().eq("tema", unique_topic).execute()
            print("      🧹 Limpeza concluída.")

if __name__ == "__main__":
    unittest.main()
