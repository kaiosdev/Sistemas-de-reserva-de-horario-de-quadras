from abc import ABC, abstractmethod

class Pagamento(ABC):
    def __init__(self, id_pagamento: int, valor_total: float, id_agendamento: int, status: str = "Pendente"):
        self.id_pagamento = id_pagamento
        self.valor_total = valor_total
        self.id_agendamento = id_agendamento
        self.status = status

    @abstractmethod
    def processar(self):
        pass

class PagamentoPix(Pagamento):
    def __init__(self, id_pagamento: int, valor_total: float, id_agendamento: int, chave_pix: str, status: str = "Pendente"):
        super().__init__(id_pagamento, valor_total, id_agendamento, status)
        self.chave_pix = chave_pix

    def processar(self):
        self.status = 'Pago'
        print(f"Pagamento PIX de R${self.valor_total:.2f} processado via chave {self.chave_pix}.")

class PagamentoCartao(Pagamento):
    def __init__(self, id_pagamento: int, valor_total: float, id_agendamento: int, final_cartao: str, status: str = "Pendente"):
        super().__init__(id_pagamento, valor_total, id_agendamento, status)
        self.final_cartao = final_cartao

    def processar(self):
        self.status = 'Pago'
        print(f"Pagamento Cartao de R${self.valor_total:.2f} processado no final {self.final_cartao}.")