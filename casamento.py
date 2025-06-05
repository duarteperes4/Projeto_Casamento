import sqlite3
import os

# Caminho para o banco de dados dentro da pasta 'database'
DATABASE_PATH = os.path.join('database', 'database.db')

# Criar a pasta 'database' se não existir
if not os.path.exists('database'):
    os.makedirs('database')

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Função para inicializar o banco de dados
def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Criar a tabela 'casamento'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS casamento (
            id INTEGER PRIMARY KEY,
            data TEXT NOT NULL,
            local TEXT NOT NULL,
            hora TEXT NOT NULL
        )
    ''')

    # Verificar se a tabela está vazia e inserir dados iniciais
    cursor.execute('SELECT COUNT(*) FROM casamento')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO casamento (id, data, local, hora)
            VALUES (1, '12 de Julho de 2025', 'Quinta de Povos, Arouca', '12:00')
        ''')

    conn.commit()
    conn.close()

def get_casamento_details():
    conn = get_db_connection()
    casamento_info = conn.execute('SELECT * FROM casamento WHERE id = 1').fetchone()
    conn.close()
    return casamento_info


init_database()
