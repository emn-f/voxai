import json
import mysql.connector

# Configurações da conexão com o banco
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Eassf.6912",
    database="vox"
)

cursor = conexao.cursor()

# Apagar dados das tabelas, mantendo a estrutura
cursor.execute("DELETE FROM referencias")
cursor.execute("DELETE FROM temas")

# Resetar AUTO_INCREMENT (opcional)
cursor.execute("ALTER TABLE referencias AUTO_INCREMENT = 1")
cursor.execute("ALTER TABLE temas AUTO_INCREMENT = 1")

# Carregar o JSON
with open("fonte.json", encoding="utf-8") as f:
    data = json.load(f)

# Inserir os dados
for item in data:
    tema = item['tema']
    descricao = item['descricao']

    cursor.execute("INSERT INTO temas (tema, descricao) VALUES (%s, %s)", (tema, descricao))
    tema_id = cursor.lastrowid

    for ref in item.get('referencias', []):
        cursor.execute("INSERT INTO referencias (tema_id, referencia) VALUES (%s, %s)", (tema_id, ref))

# Salvar e fechar
conexao.commit()
cursor.close()
conexao.close()

print("✅ Dados atualizados com sucesso no banco 'vox'.")
