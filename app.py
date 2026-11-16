from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)


def conectar():

    caminho = os.path.abspath("database/pedidos.db")

    print("\n===== BANCO UTILIZADO =====")
    print(caminho)

    return sqlite3.connect(caminho)

@app.route("/")
def home():
    return {
        "mensagem": "API de Pedidos Online"
    }


# LISTAR TODOS
@app.route("/pedidos", methods=["GET"])
def listar_pedidos():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM pedidos"
    )

    pedidos = cursor.fetchall()

    conn.close()

    resultado = []

    for pedido in pedidos:

        resultado.append({
            "id": pedido[0],
            "cliente": pedido[1],
            "status": pedido[2]
        })

    return jsonify(resultado)


# BUSCAR UM
@app.route("/pedido/<int:id>", methods=["GET"])
def buscar_pedido(id):

    conn = conectar()

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


# CRIAR
@app.route("/pedido", methods=["POST"])
def criar_pedido():

    dados = request.json

    print("\n===== DADOS RECEBIDOS =====")
    print(dados)

    conn = conectar()

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO pedidos (id, cliente, status)
            VALUES (?, ?, ?)
            """,
            (
                dados["id"],
                dados["cliente"],
                dados["status"]
            )
        )

        conn.commit()

        print("✅ Pedido inserido com sucesso!")

        return jsonify({
            "mensagem": "Pedido criado com sucesso"
        }), 201

    except Exception as e:

        print("❌ ERRO AO INSERIR:")
        print(e)

        return jsonify({
            "erro": str(e)
        }), 500

    finally:

        conn.close()


# ATUALIZAR
@app.route("/pedido/<int:id>", methods=["PUT"])
def atualizar_pedido(id):

    dados = request.json

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE pedidos
        SET status = ?
        WHERE id = ?
        """,
        (
            dados["status"],
            id
        )
    )

    conn.commit()

    conn.close()

    return jsonify({
        "mensagem": "Pedido atualizado"
    })


# EXCLUIR
@app.route("/pedido/<int:id>", methods=["DELETE"])
def remover_pedido(id):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM pedidos
        WHERE id = ?
        """,
        (id,)
    )

    conn.commit()

    conn.close()

    return jsonify({
        "mensagem": "Pedido removido"
    })


if __name__ == "__main__":
    app.run(debug=True)