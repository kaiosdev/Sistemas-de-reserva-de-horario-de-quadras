from models.agendamento import Agendamento
from repositories.agendamento_repository import AgendamentoRepository

class AgendamentoService:
    def __init__(self):
        self.repository = AgendamentoRepository()

    def cadastrar_agendamento(self, data, hora_inicio, hora_fim, id_cliente, id_espaco):
        ag = Agendamento(0, data, hora_inicio, hora_fim, id_cliente, id_espaco)
        self.repository.inserir(ag)

    def atualizar_agendamento(self, id_agendamento, data, hora_inicio, hora_fim, id_cliente, id_espaco):
        self.repository.atualizar(id_agendamento, data, hora_inicio, hora_fim, id_cliente, id_espaco)

    def listar_agendamentos(self):
        return self.repository.listar_todos()

    def excluir_agendamento(self, id_agendamento: int):
        self.repository.excluir(id_agendamento)