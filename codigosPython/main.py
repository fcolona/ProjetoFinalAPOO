# from datetime import datetime
from DB import BancoDeDados
from tarefaModel import TarefaModel
from tarefaController import TarefaController
from tarefaView import TarefaView

if __name__ == "__main__":
    # 1. Setup Inicial (Injeção de Dependência)
    db = BancoDeDados()

    # O Model recebe o DB para poder persistir os dados
    model = TarefaModel(db)

    # O Controller recebe o Model para aplicar as regras de negócio
    controller = TarefaController(model)

    # A View recebe o Controller para enviar as ações do usuário
    view = TarefaView(controller)

    # 2. Loop de Aplicação
    while True:
        try:
            # Exibe o menu e captura a escolha
            opcao = view.exibir_menu_principal()

            if opcao == "1":
                # Equivalente ao Cenário 1 e 2
                # A própria View vai pedir os dados (Título, Data, etc.) e tratar tanto o sucesso (201) quanto o erro de disciplina (404)
                view.renderizar_criar_tarefa()

            elif opcao == "2":
                # Equivalente ao Cenário 3
                # A View pede o ID e chama o controller para concluir
                view.renderizar_concluir_tarefa()

            elif opcao == "0":
                print("Saindo do sistema...")
                break

            else:
                print("Opção inválida, tente novamente.")

        except KeyboardInterrupt:
            print("\nSaindo do sistema...")
            break
