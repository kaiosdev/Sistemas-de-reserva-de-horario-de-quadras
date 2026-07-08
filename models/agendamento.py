class Agendamento:
    def __init__(self, id_agendamento: int, data_reserva: str, hora_inicio: str, hora_fim: str, id_cliente: int, nome_cliente: str = "", espacos_str: str = "", valor_total_espacos: float = 0.0):
        self.id_agendamento = id_agendamento
        self.data_reserva = data_reserva
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
        self.id_cliente = id_cliente
        self.nome_cliente = nome_cliente
        self.espacos_str = espacos_str
        self.valor_total_espacos = valor_total_espacos

    def __str__(self):
        cliente_info = self.nome_cliente if self.nome_cliente else f"Cliente {self.id_cliente}"
        espaco_info = self.nome_espaco if self.nome_espaco else f"Espaco {self.id_espaco}"
        
        return f"Reserva em {self.data_reserva} ({self.hora_inicio} as {self.hora_fim}) | {cliente_info} em {espaco_info}"

    def __repr__(self):
        return f"Agendamento(id={self.id_agendamento}, data='{self.data_reserva}', cliente={self.id_cliente}, espaco={self.id_espaco})"
    