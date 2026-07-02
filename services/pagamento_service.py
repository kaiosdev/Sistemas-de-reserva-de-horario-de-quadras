from models.pagamento import PagamentoPix, PagamentoCartao
from repositories.pagamento_repository import PagamentoRepository

class PagamentoService:
    def __init__(self):
        self.repository = PagamentoRepository()

    def processar_pagamento(self, forma: str, valor_total: float, id_agendamento: int, numero_cartao: str = ""):
        if forma == "PIX":
            pagamento = PagamentoPix(0, valor_total, id_agendamento)
        else:
            pagamento = PagamentoCartao(0, valor_total, id_agendamento, numero_cartao=numero_cartao)
            
        # O Polimorfismo ocorre nesta linha:
        pagamento.processar() 
        
        chave = getattr(pagamento, "chave_pix", "")
        final_c = getattr(pagamento, "final_cartao", "")
        
        self.repository.inserir(id_agendamento, valor_total, forma, pagamento.status, chave, final_c)
        return pagamento

    def listar_pagamentos(self):
        return self.repository.listar_todos()