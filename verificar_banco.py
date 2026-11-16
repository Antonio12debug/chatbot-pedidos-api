import sqlite3

conn = sqlite3.connect("database/pedidos.db")

cursor = conn.cursor()

cursor.execute("SELECT * FROM pedidos")

pedidos = cursor.fetchall()

print("PEDIDOS NO BANCO:")

for pedido in pedidos:
    print(pedido)

conn.close()