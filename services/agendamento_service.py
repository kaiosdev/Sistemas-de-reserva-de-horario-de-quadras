from datetime import datetime, date

from repositories.agendamento_repository import AgendamentoRepository
from models.agendamento import Agendamento


class AgendamentoService:
    """Regras de negocio da entidade Agendamento (reserva de horario).

    Validacoes aplicadas (alem da trigger anti-choque do banco):
      - cliente e espaco obrigatorios
      - data no formato ISO (AAAA-MM-DD) e nao no passado
      - horarios no formato HH:MM e inicio < fim
    A deteccao de double-booking continua sendo feita pela trigger Postgres,
    que lancara excecao em caso de conflito; esta camada apenas a repassa.
    """

    def __init__(self):
        self.repository = AgendamentoRepository()

    def listar_todos(self):
        return self.repository.listar_todos()

    def criar(self, id_cliente, id_espaco, data_reserva: str, hora_inicio: str, hora_fim: str):
        # --- Campos obrigatorios ---
        if not id_cliente or not id_espaco:
            raise ValueError("Cliente e espaco sao obrigatorios.")
        if not all([data_reserva, hora_inicio, hora_fim]):
            raise ValueError("Data e horarios sao obrigatorios.")

        # --- Tipos numericos ---
        try:
            id_cliente = int(id_cliente)
            id_espaco = int(id_espaco)
        except (TypeError, ValueError):
            raise ValueError("Cliente e espaco devem ser identificadores validos.")

        # --- Validacao de data (ISO) ---
        try:
            data_obj = date.fromisoformat(data_reserva)
        except ValueError:
            raise ValueError("Data deve estar no formato AAAA-MM-DD.")

        if data_obj < date.today():
            raise ValueError("Nao e permitido agendar para uma data passada.")

        # --- Validacao de horarios ---
        ini = self._validar_hora(hora_inicio)
        fim = self._validar_hora(hora_fim)
        if not ini or not fim:
            raise ValueError("Horarios devem estar no formato HH:MM.")
        if ini >= fim:
            raise ValueError("A hora final deve ser maior que a hora inicial.")

        # --- Persistencia (a trigger valida choque de horario) ---
        novo = Agendamento(0, data_reserva, hora_inicio, hora_fim, id_cliente, id_espaco)
        try:
            novo_id = self.repository.inserir(novo)
            return novo_id
        except Exception as e:
            # Repassa a mensagem da trigger anti-choque de horario
            raise Exception(str(e))

    @staticmethod
    def _validar_hora(hora: str):
        try:
            return datetime.strptime(hora, "%H:%M").time()
        except (TypeError, ValueError):
            return None

    def excluir(self, id_agendamento: int):
        return self.repository.deletar(id_agendamento)

    def atualizar(self, id_agendamento, id_cliente, id_espaco, data_reserva, hora_inicio, hora_fim):
        """Atualiza um agendamento existente (mesmas validacoes de criar)."""
        if not id_cliente or not id_espaco:
            raise ValueError("Cliente e espaco sao obrigatorios.")
        if not all([data_reserva, hora_inicio, hora_fim]):
            raise ValueError("Data e horarios sao obrigatorios.")

        try:
            id_cliente = int(id_cliente)
            id_espaco = int(id_espaco)
        except (TypeError, ValueError):
            raise ValueError("Cliente e espaco devem ser identificadores validos.")

        try:
            data_obj = date.fromisoformat(data_reserva)
        except ValueError:
            raise ValueError("Data deve estar no formato AAAA-MM-DD.")
        if data_obj < date.today():
            raise ValueError("Nao e permitido agendar para uma data passada.")

        ini = self._validar_hora(hora_inicio)
        fim = self._validar_hora(hora_fim)
        if not ini or not fim:
            raise ValueError("Horarios devem estar no formato HH:MM.")
        if ini >= fim:
            raise ValueError("A hora final deve ser maior que a hora inicial.")

        try:
            return self.repository.atualizar(
                int(id_agendamento), data_reserva, hora_inicio, hora_fim, id_cliente, id_espaco,
            )
        except Exception as e:
            # Repassa erro da trigger anti-choque (caso a nova hora conflite)
            raise Exception(str(e))
