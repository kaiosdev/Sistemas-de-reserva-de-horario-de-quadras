from repositories.pagamento_repository import PagamentoRepository
from repositories.agendamento_repository import AgendamentoRepository
from models.pagamento import factory_pagamento, Pagamento


class PagamentoService:
    """Regras de negocio da entidade Pagamento.

    DEMONSTRACAO DE POLIMORFISMO:
        O metodo processar() usa a factory para instanciar a subclasse correta
        de Pagamento (PagamentoPix ou PagamentoCartao) e chama .processar().
        Como cada subclasse implementa processar() de forma diferente, o mesmo
        chamada de metodo produz comportamentos distintos - polimorfismo real.
    """

    FORMAS_VALIDAS = {"PIX", "CARTAO"}
    STATUS_VALIDOS = {"Pendente", "Pago", "Cancelado"}

    def __init__(self):
        self.repository = PagamentoRepository()
        self.agendamento_repo = AgendamentoRepository()

    def listar_todos(self):
        return self.repository.listar_todos()

    def processar(self, id_agendamento, valor_total=None, forma_pagamento="PIX", status=None,
                  chave_pix="", final_cartao=""):
        # --- Agendamento existe? ---
        try:
            id_agendamento = int(id_agendamento)
        except (TypeError, ValueError):
            raise ValueError("id_agendamento deve ser um numero valido.")

        agendamento = self.agendamento_repo.buscar_por_id(id_agendamento)
        if not agendamento:
            raise ValueError("Agendamento nao encontrado.")

        # --- Forma de pagamento ---
        forma = (forma_pagamento or "PIX").upper()
        if forma not in self.FORMAS_VALIDAS:
            raise ValueError("Forma de pagamento deve ser PIX ou CARTAO.")

        # --- Valor (default: valor_hora da quadra) ---
        if valor_total in (None, ""):
            valor = agendamento["valor_hora"]
        else:
            try:
                valor = float(valor_total)
            except (TypeError, ValueError):
                raise ValueError("O valor deve ser numerico.")
        if valor <= 0:
            raise ValueError("O valor do pagamento deve ser maior que zero.")

        # ===================================================================
        # POLIMORFISMO: factory instancia a subclasse correta e chamamos
        # .processar() - cada subclasse tem sua propria implementacao.
        # ===================================================================
        pagamento = factory_pagamento(
            forma_pagamento=forma,
            id_pagamento=0,
            valor_total=valor,
            id_agendamento=id_agendamento,
            chave_pix=chave_pix,
            final_cartao=final_cartao,
        )
        status_resultante = pagamento.processar()  # polimorfico: PIX vs Cartao

        # Se o caller forcou um status (ex.: edicao manual), respeita.
        if status is not None:
            status = (status or "").strip()
            if status not in self.STATUS_VALIDOS:
                raise ValueError("Status invalido. Use: Pendente, Pago ou Cancelado.")
            status_resultante = status

        id_pagamento = self.repository.inserir(valor, forma, id_agendamento, status_resultante)
        return id_pagamento

    def atualizar(self, id_pagamento, valor_total=None, forma_pagamento=None, status=None):
        if forma_pagamento is not None:
            forma = (forma_pagamento or "").upper()
            if forma not in self.FORMAS_VALIDAS:
                raise ValueError("Forma de pagamento deve ser PIX ou CARTAO.")
        else:
            forma = None

        if status is not None:
            status = (status or "").strip()
            if status not in self.STATUS_VALIDOS:
                raise ValueError("Status invalido. Use: Pendente, Pago ou Cancelado.")

        if valor_total is not None and valor_total != "":
            try:
                valor = float(valor_total)
            except (TypeError, ValueError):
                raise ValueError("O valor deve ser numerico.")
            if valor <= 0:
                raise ValueError("O valor do pagamento deve ser maior que zero.")
        else:
            valor = None

        atual = None
        for p in self.repository.listar_todos():
            if p["id_pagamento"] == int(id_pagamento):
                atual = p
                break
        if not atual:
            raise ValueError("Pagamento nao encontrado.")

        return self.repository.atualizar(
            int(id_pagamento),
            valor if valor is not None else atual["valor_total"],
            forma if forma is not None else atual["forma_pagamento"],
            status if status is not None else atual["status"],
        )

    def atualizar_status(self, id_pagamento, novo_status):
        if novo_status not in self.STATUS_VALIDOS:
            raise ValueError("Status invalido. Use: Pendente, Pago ou Cancelado.")
        self.repository.atualizar_status(id_pagamento, novo_status)

    def excluir(self, id_pagamento: int):
        return self.repository.deletar(id_pagamento)
