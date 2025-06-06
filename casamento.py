import sqlite3
import os

# Caminho para o banco de dados dentro da pasta 'database'
DATABASE_PATH = os.path.join('database', 'database.db')

# Criar a pasta 'database' se não existir
if not os.path.exists('database'):
    os.makedirs('database')

# Função para conectar ao banco de dados
def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise

# Função para inicializar o banco de dados
def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Criar a tabela 'casamento'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS casamento (
                id INTEGER PRIMARY KEY,
                data TEXT NOT NULL,
                local TEXT NOT NULL,
                hora TEXT NOT NULL
            )
        ''')

        # Criar a tabela 'convidados'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS convidados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                restricoes TEXT,
                confirmado TEXT
            )
        ''')

        # Verificar se a tabela 'casamento' está vazia e inserir dados iniciais
        cursor.execute('SELECT COUNT(*) FROM casamento')
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO casamento (id, data, local, hora)
                VALUES (1, '15 de Agosto de 2025', 'Quinta das Flores, Lisboa', '16:00')
            ''')

        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
        conn.rollback()
    finally:
        conn.close()


def get_casamento_details():
    conn = get_db_connection()
    try:
        casamento_info = conn.execute('SELECT * FROM casamento WHERE id = 1').fetchone()
        return casamento_info
    except sqlite3.Error as e:
        print(f"Erro ao buscar detalhes do casamento: {e}")
        return None
    finally:
        conn.close()

def get_convidados():
    conn = get_db_connection()
    try:
        convidados_list = conn.execute('SELECT * FROM convidados').fetchall()
        return convidados_list
    except sqlite3.Error as e:
        print(f"Erro ao buscar convidados: {e}")
        return []
    finally:
        conn.close()

def adicionar_convidado(nome, restricoes, confirmado):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO convidados (nome, restricoes, confirmado)
            VALUES (?, ?, ?)
        ''', (nome, restricoes, confirmado))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao adicionar convidado: {e}")
        conn.rollback()
    finally:
        conn.close()


init_database()
