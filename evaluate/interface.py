from evaluate_prompt import evaluate_single_chat, evaluate_multiple_chats

def main():
    while True:
        print("\n" + "=" * 40)
        print("  AVALIADOR DE PROMPTS - TUTORIA IA")
        print("=" * 40)
        print("1. Executar todas as perguntas em um chat")
        print("2. Executar perguntas em múltiplos chats")
        print("0. Sair")
        print("=" * 40)

        option = input("Escolha uma opção: ").strip()

        if option == "0":
            print("Encerrando o avaliador.")
            break

        elif option == "1":
            name = input(
                "Nome do arquivo de resultados (Enter para automático): "
            ).strip()

            try:
                evaluate_single_chat(name or None)
            except Exception as error:
                print(f"\nFalha na avaliação: {error}")

        elif option == "2":
            try:
                questions_per_chat = int(
                    input("Quantas perguntas por chat? ").strip()
                )
            except ValueError:
                print("Informe um número inteiro válido.")
                continue

            if questions_per_chat < 1:
                print("Informe um número maior que zero.")
                continue

            name = input(
                "Nome do arquivo de resultados (Enter para automático): "
            ).strip()

            try:
                evaluate_multiple_chats(
                    questions_per_chat=questions_per_chat,
                    name=name or None
                )
            except Exception as error:
                print(f"\nFalha na avaliação: {error}")

        else:
            print("Opção inválida. Escolha 1, 2 ou 0.")


if __name__ == "__main__":
    main()
