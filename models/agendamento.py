class Agendamento:
    
    def __init__(self, id_agendamento: int, data_reserva: str, hora_inicio: str, hora_fim: str, id_cliente: int, id_espaco: int, nome_cliente: str = "", nome_espaco: str = ""):
        self.id_agendamento = id_agendamento
        self.data_reserva = data_reserva
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
        self.id_cliente = id_cliente
        self.id_espaco = id_espaco
        self.nome_cliente = nome_cliente
        self.nome_espaco = nome_espaco

    def __str__(self):
        cliente_info = self.nome_cliente if self.nome_cliente else f"Cliente {self.id_cliente}"
        espaco_info = self.nome_espaco if self.nome_espaco else f"Espaco {self.id_espaco}"
        
        return f"Reserva em {self.data_reserva} ({self.hora_inicio} as {self.hora_fim}) | {cliente_info} em {espaco_info}"