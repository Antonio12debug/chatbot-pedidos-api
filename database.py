import sqlite3
import os

os.makedirs("database", exist_ok=True)

conn = sqlite3.connect("database/pedidos.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY,
    cliente TEXT,
    status TEXT
)
""")

pedidos = [
    (101, "João", "Em transporte"),
    (102, "Maria", "Entregue"),
    (103, "Pedro", "Em separação")
]

for pedido in pedidos:
    cursor.execute("""
    INSERT OR IGNORE INTO pedidos
    VALUES (?, ?, ?)
    """, pedido)

conn.commit()

print("Banco criado com sucesso!")

conn.close()