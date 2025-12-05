from tarefaModel import TarefaModel


class TarefaController:
    def __init__(self, model: TarefaModel):
        self.model = model

    # Endpoint para Criar Tarefa
    def post_criar_tarefa(self, dados: dict):
        print(f"--- Recebendo Request POST Criar Tarefa: {dados.get('titulo')} ---")

        # Controller -> Controller : Validar formato dos dados
        if not dados.get("titulo") or not dados.get("id_disciplina"):
            # View <-- Controller : Resposta HTTP: 400 Bad Request
            return {"status": 400, "body": "Campos obrigatórios faltando"}

        # Controller -> Model : Criar tarefa
        resultado = self.model.criar_tarefa(
            id_disciplina=dados["id_disciplina"],
            titulo=dados["titulo"],
            descricao=dados.get("descricao", ""),
            data=dados.get("data_entrega"),
            tipo=dados.get("tipo"),
        )

        return {
            "status": resultado["status_code"],
            "body": resultado.get("tarefa", resultado.get("erro")),
        }

    # Endpoint para Concluir Tarefa
    def put_concluir_tarefa(self, id_tarefa: int):
        print(f"--- Recebendo Request PUT Concluir Tarefa ID: {id_tarefa} ---")

        # Controller -> Model : Editar Tarefa (Conclusão)
        resultado = self.model.concluir_tarefa(id_tarefa)

        return {
            "status": resultado["status_code"],
            "body": resultado.get("mensagem", resultado.get("erro")),
        }
