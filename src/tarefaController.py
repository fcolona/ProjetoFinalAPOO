from tarefaModel import TarefaModel
from classes import Tipo
from datetime import datetime
import re


class TarefaController:
    """Camada de orquestração entre View e Model (simula endpoints HTTP)."""

    def __init__(self, model: TarefaModel):
        """Injeta o model que contém as regras de negócio."""
        self.model = model

    # Endpoint para Criar Tarefa
    def post_criar_tarefa(self, dados: dict) -> dict:
        """Valida/coage dados de criação e delega ao model."""
        # print(f"--- Recebendo Request POST Criar Tarefa: {dados.get('titulo')} ---")
        try:
            titulo = (dados.get("titulo") or "").strip()
            id_disciplina = dados.get("id_disciplina")
            descricao = (dados.get("descricao") or "").strip()
            data_entrega = dados.get("data_entrega")
            tipo = dados.get("tipo")

            if not titulo or id_disciplina is None:
                # View <-- Controller: Resposta HTTP 400: Bad Request
                return {"status": 400, "body": "Informe título e ID da disciplina."}

            # Coerções/validações
            try:
                id_disciplina = int(id_disciplina)
                if id_disciplina <= 0:
                    return {
                        "status": 400,
                        "body": "ID da disciplina deve ser positivo.",
                    }
            except Exception:
                return {"status": 400, "body": "ID da disciplina deve ser numérico."}

            # Validação obrigando horário
            ok, motivo = self._validar_data_str(data_entrega)

            if not ok:
                # Diagnóstico: mostra o valor recebido e a razão
                return {
                    "status": 400,
                    "body": f"Data/Horário inválido: {motivo}",
                }
            data_entrega = self._coerce_datetime(data_entrega)

            if not isinstance(data_entrega, datetime):
                return {
                    "status": 400,
                    "body": f"Data/Horário inválido. Recebido: '{dados.get('data_entrega')}'. Use dd/mm/aaaa [HH:MM] ou yyyy-mm-dd [HH:MM].",
                }

            tipo = self._coerce_tipo(tipo)
            if not isinstance(tipo, Tipo):
                return {
                    "status": 400,
                    "body": "Tipo inválido. Use PROVA, TRABALHO ou ATIVIDADE.",
                }

            # Controller -> Model : Criar Tarefa
            resultado = self.model.criar_tarefa(
                id_disciplina=id_disciplina,
                titulo=titulo,
                descricao=descricao,
                data=data_entrega,
                tipo=tipo,
            )

            return {
                "status": resultado["status_code"],
                "body": resultado.get("tarefa", resultado.get("erro")),
            }

        except Exception:
            return {"status": 500, "body": "Falha ao processar a criação."}

    # Endpoint para Concluir Tarefa
    def put_concluir_tarefa(self, id_tarefa: int) -> dict:
        """Recebe o ID e delega a conclusão ao model."""
        # print(f"--- Recebendo Request PUT Concluir Tarefa ID: {id_tarefa} ---")
        # Controller -> Model : Editar Tarefa (Conclusão)
        try:
            id_tarefa = int(id_tarefa)
            if id_tarefa <= 0:
                return {"status": 400, "body": "ID da tarefa deve ser positivo."}
        except Exception:
            return {"status": 400, "body": "ID da tarefa deve ser numérico."}

        resultado = self.model.concluir_tarefa(id_tarefa)
        return {
            "status": resultado["status_code"],
            "body": resultado.get("mensagem", resultado.get("erro")),
        }

    # Endpoint para LIstar Tarefas
    def get_listar_tarefas(self) -> dict:
        # print(f"--- Recebendo Request GET Listar Tarefas")
        resultado = self.model.listar_tarefas()
        return {
            "status": resultado["status_code"],
            "body": resultado["tarefas"],
        }

    # Helpers
    def _coerce_datetime(self, v) -> datetime | None:
        """Converte string em datetime, exigindo horário (HH:MM)."""
        if isinstance(v, datetime):
            return v
        if isinstance(v, str):
            for fmt in (
                "%Y-%m-%d %H:%M",
                "%Y-%m-%d",
                "%d/%m/%Y %H:%M",
                "%d/%m/%Y",
                "%d-%m-%Y %H:%M",
                "%d-%m-%Y",
            ):
                try:
                    return datetime.strptime(v.strip(), fmt)
                except ValueError:
                    pass
        return None

    def _coerce_tipo(self, v) -> Tipo | None:
        """Converte string (nome/valor) em enum Tipo."""
        if isinstance(v, Tipo):
            return v
        if isinstance(v, str):
            s = v.strip().casefold()
            for t in Tipo:
                if s == t.name.casefold() or s == t.value.casefold():
                    return t
        return None

    def _validar_data_str(self, v) -> tuple[bool, str | None]:
        """Valida formato e existência no calendário, exigindo horário. Retorna (ok, motivo_erro)."""
        if isinstance(v, datetime):
            return True, None
        if not isinstance(v, str):
            return (
                False,
                "Data/Horário inválido. Use dd/mm/aaaa [HH:MM] ou yyyy-mm-dd [HH:MM].",
            )

        s = v.strip()
        formatos = [
            ("%d/%m/%Y %H:%M", r"^\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}$"),
            ("%d/%m/%Y", r"^\d{1,2}/\d{1,2}/\d{4}$"),
            ("%Y-%m-%d %H:%M", r"^\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{2}$"),
            ("%Y-%m-%d", r"^\d{4}-\d{1,2}-\d{1,2}$"),
            ("%d-%m-%Y %H:%M", r"^\d{1,2}-\d{1,2}-\d{4}\s+\d{1,2}:\d{2}$"),
            ("%d-%m-%Y", r"^\d{1,2}-\d{1,2}-\d{4}$"),
        ]

        # Checa se algum formato é compatível com o padrão
        padrao_combinou = False
        for fmt, regex in formatos:
            if re.match(regex, s):
                padrao_combinou = True
                try:
                    # strptime já valida meses com zero à esquerda (ex.: 08)
                    dt = datetime.strptime(s, fmt)
                    # valida faixa de hora/minuto quando presente
                    if "%H:%M" in fmt and not (
                        0 <= dt.hour <= 23 and 0 <= dt.minute <= 59
                    ):
                        return False, "Horário inexistente (hora/minuto fora da faixa)."
                    return True, None
                except ValueError:
                    # Padrão ok, mas data impossível (ex.: 31/02/2024)
                    return False, "Data inexistente no calendário."

        # Nenhum padrão bateu
        if not padrao_combinou:
            return (
                False,
                "Formato inválido. Use dd/mm/aaaa [HH:MM] ou yyyy-mm-dd [HH:MM].",
            )

        # fallback
        return False, "Data/Horário inválido."
