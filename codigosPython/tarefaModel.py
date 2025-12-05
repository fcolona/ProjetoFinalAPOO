from datetime import datetime
from DB import BancoDeDados
from classes import Tarefa, Tipo, Status


class TarefaModel:
    def __init__(self, db: BancoDeDados):
        self.db = db

    # Funcionalidade 1: Criar Tarefa (baseado em criar_tarefa.puml)
    def criar_tarefa(
        self,
        id_disciplina: int,
        titulo: str,
        descricao: str,
        data: datetime,
        tipo: Tipo,
    ):
        # Model -> DB : Verificar existência da disciplina
        if not self.db.existe_disciplina(id_disciplina):
            return {
                "sucesso": False,
                "erro": "Disciplina inexistente",
                "status_code": 404,
            }

        nova_tarefa = Tarefa(
            id_tarefa=len(self.db.tarefas) + 1,
            titulo=titulo,
            descricao=descricao,
            data_entrega=data,
            tipo=tipo,
        )

        try:
            # Model -> DB : Criar Tarefa
            self.db.salvar_tarefa(nova_tarefa)
            return {
                "sucesso": True,
                "tarefa": nova_tarefa,
                "status_code": 201,
            }  # 201 Created
        except Exception as e:
            # Controller <-- Model : Exceção de Banco de Dados
            return {"sucesso": False, "erro": str(e), "status_code": 500}

    # Funcionalidade 2: Concluir Tarefa (baseado em concluir_tarefa.puml)
    def concluir_tarefa(self, id_tarefa: int):
        tarefa = self.db.buscar_tarefa(id_tarefa)

        # Validação se tarefa existe (Caso de Erro 2)
        if not tarefa:
            return {
                "sucesso": False,
                "erro": "Tarefa não encontrada",
                "status_code": 404,
            }

        try:
            # Model -> DB : Atualizar Status para CONCLUIDO
            tarefa.status = Status.CONCLUIDO

            # Loop: Itera pelos Lembretes da Tarefa
            for lembrete in tarefa.lembretes:
                # Model -> DB : Desagendar Lembrete
                lembrete.desagendar()

            # Persistir alterações
            self.db.atualizar_tarefa(tarefa)

            return {
                "sucesso": True,
                "mensagem": "Tarefa concluída com sucesso",
                "status_code": 200,
            }
        except Exception:
            # Controller <-- Model : Exceção de Banco de Dados
            return {"sucesso": False, "erro": "Erro interno", "status_code": 500}
