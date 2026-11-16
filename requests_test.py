import requests

while True:

    print("\n==============================")
    print("🤖 ASSISTENTE VIRTUAL")
    print("==============================")
    print("1 - Consultar pedido")
    print("2 - Listar pedidos")
    print("3 - Sair")

    opcao = input("\nEscolha uma opção: ")

    if opcao == "1":

        pedido = input(
            "\nInforme o número do pedido: "
        )

        response = requests.get(
            f"http://127.0.0.1:5000/pedido/{pedido}"
        )

        if response.status_code == 200:

            dados = response.json()

            print("\n✅ RESULTADO")
            print(
                f"Cliente: {dados['cliente']}"
            )
            print(
                f"Status: {dados['status']}"
            )

        else:

            print(
                "\n❌ Pedido não encontrado."
            )

    elif opcao == "2":

        response = requests.get(
            "http://127.0.0.1:5000/pedidos"
        )

        pedidos = response.json()

        print("\n📦 LISTA DE PEDIDOS")

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

    elif opcao == "3":

        print("\n👋 Até logo!")

        break

    else:

        print("\n❌ Opção inválida.")