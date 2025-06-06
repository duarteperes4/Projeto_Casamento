import sqlite3
import os


DATABASE_PATH = os.path.join('database', 'database.db')

if not os.path.exists('database'):
    os.makedirs('database')

def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise


def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS casamento (
                id INTEGER PRIMARY KEY,
                data TEXT NOT NULL,
                local TEXT NOT NULL,
                hora TEXT NOT NULL
            )
        ''')

        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS convidados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                restricoes TEXT,
                confirmado TEXT
            )
        ''')

        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS musicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                tipo TEXT,
                horario TEXT
            )
        ''')

        
        cursor.execute('SELECT COUNT(*) FROM casamento')
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO casamento (id, data, local, hora)
                VALUES (1, '12 de Julho 2025', 'Quinta de Povos, Arouca', '12:00')
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


init_database()
