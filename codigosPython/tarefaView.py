from datetime import datetime
from classes import Tipo
import os


class TarefaView:
    """Interface de linha de comando para criar e concluir tarefas."""

    def __init__(self, controller):
        """Recebe o controller para enviar ações do usuário."""
        self.controller = controller

    def exibir_menu_principal(self):
        """Exibe opções principais e retorna a seleção do usuário."""
        self.limpar_tela()
        print("\n=== SISTEMA DE GESTÃO DE TAREFAS ===")
        print("1. Nova Tarefa")
        print("2. Concluir Tarefa")
        print("0. Sair")
        opcao = input("Selecione uma opção: ")
        return opcao

    # Implementação do fluxo visual de "Criar Tarefa" (referência: criar_tarefa.puml)

    def renderizar_criar_tarefa(self):
        """Fluxo de criação de tarefa com validações de entrada."""
        self.limpar_tela()
        print("\n--- [Tela] Nova Tarefa ---")
        # 1. Coleta de dados (User -> View)
        try:
            id_disciplina = self._input_int("ID da Disciplina: ")
            titulo = self._input_nonempty("Título: ")
            descricao = input("Descrição: ").strip()

            # aceita data com ou sem horário
            data_entrega = self._input_datetime(
                "Data/Horário de Entrega (dd/mm/aaaa [HH:MM]): "
            )

            # Montagem do payload (simula o corpo de requisição HTTP)
            # Mapeamento de string para Enum (lógica simples de front-end)
            tipo = self._input_tipo("Tipo (PROVA, TRABALHO, ATIVIDADE): ")

            payload = {
                "id_disciplina": id_disciplina,
                "titulo": titulo,
                "descricao": descricao,
                "data_entrega": data_entrega,
                "tipo": tipo,
            }
            # 2. Envio ao Controller (View -> Controller : Requisição HTTP POST)
            resposta = self.controller.post_criar_tarefa(payload)
            # 3. Exibição do Resultado
            self._processar_resposta_http(resposta)
        except KeyboardInterrupt:
            print("\nOperação cancelada.")

    # Implementação do fluxo visual de "Concluir Tarefa" (referência: concluir_tarefa.puml)

    def renderizar_concluir_tarefa(self):
        """Fluxo de conclusão de tarefa com validação de ID."""
        self.limpar_tela()
        print("\n--- [Tela] Concluir Tarefa ---")

        # 1. Coleta de dados
        try:
            # 2. Envio ao Controller (View -> Controller : Requisição HTTP PUT)
            id_tarefa = self._input_int("Digite o ID da Tarefa a concluir: ")
            resposta = self.controller.put_concluir_tarefa(id_tarefa)
            # 3. Exibição do Resultado
            self._processar_resposta_http(resposta)
        except KeyboardInterrupt:
            print("\nOperação cancelada.")

    # Método Auxiliar para tratar "Códigos HTTP"
    # Baseado nas respostas mostradas nos diagramas de sequência

    def _processar_resposta_http(self, resposta):
        """Interpreta o 'status' e o 'body' simulando códigos HTTP."""
        status = resposta["status"]
        body = resposta["body"]

        if status == 200:
            # View <-- Controller : Resposta HTTP: 200 OK
            print(f"SUCESSO: {body}")  # "Tela de confirmação"

        elif status == 201:
            # View <-- Controller : Resposta HTTP: 201 Created
            # O body presente será o objeto Tarefa
            titulo = body.titulo if hasattr(body, "titulo") else "Nova Tarefa"
            tarefa_id = getattr(body, "id", None)
            print(
                f"CRIADO: Tarefa '{titulo}' registrada com sucesso!"
                f"{' ID: ' + str(tarefa_id) if tarefa_id is not None else ''}"
            )

        elif status == 400:
            # View <-- Controller : Resposta HTTP: 400 Bad Request
            print(
                f"AVISO: Entrada de dados inválida - {body}"
            )  # "Exibir mensagens de validação"

        elif status == 404:
            # View <-- Controller : Resposta HTTP: 404 Not Found
            print(
                f"NÃO ENCONTRADO: {body}"
            )  # "Mensagem: Disciplina/Tarefa não encontrada"

        elif status == 500:
            # View <-- Controller : Resposta HTTP: 500 Internal Server Error
            print(f"ERRO INTERNO: {body}")  # "Mensagem: Erro interno..."

        else:
            print(f"Status {status}: {body}")

    # Helpers de entrada robusta
    def _input_int(self, prompt: str) -> int:
        """Lê um inteiro positivo com repetição até ser válido."""
        while True:
            try:
                v = int(input(prompt).strip())
                if v <= 0:
                    print("Informe um número positivo.")
                    continue
                return v
            except ValueError:
                print("Valor inválido, tente novamente.")

    def _input_nonempty(self, prompt: str) -> str:
        """Lê uma string não vazia."""
        while True:
            v = input(prompt).strip()
            if v:
                return v
            print("O campo não pode ser vazio.")

    def _input_date(self, prompt: str) -> datetime:
        """Aceita múltiplos formatos de data e retorna datetime."""
        while True:
            s = input(prompt).strip()
            for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
                try:
                    return datetime.strptime(s, fmt)
                except ValueError:
                    pass
            print("Data inválida. Use formatos: dd/mm/aaaa ou yyyy-mm-dd.")

    def _input_datetime(self, prompt: str) -> datetime:
        """Aceita data com ou sem horário. Exemplos: 25/12/2025, 25/12/2025 14:30, 2025-12-25 14:30."""
        while True:
            s = input(prompt).strip()
            formatos = (
                "%d/%m/%Y %H:%M",
                "%d/%m/%Y",
                "%Y-%m-%d %H:%M",
                "%Y-%m-%d",
                "%d-%m-%Y %H:%M",
                "%d-%m-%Y",
            )
            for fmt in formatos:
                try:
                    return datetime.strptime(s, fmt)
                except ValueError:
                    pass
            print(
                "Data/Horário inválido. Use dd/mm/aaaa [HH:MM] ou yyyy-mm-dd [HH:MM]."
            )

    def _input_tipo(self, prompt: str) -> Tipo:
        """Lê e normaliza o tipo (nome ou valor do enum)."""
        while True:
            s = input(prompt).strip()
            t = self._normalizar_tipo(s)
            if t:
                return t
            print("Tipo inválido. Opções: PROVA, TRABALHO, ATIVIDADE.")

    def _normalizar_tipo(self, valor: str):
        """Converte texto para enum Tipo, ou None se inválido."""
        v = valor.strip().casefold()
        for t in Tipo:
            if v == t.name.casefold() or v == t.value.casefold():
                return t
        return None

    def limpar_tela(self):
        """Limpa a tela do terminal (Windows/Linux/macOS)."""
        try:
            os.system("cls" if os.name == "nt" else "clear")
        except Exception:
            pass
