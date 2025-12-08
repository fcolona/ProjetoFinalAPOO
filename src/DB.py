from typing import Optional
from typing import List
from classes import Tarefa, Tipo, Status
import csv
from datetime import datetime
import os


class BancoDeDados:
    """Banco de dados em memória com persistência CSV simples."""

    CSV_FILENAME = os.path.join(os.path.dirname(__file__), "tarefas.csv")

    def __init__(self):
        """Inicializa o repositório e carrega dados do CSV, se houver."""
        self.tarefas = {}
        self.disciplinas_existentes = {  # Exemplo de disciplinas existentes
            1: "Matemática",
            2: "Português",
            3: "História",
            4: "Geografia",
            5: "Ciências",
            6: "Biologia",
            7: "Física",
            8: "Química",
            9: "Inglês",
            10: "Espanhol",
            11: "Artes",
            12: "Educação Física",
            13: "Literatura",
            14: "Redação",
            15: "Gramática",
            16: "Sociologia",
            17: "Filosofia",
            18: "Tecnologia da Informação",
            19: "Programação",
            20: "Robótica",
            21: "Educação Financeira",
            22: "Empreendedorismo",
            23: "Música",
            24: "Teatro",
            25: "Desenho Geométrico",
            26: "Estatística",
            27: "Geometria",
            28: "Algebra",
            29: "Cálculo",
            30: "Astronomia",
            31: "Ecologia",
            32: "Psicologia",
            33: "Direito",
            34: "Metodologia Científica",
            35: "Informática",
            36: "Lógica",
            37: "Educação Ambiental",
            38: "Educação Digital",
            39: "Projetos Interdisciplinares",
            40: "Oficina de Texto",
            41: "Comunicação",
            42: "Geopolítica",
            43: "Atualidades",
            44: "Arqueologia",
            45: "Antropologia",
            46: "Administração",
            47: "Marketing",
            48: "Economia",
            49: "Contabilidade",
            50: "Desenvolvimento Web",
        }  # Mock de disciplinas
        self._carregar_csv()  # garante que os dados persistidos sejam carregados

    # Simula 'Verificar existência da disciplina' em criar_tarefa.puml
    def existe_disciplina(self, id_disciplina: int) -> bool:
        """Verifica se a disciplina informada existe no catálogo mockado."""
        return id_disciplina in self.disciplinas_existentes

    # Simula 'Criar Tarefa' em criar_tarefa.puml
    def salvar_tarefa(self, tarefa: Tarefa) -> bool:
        """Persiste/atualiza uma tarefa em memória e no CSV."""
        # Simulação de erro de banco (Constraint/Conexão)'
        if tarefa.titulo == "ErroDB":
            raise Exception("Erro de Conexão com Banco de Dados")
        if isinstance(tarefa.tipo, str):
            tarefa.tipo = self._tipo_from_value(tarefa.tipo)
        if isinstance(getattr(tarefa, "status", None), str):
            tarefa.status = self._status_from_value(tarefa.status)

        # IDs devem ser únicos: rejeita se o ID já existe e está sendo reutilizado indevidamente
        # Race Condition. Se o ID já existir (ex: clique duplo), calcula-se o próximo para evitar erro 500.
        if tarefa.id in self.tarefas and self.tarefas[tarefa.id] is not tarefa:
            tarefa.id = self.proximo_id()

        self.tarefas[tarefa.id] = tarefa
        self._salvar_csv()
        return True

    def buscar_tarefa(self, id_tarefa: int) -> Optional[Tarefa]:
        """Retorna a tarefa pelo ID ou None se não existir."""
        return self.tarefas.get(id_tarefa)

    # Simula 'Atualizar Status' e 'Desagendar Lembrete' em concluir_tarefa.puml
    def atualizar_tarefa(self, tarefa: Tarefa) -> bool:
        """Atualiza uma tarefa existente e salva no CSV."""
        if tarefa.id not in self.tarefas:
            return False
        self.tarefas[tarefa.id] = tarefa
        self._salvar_csv()
        return True

    def id_existe(self, id_tarefa: int) -> bool:
        """Verifica se um ID de tarefa já existe."""
        return id_tarefa in self.tarefas

    def proximo_id(self) -> int:
        """Calcula o próximo ID com base no maior ID atual."""
        # calcula próximo ID com base no maior ID carregado do CSV
        return (max(self.tarefas.keys()) + 1) if self.tarefas else 1

    # CSV persistence helpers
    def _carregar_csv(self) -> None:
        """Carrega tarefas do CSV, ignorando linhas inválidas."""
        if not os.path.exists(self.CSV_FILENAME):
            return
        try:
            with open(self.CSV_FILENAME, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        id_tarefa = int(row.get("id", "").strip())
                        titulo = row.get("titulo", "").strip()
                        if not id_tarefa or not titulo:
                            continue
                        descricao = row.get("descricao", "").strip()
                        data_raw = row.get("data_entrega", "").strip()
                        if not data_raw:
                            continue
                        data_entrega = datetime.fromisoformat(data_raw)
                        tipo = self._tipo_from_value(row.get("tipo", "").strip())
                        status = self._status_from_value(
                            row.get("status", Status.EM_ANDAMENTO.value).strip()
                        )
                        nota_str = row.get("nota", "").strip()
                        nota = float(nota_str) if nota_str not in ("", None) else None

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

    def _salvar_csv(self) -> None:
        """Grava todas as tarefas atuais no CSV, sobrescrevendo o arquivo."""
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
                for tarefa in sorted(self.tarefas.values(), key=lambda t: t.id):
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
        except Exception as e:
            print(
                f"AVISO: Falha ao salvar CSV. Verifique se o arquivo está aberto. Erro: {e}"
            )
            # Em caso de erro, silenciosamente não persiste para não quebrar o fluxo
            pass

    def _tipo_from_value(self, value: str) -> Tipo:
        """Converte nome/valor (case-insensitive) em Tipo; fallback ATIVIDADE."""
        v = (value or "").strip().casefold()
        for t in Tipo:
            if v == t.value.casefold() or v == t.name.casefold():
                return t
        # fallback por segurança
        return Tipo.ATIVIDADE

    def _status_from_value(self, value: str) -> Status:
        """Converte nome/valor (case-insensitive) em Status; fallback EM_ANDAMENTO."""
        v = (value or "").strip().casefold()
        for s in Status:
            if v == s.value.casefold() or v == s.name.casefold():
                return s
        return Status.EM_ANDAMENTO

    def listar_tarefas(self) -> List[Tarefa]:
        return self.tarefas
