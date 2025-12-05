from typing import Optional
from classes import Tarefa


class BancoDeDados:
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
        return True

    def buscar_tarefa(self, id_tarefa: int) -> Optional[Tarefa]:
        return self.tarefas.get(id_tarefa)

    # Simula 'Atualizar Status' e 'Desagendar Lembrete' em concluir_tarefa.puml
    def atualizar_tarefa(self, tarefa: Tarefa):
        if tarefa.id not in self.tarefas:
            return False
        self.tarefas[tarefa.id] = tarefa
        return True
