import re
import requests

API_URL = "http://127.0.0.1:5000"

print("=" * 40)
print("🤖 ASSISTENTE VIRTUAL BLIP DEMO")
print("=" * 40)

# Verifica se a API está online
try:

    requests.get(
        f"{API_URL}/pedidos",
        timeout=3
    )

    print("✅ API conectada com sucesso!")

except Exception:

    print("\n❌ Não foi possível conectar na API.")
    print("Verifique se o app.py está rodando.")
    print("\nExecute em outro terminal:")
    print("python app.py")

    exit()

while True:

    texto = input("\nVocê: ").lower().strip()

    # SAIR

    if texto == "sair":

        print("\nBot: Até logo!")

        break

    # LISTAR PEDIDOS

    elif (
        "listar" in texto
        or "mostrar" in texto
        or "listar pedidos" in texto
        or "mostrar pedidos" in texto
    ):

        try:

            response = requests.get(
                f"{API_URL}/pedidos"
            )

            pedidos = response.json()

            print("\n📦 PEDIDOS CADASTRADOS")

            for pedido in pedidos:

                print(
                    f"\nPedido: {pedido['id']}"
                )

                print(
                    f"Cliente: {pedido['cliente']}"
                )

                print(
                    f"Status: {pedido['status']}"
                )

        except Exception as erro:

            print(
                f"\n❌ Erro ao consultar API: {erro}"
            )

    # QUANTOS PEDIDOS EXISTEM

    elif (
        "quantos" in texto
        or "quantidade" in texto
    ):

        try:

            response = requests.get(
                f"{API_URL}/pedidos"
            )

            pedidos = response.json()

            print(
                f"\nBot: Existem {len(pedidos)} pedidos cadastrados."
            )

        except Exception as erro:

            print(
                f"\n❌ Erro: {erro}"
            )

    # CONSULTA DE PEDIDO

    elif "pedido" in texto:

        numeros = re.findall(
            r"\d+",
            texto
        )

        if not numeros:

            print(
                "\nBot: Informe o número do pedido."
            )

            continue

        pedido_id = numeros[0]

        try:

            response = requests.get(
                f"{API_URL}/pedido/{pedido_id}"
            )

            if response.status_code == 200:

                dados = response.json()

                print(
                    f"\nBot: O pedido {pedido_id} está '{dados['status']}'."
                )

            else:

                print(
                    "\nBot: Pedido não encontrado."
                )

        except Exception as erro:

            print(
                f"\n❌ Erro: {erro}"
            )

    # AJUDA

    elif (
        "ajuda" in texto
        or "help" in texto
    ):

        print("\n🤖 Posso ajudar com:")

        print("- listar pedidos")
        print("- mostrar pedidos")
        print("- quantos pedidos existem")
        print("- status do pedido 101")
        print("- pedido 102")
        print("- sair")

    # NÃO ENTENDI

    else:

        print(
            "\nBot: Não entendi sua solicitação."
        )

        print(
            "Digite 'ajuda' para ver exemplos."
        )