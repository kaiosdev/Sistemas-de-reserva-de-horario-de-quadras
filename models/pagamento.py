from abc import ABC, abstractmethod


class Pagamento(ABC):
    """Classe abstrata base da hierarquia de Pagamento.

    Contrato definido (por que ABC + @abstractmethod):
        - Todo Pagamento DEVE saber se processar (processar).
        - Cada subclasse concretiza a logica conforme a forma (PIX, Cartao).
        - O banco guarda apenas a coluna 'forma_pagamento', mas no dominio
          usamos polimorfismo para que o mesmo metodo processar() se comporte
          de forma diferente em PagamentoPix e PagamentoCartao.
    """

    def __init__(self, id_pagamento: int, valor_total: float, id_agendamento: int, status: str = "Pendente"):
        self.id_pagamento = id_pagamento
        self.valor_total = valor_total
        self.id_agendamento = id_agendamento
        self.status = status

    @abstractmethod
    def processar(self) -> str:
        """Processa o pagamento e retorna o status final ('Pago' ou 'Cancelado')."""
        pass

    @property
    def forma(self) -> str:
        return self.__class__.__name__

    def __str__(self):
        return f"Pagamento #{self.id_pagamento} | R$ {self.valor_total:.2f} | {self.forma} | {self.status}"


class PagamentoPix(Pagamento):
    """Pagamento via PIX - confirmacao automatica (sem intermediador)."""

    def __init__(self, id_pagamento, valor_total, id_agendamento, chave_pix: str = "", status="Pendente"):
        super().__init__(id_pagamento, valor_total, id_agendamento, status)
        self.chave_pix = chave_pix or "nao-informada"

    def processar(self) -> str:
        # Regra de negocio do PIX: confirmado imediatamente apos gerar QR
        self.status = "Pago"
        return self.status

    def __str__(self):
        return f"PagamentoPIX #{self.id_pagamento} | R$ {self.valor_total:.2f} | chave {self.chave_pix} | {self.status}"


class PagamentoCartao(Pagamento):
    """Pagamento via Cartao - pode falhar por validacao de limite."""

    def __init__(self, id_pagamento, valor_total, id_agendamento, final_cartao: str = "0000", status="Pendente"):
        super().__init__(id_pagamento, valor_total, id_agendamento, status)
        self.final_cartao = final_cartao or "0000"

    def processar(self) -> str:
        # Regra de negocio do Cartao: valores acima de 1000 sao recusados
        # (regra simplificada para demonstrar comportamento polimorfico diferente do PIX)
        if self.valor_total > 1000:
            self.status = "Cancelado"
        else:
            self.status = "Pago"
        return self.status

    def __str__(self):
        return f"PagamentoCartao #{self.id_pagamento} | R$ {self.valor_total:.2f} | final {self.final_cartao} | {self.status}"


def factory_pagamento(forma_pagamento: str, id_pagamento: int, valor_total: float, id_agendamento: int, status="Pendente", **extras) -> Pagamento:
    """Factory Method que instancia a subclasse correta de Pagamento.

    Centraliza a decisao de qual subclasse criar e e o ponto de entrada
    para o polimorfismo: quem chama recebe um Pagamento e so precisa
    invocar .processar() - nao precisa saber se e PIX ou Cartao.
    """
    forma = (forma_pagamento or "").upper()
    if forma == "CARTAO":
        return PagamentoCartao(
            id_pagamento, valor_total, id_agendamento,
            final_cartao=extras.get("final_cartao", "0000"), status=status,
        )
    # default: PIX
    return PagamentoPix(
        id_pagamento, valor_total, id_agendamento,
        chave_pix=extras.get("chave_pix", ""), status=status,
    )
