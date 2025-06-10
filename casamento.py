import sqlite3
import os
from datetime import datetime

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

        # Criar a tabela 'catering'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS catering (
                id INTEGER PRIMARY KEY,
                menu TEXT NOT NULL,
                numero_convidados INTEGER NOT NULL,
                observacoes TEXT,
                data_atualizacao TEXT NOT NULL
            )
        ''')

        # Verificar se a tabela 'casamento' está vazia e inserir dados iniciais
        cursor.execute('SELECT COUNT(*) FROM casamento')
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO casamento (id, data, local, hora)
                VALUES (1, '12 de Julho de 2025', 'Quinta de Povos, Arouca', '12:00')
            ''')

        # Verificar se a tabela 'catering' está vazia e inserir dados iniciais (exemplo inicial)
        cursor.execute('SELECT COUNT(*) FROM catering')
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO catering (id, menu, numero_convidados, observacoes, data_atualizacao)
                VALUES (1, '', 0, '', ?)
            ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),))  # Valores iniciais vazios

        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
        conn.rollback()
    finally:
        conn.close()

# Função para buscar os detalhes do casamento
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

# Função para buscar os detalhes do catering
def get_catering():
    conn = get_db_connection()
    try:
        catering = conn.execute('SELECT * FROM catering WHERE id = 1').fetchone()
        return catering
    except sqlite3.Error as e:
        print(f"Erro ao buscar detalhes do catering: {e}")
        return None
    finally:
        conn.close()

# Função para atualizar os detalhes do catering
def atualizar_catering(menu, numero_convidados, observacoes, data_atualizacao):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE catering
            SET menu = ?, numero_convidados = ?, observacoes = ?, data_atualizacao = ?
            WHERE id = 1
        ''', (menu, numero_convidados, observacoes, data_atualizacao))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao atualizar catering: {e}")
        conn.rollback()
    finally:
        conn.close()

# Função para buscar a lista de convidados
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

# Função para adicionar um novo convidado
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

# Função para buscar a lista de DJ's e músicos
def get_musicos():
    conn = get_db_connection()
    try:
        musicos_list = conn.execute('SELECT * FROM musicos').fetchall()
        return musicos_list
    except sqlite3.Error as e:
        print(f"Erro ao buscar músicos: {e}")
        return []
    finally:
        conn.close()

# Função para adicionar um novo DJ/músico
def adicionar_musico(nome, tipo, horario):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO musicos (nome, tipo, horario)
            VALUES (?, ?, ?)
        ''', (nome, tipo, horario))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao adicionar músico: {e}")
        conn.rollback()
    finally:
        conn.close()

# Função para adicionar um novo feedback
def adicionar_feedback(nome, comentario, data_envio):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO feedback (nome, comentario, data_envio)
            VALUES (?, ?, ?)
        ''', (nome, comentario, data_envio))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao adicionar feedback: {e}")
        conn.rollback()
    finally:
        conn.close()

# Função para obter o orçamento final
def get_orcamento_final():
    conn = get_db_connection()
    try:
        orcamento = conn.execute('SELECT * FROM orcamento_final WHERE id = 1').fetchone()
        return orcamento
    except sqlite3.Error as e:
        print(f"Erro ao buscar orçamento final: {e}")
        return None
    finally:
        conn.close()

def atualizar_orcamento_final(catering, decoracao, fotografia, musica, outros, total, data_atualizacao):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE orcamento_final
            SET catering = ?, decoracao = ?, fotografia = ?, musica = ?, outros = ?, total = ?, data_atualizacao = ?
            WHERE id = 1
        ''', (catering, decoracao, fotografia, musica, outros, total, data_atualizacao))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao atualizar orçamento final: {e}")
        conn.rollback()
    finally:
        conn.close()

# Função para obter os detalhes do catering
def get_catering():
    conn = get_db_connection()
    try:
        catering = conn.execute('SELECT * FROM catering WHERE id = 1').fetchone()
        return catering
    except sqlite3.Error as e:
        print(f"Erro ao buscar detalhes do catering: {e}")
        return None
    finally:
        conn.close()

# Função para atualizar os detalhes do catering
def atualizar_catering(menu, numero_convidados, observacoes, data_atualizacao):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE catering
            SET menu = ?, numero_convidados = ?, observacoes = ?, data_atualizacao = ?
            WHERE id = 1
        ''', (menu, numero_convidados, observacoes, data_atualizacao))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao atualizar catering: {e}")
        conn.rollback()
    finally:
        conn.close()


init_database()