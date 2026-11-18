import streamlit as st
import requests
import re
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:5000"

st.set_page_config(
    page_title="Assistente Blip Demo",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Assistente Virtual")

# ==========================
# MÉTRICAS E DASHBOARD
# ==========================

try:

    response = requests.get(
        f"{API_URL}/pedidos"
    )

    pedidos = response.json()

    total_pedidos = len(pedidos)

    entregues = len(
        [
            p for p in pedidos
            if p["status"].lower() == "entregue"
        ]
    )

    transporte = len(
        [
            p for p in pedidos
            if "transporte" in p["status"].lower()
        ]
    )

    separacao = len(
        [
            p for p in pedidos
            if "separação" in p["status"].lower()
        ]
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📦 Total",
        total_pedidos
    )

    col2.metric(
        "✅ Entregues",
        entregues
    )

    col3.metric(
        "🚚 Transporte",
        transporte
    )

    col4.metric(
        "📋 Separação",
        separacao
    )

    dados_grafico = pd.DataFrame({
        "Status": [
            "Entregue",
            "Transporte",
            "Separação"
        ],
        "Quantidade": [
            entregues,
            transporte,
            separacao
        ]
    })

    grafico = px.bar(
        dados_grafico,
        x="Status",
        y="Quantidade",
        color="Status",
        title="Pedidos por Status"
    )

    st.plotly_chart(
        grafico,
        use_container_width=True
    )

    st.subheader("📋 Pedidos Cadastrados")

    tabela_pedidos = pd.DataFrame(
        pedidos
    )

    tabela_pedidos = tabela_pedidos.rename(
        columns={
            "id": "Pedido",
            "cliente": "Cliente",
            "status": "Status"
        }
    )

    st.dataframe(
        tabela_pedidos,
        use_container_width=True,
        hide_index=True
    )
except Exception:

    st.error(
        "Não foi possível carregar métricas."
    )

st.caption(
    "Simulação de chatbot conectado à API Flask."
)

# ==========================
# HISTÓRICO
# ==========================

if "mensagens" not in st.session_state:

    st.session_state.mensagens = []

for msg in st.session_state.mensagens:

    with st.chat_message(msg["tipo"]):

        st.markdown(msg["texto"])

# ==========================
# CHAT
# ==========================

pergunta = st.chat_input(
    "Digite sua mensagem..."
)

if pergunta:

    st.session_state.mensagens.append(
        {
            "tipo": "user",
            "texto": pergunta
        }
    )

    with st.chat_message("user"):

        st.markdown(pergunta)

    resposta = ""

    texto = pergunta.lower()

    try:

        # LISTAR PEDIDOS
        if (
            "listar" in texto
            or "mostrar" in texto
        ):

            response = requests.get(
                f"{API_URL}/pedidos"
            )

            pedidos = response.json()

            resposta = "### 📦 Pedidos cadastrados\n\n"

            for pedido in pedidos:

                resposta += (
                    f"**Pedido {pedido['id']}**\n\n"
                    f"Cliente: {pedido['cliente']}\n\n"
                    f"Status: {pedido['status']}\n\n"
                )

        # QUANTOS PEDIDOS
        elif "quantos" in texto:

            response = requests.get(
                f"{API_URL}/pedidos"
            )

            pedidos = response.json()

            resposta = (
                f"Existem {len(pedidos)} pedidos cadastrados."
            )

        # CRIAR PEDIDO
        elif texto.startswith("criar pedido"):

            numeros = re.findall(r"\d+", texto)

            if numeros:

                pedido_id = int(numeros[0])

                partes = pergunta.split()

                cliente = partes[3]

                status = " ".join(
                    partes[4:]
                )

                response = requests.post(
                    f"{API_URL}/pedido",
                    json={
                        "id": pedido_id,
                        "cliente": cliente,
                        "status": status
                    }
                )

                if response.status_code == 201:

                    resposta = (
                        f"✅ Pedido {pedido_id} criado com sucesso."
                    )

                else:

                    erro = response.json()

                    resposta = (
                        f"⚠️ {erro['erro']}"
                    )

            else:

                resposta = (
                    "Informe o número do pedido."
                )

        # ATUALIZAR PEDIDO
        elif texto.startswith("atualizar pedido"):

            numeros = re.findall(r"\d+", texto)

            if numeros:

                pedido_id = numeros[0]

                partes = pergunta.split()

                novo_status = " ".join(
                    partes[3:]
                )

                requests.put(
                    f"{API_URL}/pedido/{pedido_id}",
                    json={
                        "status": novo_status
                    }
                )

                resposta = (
                    f"✏️ Pedido {pedido_id} atualizado."
                )

            else:

                resposta = (
                    "Informe o número do pedido."
                )

        # REMOVER PEDIDO
        elif texto.startswith("remover pedido"):

            numeros = re.findall(
                r"\d+",
                texto
            )

            if numeros:

                pedido_id = numeros[0]

                requests.delete(
                    f"{API_URL}/pedido/{pedido_id}"
                )

                resposta = (
                    f"🗑️ Pedido {pedido_id} removido."
                )

            else:

                resposta = (
                    "Informe o número do pedido."
                )

        # CONSULTAR PEDIDO
        elif "pedido" in texto:

            numeros = re.findall(
                r"\d+",
                texto
            )

            if numeros:

                pedido_id = numeros[0]

                response = requests.get(
                    f"{API_URL}/pedido/{pedido_id}"
                )

                if response.status_code == 200:

                    dados = response.json()

                    resposta = (
                        f"O pedido {pedido_id} está "
                        f"**{dados['status']}**."
                    )

                else:

                    resposta = (
                        f"⚠️ O pedido {pedido_id} não foi encontrado."
                    )

            else:

                resposta = (
                    "Informe o número do pedido."
                )

        else:

            resposta = (
                "Posso ajudar com:\n\n"
                "- listar pedidos\n"
                "- pedido 101\n"
                "- criar pedido 300 Antonio Em transporte\n"
                "- atualizar pedido 300 Entregue\n"
                "- remover pedido 300\n"
                "- quantos pedidos existem"
            )

    except Exception as erro:

        resposta = (
            f"Erro:\n\n{erro}"
        )

    st.session_state.mensagens.append(
        {
            "tipo": "assistant",
            "texto": resposta
        }
    )

    with st.chat_message("assistant"):

        st.markdown(resposta)