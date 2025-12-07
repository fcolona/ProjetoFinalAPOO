from enum import Enum
from datetime import datetime
from typing import Optional, List


# Baseado em classes_tarefa.puml
class Status(Enum):
    """Estados possíveis de uma tarefa."""

    PENDENTE = "Pendente"
    EM_ANDAMENTO = "Em Andamento"
    CONCLUIDO = "Concluido"


class Tipo(Enum):
    """Tipos de tarefa conforme o escopo do sistema."""

    PROVA = "Prova"
    TRABALHO = "Trabalho"
    ATIVIDADE = "Atividade"


class Lembrete:
    """Representa um lembrete associado a uma tarefa."""

    def __init__(self, data: datetime):
        self.data = data
        self.agendado = True  # Atributo 'agendado'

    def desagendar(self):
        """Lógica para cancelar o agendamento no sistema externo"""
        self.agendado = False
        print(f"[Sistema Email] Lembrete para {self.data} foi CANCELADO.")


class Tarefa:
    """Entidade de domínio, Tarefa com lembretes e status."""

    def __init__(
        self,
        id_tarefa: int,
        titulo: str,
        descricao: str,
        data_entrega: datetime,
        tipo: Tipo,
    ):
        self.id = id_tarefa
        self.titulo = titulo
        self.descricao = descricao
        self.data_entrega = data_entrega
        self.tipo = tipo
        self.nota: Optional[float] = (
            None 
        )
        self.status = (
            Status.EM_ANDAMENTO  # Status inicial
        ) 
        self.lembretes: List[Lembrete] = []

    def adicionar_lembrete(self, data: datetime):
        """Adiciona um novo lembrete para a tarefa."""
        self.lembretes.append(Lembrete(data))
