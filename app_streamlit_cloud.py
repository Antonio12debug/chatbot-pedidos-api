import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import re
import os

def criar_banco():

    os.makedirs(
        "database",
        exist_ok=True
    )

    conn = sqlite3.connect(
        "database/pedidos.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY,
        cliente TEXT,
        status TEXT
    )
    """)

    pedidos_iniciais = [
        (101, "João", "Em transporte"),
        (102, "Maria", "Entregue"),
        (103, "Pedro", "Em separação")
    ]

    for pedido in pedidos_iniciais:

        cursor.execute(
            """
            INSERT OR IGNORE INTO pedidos
            VALUES (?, ?, ?)
            """,
            pedido
        )

    conn.commit()

    conn.close()

def conectar():
    return sqlite3.connect(
        "database/pedidos.db"
    )


def listar_pedidos():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM pedidos"
    )

    pedidos = cursor.fetchall()

    conn.close()

    return pedidos


def buscar_pedido(id_pedido):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM pedidos WHERE id=?",
        (id_pedido,)
    )

    pedido = cursor.fetchone()

    conn.close()

    return pedido


def criar_pedido(
    id_pedido,
    cliente,
    status
):

    try:

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO pedidos
            VALUES (?, ?, ?)
            """,
            (
                id_pedido,
                cliente,
                status
            )
        )

        conn.commit()

        conn.close()

        return True

    except:

        return False


def atualizar_pedido(
    id_pedido,
    status
):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE pedidos
        SET status=?
        WHERE id=?
        """,
        (
            status,
            id_pedido
        )
    )

    conn.commit()

    conn.close()


def remover_pedido(
    id_pedido
):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM pedidos
        WHERE id=?
        """,
        (id_pedido,)
    )

    conn.commit()

    conn.close()

criar_banco()
st.set_page_config(
    page_title="Assistente Virtual",
    page_icon="🤖",
    layout="wide"
)

st.title(
    "🤖 Assistente Virtual Blip Demo"
)

pedidos = listar_pedidos()

df = pd.DataFrame(
    pedidos,
    columns=[
        "id",
        "cliente",
        "status"
    ]
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "📦 Pedidos",
    len(df)
)

col2.metric(
    "✅ Entregues",
    len(
        df[
            df["status"] == "Entregue"
        ]
    )
)

col3.metric(
    "🚚 Transporte",
    len(
        df[
            df["status"].str.contains(
                "transporte",
                case=False,
                na=False
            )
        ]
    )
)

grafico = px.bar(
    df["status"].value_counts().reset_index(),
    x="status",
    y="count",
    title="Pedidos por Status"
)

st.plotly_chart(
    grafico,
    use_container_width=True
)

st.subheader(
    "📋 Pedidos"
)

st.dataframe(
    df,
    use_container_width=True
)

pergunta = st.chat_input(
    "Digite sua mensagem..."
)

if pergunta:

    texto = pergunta.lower()

    resposta = ""

    if (
        "listar" in texto
        or "mostrar" in texto
    ):

        resposta = df.to_string(
            index=False
        )

    elif texto.startswith(
        "criar pedido"
    ):

        numeros = re.findall(
            r"\d+",
            texto
        )

        if numeros:

            pedido_id = int(
                numeros[0]
            )

            partes = pergunta.split()

            cliente = partes[3]

            status = " ".join(
                partes[4:]
            )

            sucesso = criar_pedido(
                pedido_id,
                cliente,
                status
            )

            if sucesso:

                resposta = (
                    "✅ Pedido criado."
                )

            else:

                resposta = (
                    "⚠️ Pedido já existe."
                )

    elif texto.startswith(
        "atualizar pedido"
    ):

        numeros = re.findall(
            r"\d+",
            texto
        )

        if numeros:

            pedido_id = int(
                numeros[0]
            )

            partes = pergunta.split()

            status = " ".join(
                partes[3:]
            )

            atualizar_pedido(
                pedido_id,
                status
            )

            resposta = (
                "✏️ Pedido atualizado."
            )

    elif texto.startswith(
        "remover pedido"
    ):

        numeros = re.findall(
            r"\d+",
            texto
        )

        if numeros:

            remover_pedido(
                int(numeros[0])
            )

            resposta = (
                "🗑️ Pedido removido."
            )

    elif "pedido" in texto:

        numeros = re.findall(
            r"\d+",
            texto
        )

        if numeros:

            pedido = buscar_pedido(
                int(numeros[0])
            )

            if pedido:

                resposta = (
                    f"Pedido {pedido[0]} está "
                    f"{pedido[2]}"
                )

            else:

                resposta = (
                    "Pedido não encontrado."
                )

    else:

        resposta = (
            "Digite:\n"
            "- listar pedidos\n"
            "- pedido 101\n"
            "- criar pedido 300 Antonio Em transporte\n"
            "- atualizar pedido 300 Entregue\n"
            "- remover pedido 300"
        )

    st.chat_message(
        "assistant"
    ).markdown(
        resposta
    )