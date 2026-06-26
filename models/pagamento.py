from abc import ABC, abstractmethod

# Classe Abstrata
class Pagamento(ABC):
    def __init__(self, id_pagamento: int, valor_total: float, id_agendamento: int, status: str = "Pendente"):
        self.id_pagamento = id_pagamento
        self.valor_total = valor_total
        self.id_agendamento = id_agendamento
        self.status = status

    @abstractmethod
    def processar(self):
        pass

# Heranca e Polimorfismo aplicados apenas onde existe especializacao real
class PagamentoPix(Pagamento):
    def __init__(self, id_pagamento: int, valor_total: float, id_agendamento: int, chave_pix: str, status: str = "Pendente"):
        super().__init__(id_pagamento, valor_total, id_agendamento, status)
        self.chave_pix = chave_pix

    def processar(self):
        self.status = 'Pago'
        print(f"Gerando QR Code para a chave {self.chave_pix}... Pagamento de R${self.valor_total:.2f} Aprovado!")

class PagamentoCartao(Pagamento):
    def __init__(self, id_pagamento: int, valor_total: float, id_agendamento: int, final_cartao: str, status: str = "Pendente"):
        super().__init__(id_pagamento, valor_total, id_agendamento, status)
        self.final_cartao = final_cartao

    def processar(self):
        self.status = 'Pago'
        print(f"Processando cartao final {self.final_cartao}... Transacao de R${self.valor_total:.2f} Aprovada!")