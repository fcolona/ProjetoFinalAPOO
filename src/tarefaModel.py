from datetime import datetime
from DB import BancoDeDados
from classes import Tarefa, Tipo, Status


class TarefaModel:
    """Camada de regras de negócio para operações de Tarefa."""

    def __init__(self, db: BancoDeDados):
        """Recebe a dependência de acesso a dados."""
        self.db = db

    # Funcionalidade 1: Criar Tarefa (baseado em criar_tarefa.puml)
    def criar_tarefa(
        self,
        id_disciplina: int,
        titulo: str,
        descricao: str,
        data: datetime,
        tipo: Tipo,
    ) -> dict:
        # Model -> DB : Verificar existência da disciplina
        """Cria uma nova tarefa após validar entradas e existência de disciplina."""
        if not isinstance(id_disciplina, int) or id_disciplina <= 0:
            return {"sucesso": False, "erro": "Disciplina inválida", "status_code": 400}
        if not self.db.existe_disciplina(id_disciplina):
            return {
                "sucesso": False,
                "erro": "Disciplina inexistente",
                "status_code": 404,
            }
        if tipo is None:
            return {"sucesso": False, "erro": "Tipo inválido", "status_code": 400}
        if not isinstance(data, datetime):
            return {"sucesso": False, "erro": "Data inválida", "status_code": 400}

        titulo = (titulo or "").strip()
        descricao = (descricao or "").strip()
        if len(titulo) < 3:
            return {"sucesso": False, "erro": "Título muito curto", "status_code": 400}

        nova_tarefa = Tarefa(
            id_tarefa=self.db.proximo_id(),  # sempre gera um ID único
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
    def concluir_tarefa(self, id_tarefa: int) -> dict:
        """Conclui a tarefa, desagendando lembretes e persistindo alterações."""
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
            if tarefa.status == Status.CONCLUIDO:
                return {
                    "sucesso": True,
                    "mensagem": "Tarefa já estava concluída",
                    "status_code": 200,
                }
            tarefa.status = Status.CONCLUIDO
            # Loop: Itera pelos Lembretes da Tarefa
            for lembrete in getattr(tarefa, "lembretes", []):
                # Model -> DB : Desagendar Lembrete
                # Tentativa de persistir alterações no sistema externo
                try:
                    lembrete.desagendar()
                except Exception:
                    continue
            self.db.atualizar_tarefa(tarefa)
            return {
                "sucesso": True,
                "mensagem": "Tarefa concluída com sucesso",
                "status_code": 200,
            }
        except Exception:
            # Controller <-- Model : Exceção de Banco de Dados
            return {"sucesso": False, "erro": "Erro interno", "status_code": 500}
    
    def listar_tarefas(self) -> dict:
        tarefas = self.db.listar_tarefas()
        return {
            "sucesso": True,
            "mensagem": "Tarefas listadas com sucesso",
            "status_code": 200,
            "tarefas" : tarefas
        }
