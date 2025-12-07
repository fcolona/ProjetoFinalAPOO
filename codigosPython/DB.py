from typing import Optional
from classes import Tarefa, Tipo, Status
import csv
from datetime import datetime
import os


class BancoDeDados:
    CSV_FILENAME = os.path.join(os.path.dirname(__file__), "tarefas.csv")

    def __init__(self):
        self.tarefas = {}
        self.disciplinas_existentes = {  # Exemplo de disciplinas existentes
            1: "Matemática",
            2: "História",
        }  # Mock de disciplinas

    # Simula 'Verificar existência da disciplina' em criar_tarefa.puml
    def existe_disciplina(self, id_disciplina: int) -> bool:
        return id_disciplina in self.disciplinas_existentes

    # Simula 'Criar Tarefa' em criar_tarefa.puml
    def salvar_tarefa(self, tarefa: Tarefa):
        # Simulação de erro de banco (Constraint/Conexão)'
        if tarefa.titulo == "ErroDB":
            raise Exception("Erro de Conexão com Banco de Dados")
        self.tarefas[tarefa.id] = tarefa
        self._salvar_csv()
        return True

    def buscar_tarefa(self, id_tarefa: int) -> Optional[Tarefa]:
        return self.tarefas.get(id_tarefa)

    # Simula 'Atualizar Status' e 'Desagendar Lembrete' em concluir_tarefa.puml
    def atualizar_tarefa(self, tarefa: Tarefa):
        if tarefa.id not in self.tarefas:
            return False
        self.tarefas[tarefa.id] = tarefa
        self._salvar_csv()
        return True

    # CSV persistence helpers
    def _carregar_csv(self):
        if not os.path.exists(self.CSV_FILENAME):
            return
        try:
            with open(self.CSV_FILENAME, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        id_tarefa = int(row["id"])
                        titulo = row["titulo"]
                        descricao = row.get("descricao", "")
                        data_entrega = datetime.fromisoformat(row["data_entrega"])
                        tipo = self._tipo_from_value(row["tipo"])
                        status = self._status_from_value(
                            row.get("status", Status.EM_ANDAMENTO.value)
                        )
                        nota = float(row["nota"]) if row.get("nota") else None

                        tarefa = Tarefa(
                            id_tarefa=id_tarefa,
                            titulo=titulo,
                            descricao=descricao,
                            data_entrega=data_entrega,
                            tipo=tipo,
                        )
                        tarefa.status = status
                        tarefa.nota = nota
                        # lembretes não são persistidos neste CSV simples
                        self.tarefas[id_tarefa] = tarefa
                    except Exception:
                        # Ignora linhas inválidas
                        continue
        except Exception:
            # Falha ao carregar CSV, não bloqueia a aplicação
            pass

    def _salvar_csv(self):
        try:
            with open(self.CSV_FILENAME, mode="w", newline="", encoding="utf-8") as f:
                fieldnames = [
                    "id",
                    "titulo",
                    "descricao",
                    "data_entrega",
                    "tipo",
                    "status",
                    "nota",
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for tarefa in self.tarefas.values():
                    writer.writerow(
                        {
                            "id": tarefa.id,
                            "titulo": tarefa.titulo,
                            "descricao": tarefa.descricao,
                            "data_entrega": tarefa.data_entrega.isoformat(),
                            "tipo": tarefa.tipo.value,
                            "status": tarefa.status.value,
                            "nota": "" if tarefa.nota is None else tarefa.nota,
                        }
                    )
        except Exception:
            # Em caso de erro, silenciosamente não persiste para não quebrar o fluxo
            pass

    def _tipo_from_value(self, value: str) -> Tipo:
        for t in Tipo:
            if t.value == value:
                return t
        # fallback por segurança
        return Tipo.ATIVIDADE

    def _status_from_value(self, value: str) -> Status:
        for s in Status:
            if s.value == value:
                return s
        return Status.EM_ANDAMENTO
