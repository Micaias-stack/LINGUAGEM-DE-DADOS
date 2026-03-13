import sqlite3

def inicializar_banco():
    # Removemos a criação da pasta 'data/' para salvar na raiz
    conn = sqlite3.connect('arquitetura.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS languages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            creator TEXT,
            year INTEGER,
            difficulty TEXT
        )
    ''')
    conn.commit()
    conn.close()

def listar_linguagens():
    conn = sqlite3.connect('arquitetura.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM languages")
    dados = cursor.fetchall()
    conn.close()
    return dados
    def salvar_linguagem(nome, criador, ano, dificuldade):
    conn = sqlite3.connect('arquitetura.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO languages (name, creator, year, difficulty)
        VALUES (?, ?, ?, ?)
    ''', (nome, criador, ano, dificuldade))
    conn.commit()
    conn.close()

