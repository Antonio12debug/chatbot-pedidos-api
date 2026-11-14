from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/pedido/<int:id>")
def consultar_pedido(id):

    conn = sqlite3.connect("database/pedidos.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM pedidos WHERE id=?",
        (id,)
    )

    pedido = cursor.fetchone()

    conn.close()

    if pedido:
        return jsonify({
            "id": pedido[0],
            "cliente": pedido[1],
            "status": pedido[2]
        })

    return jsonify({
        "erro": "Pedido não encontrado"
    }), 404

if __name__ == "__main__":
    app.run(debug=True)