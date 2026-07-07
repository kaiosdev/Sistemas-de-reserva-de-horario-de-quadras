class Espaco:
    def __init__(self, id_espaco: int, nome: str, descricao: str, tamanho_quadra: str, valor_hora: float, id_modalidade: int = 1, modalidade_nome: str = None):
        self.id_espaco = id_espaco
        self.nome = nome
        self.descricao = descricao
        self.tamanho_quadra = tamanho_quadra
        self.valor_hora = valor_hora
        self.id_modalidade = id_modalidade
        self.modalidade_nome = modalidade_nome  # preenchido via JOIN com Modalidade

    def __str__(self):
        mod = f" [{self.modalidade_nome}]" if self.modalidade_nome else ""
        return f"Espaco: {self.nome}{mod} ({self.tamanho_quadra}) - {self.descricao}"