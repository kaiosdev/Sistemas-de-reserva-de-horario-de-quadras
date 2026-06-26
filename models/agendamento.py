class Agendamento:
    def __init__(self, id_agendamento: int, data_reserva: str, hora_inicio: str, hora_fim: str, id_cliente: int, id_espaco: int):
        self.id_agendamento = id_agendamento
        self.data_reserva = data_reserva
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
        self.id_cliente = id_cliente
        self.id_espaco = id_espaco

    def __str__(self):
        return f"Reserva {self.id_agendamento}: Data {self.data_reserva} das {self.hora_inicio} as {self.hora_fim}"