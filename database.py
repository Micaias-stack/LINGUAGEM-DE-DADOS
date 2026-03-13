import sqlite3
import os

def inicializar_banco():
    if not os.path.exists('data'):
        os.makedirs('data')
        
    conn = sqlite3.connect('data/arquitetura.db')
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
    conn = sqlite3.connect('data/arquitetura.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM languages")
    dados = cursor.fetchall()
    conn.close()
    return dados
