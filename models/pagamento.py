from abc import ABC, abstractmethod

class Pagamento(ABC):
    def __init__(self, id_pagamento: int, valor_total: float, status: str, id_agendamento: int):
        self.id_pagamento = id_pagamento
        self.valor_total = valor_total
        self.status = status
        self.id_agendamento = id_agendamento

    @abstractmethod
    def processar(self):
        pass

    def __str__(self):
        return f"Pagamento(ID: {self.id_pagamento} | Valor: R${self.valor_total:.2f} | Status: {self.status})"

class PagamentoPix(Pagamento):

    def processar(self):
        self.status = 'Pago'
        print(f"Gerando QR Code PIX no valor de R${self.valor_total:.2f}... Pagamento Aprovado!")

class PagamentoCartao(Pagamento):

    def processar(self):
        self.status = 'Pago'
        print(f"Conectando com a maquininha para R${self.valor_total:.2f}... Transação Aprovada!")