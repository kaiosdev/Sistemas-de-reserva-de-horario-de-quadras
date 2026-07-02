import hashlib
import random
import time
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
    def __init__(self, id_pagamento: int, valor_total: float, id_agendamento: int, chave_pix: str = "", status: str = "Pendente"):
        super().__init__(id_pagamento, valor_total, id_agendamento, status)
        self.chave_pix = chave_pix

    def gerar_qr_fake(self) -> str:
        base = f"athletix-{self.id_agendamento}-{self.valor_total}-{time.time()}-{random.randint(1000, 9999)}"
        return hashlib.sha256(base.encode()).hexdigest()[:32].upper()

    def processar(self):
        if self.valor_total <= 0:
            raise ValueError("Valor do pagamento invalido.")
        if not self.chave_pix:
            self.chave_pix = self.gerar_qr_fake()
        self.status = 'Pago'
        print(f"Pagamento PIX processado via chave {self.chave_pix}.")

class PagamentoCartao(Pagamento):
    def __init__(self, id_pagamento: int, valor_total: float, id_agendamento: int, numero_cartao: str = "", final_cartao: str = "", status: str = "Pendente"):
        super().__init__(id_pagamento, valor_total, id_agendamento, status)
        self.numero_cartao = numero_cartao
        self.final_cartao = final_cartao

    @staticmethod
    def validar_luhn(numero: str) -> bool:
        numero = numero.replace(" ", "").replace("-", "")
        if not numero.isdigit() or len(numero) < 13:
            return False
        soma = 0
        alternar = False
        for digito in reversed(numero):
            d = int(digito)
            if alternar:
                d *= 2
                if d > 9:
                    d -= 9
            soma += d
            alternar = not alternar
        return soma % 10 == 0

    def processar(self):
        if self.valor_total <= 0:
            raise ValueError("Valor do pagamento invalido.")
        if self.numero_cartao:
            if not self.validar_luhn(self.numero_cartao):
                self.status = 'Cancelado'
                raise ValueError("Numero de cartao invalido.")
            self.final_cartao = self.numero_cartao.replace(" ", "")[-4:]
        self.status = 'Pago'
        print(f"Pagamento Cartao processado no final {self.final_cartao}.")