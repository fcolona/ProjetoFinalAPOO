from datetime import datetime
from classes import Tipo


class TarefaView:
    def __init__(self, controller):
        self.controller = controller

    def exibir_menu_principal(self):
        print("\n=== SISTEMA DE GESTÃO DE TAREFAS ===")
        print("1. Nova Tarefa")
        print("2. Concluir Tarefa")
        print("0. Sair")
        opcao = input("Selecione uma opção: ")
        return opcao

    # Implementação do fluxo visual de "Criar Tarefa" (referência: criar_tarefa.puml)

    def renderizar_criar_tarefa(self):
        print("\n--- [Tela] Nova Tarefa ---")

        # 1. Coleta de dados (User -> View)
        try:
            id_disciplina = int(input("ID da Disciplina: "))
            titulo = input("Título: ")
            descricao = input("Descrição: ")
            data_str = input("Data de Entrega (dd/mm/aaaa): ")
            tipo_str = input("Tipo (PROVA, TRABALHO, ATIVIDADE): ").upper()

            # Conversão simples de dados de entrada
            data_entrega = datetime.strptime(data_str, "%d/%m/%Y")

            # Montagem do payload (simula o corpo da requisição HTTP)
            # Mapeamento de string para Enum (logica simples de front-end)
            tipo_map = {
                "PROVA": Tipo.PROVA,
                "TRABALHO": Tipo.TRABALHO,
                "ATIVIDADE": Tipo.ATIVIDADE,
            }

            payload = {
                "id_disciplina": id_disciplina,
                "titulo": titulo,
                "descricao": descricao,
                "data_entrega": data_entrega,
                "tipo": tipo_map.get(tipo_str),
            }

            # 2. Envio ao Controller (View -> Controller : Requisição HTTP POST)
            resposta = self.controller.post_criar_tarefa(payload)

            # 3. Exibição do Resultado
            self._processar_resposta_http(resposta)

        except ValueError:
            print("[View] Erro de formato nos dados inseridos.")

    # Implementação do fluxo visual de "Concluir Tarefa" (referência: concluir_tarefa.puml)

    def renderizar_concluir_tarefa(self):
        print("\n--- [Tela] Concluir Tarefa ---")

        # 1. Coleta de dados
        try:
            id_tarefa = int(input("Digite o ID da Tarefa a concluir: "))

            # 2. Envio ao Controller (View -> Controller : Requisição HTTP PUT)
            resposta = self.controller.put_concluir_tarefa(id_tarefa)

            # 3. Exibição do Resultado
            self._processar_resposta_http(resposta)

        except ValueError:
            print("[View] ID inválido.")

    # Método Auxiliar para tratar "Códigos HTTP"
    # Baseado nas respostas mostradas nos diagramas de sequência

    def _processar_resposta_http(self, resposta):
        status = resposta["status"]
        body = resposta["body"]

        if status == 200:
            # View <-- Controller : Resposta HTTP: 200 OK
            print(f"SUCESSO: {body}")  # "Tela de confirmação"

        elif status == 201:
            # View <-- Controller : Resposta HTTP: 201 Created
            # O body presente será o objeto Tarefa
            titulo = body.titulo if hasattr(body, "titulo") else "Nova Tarefa"
            print(f"CRIADO: Tarefa '{titulo}' registrada com sucesso!")

        elif status == 400:
            # View <-- Controller : Resposta HTTP: 400 Bad Request
            print(f"AVISO: Dados inválidos - {body}")  # "Exibir mensagens de validação"

        elif status == 404:
            # View <-- Controller : Resposta HTTP: 404 Not Found
            print(
                f"NÃO ENCONTRADO: {body}"
            )  # "Mensagem: Disciplina/Tarefa não encontrada"

        elif status == 500:
            # View <-- Controller : Resposta HTTP: 500 Internal Server Error
            print(f"ERRO CRÍTICO: {body}")  # "Mensagem: Erro interno..."

        else:
            print(f"Status desconhecido ({status}): {body}")
