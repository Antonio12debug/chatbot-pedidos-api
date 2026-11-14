import requests

while True:

    pedido = input(
        "\nDigite o número do pedido (ou 'sair'): "
    )

    if pedido.lower() == "sair":
        print("\nEncerrando chatbot...")
        break

    response = requests.get(
        f"http://127.0.0.1:5000/pedido/{pedido}"
    )

    if response.status_code == 200:

        dados = response.json()

        print(
            f"\n✅ Seu pedido está: {dados['status']}"
        )

    else:

        print(
            "\n❌ Pedido não encontrado."
        )