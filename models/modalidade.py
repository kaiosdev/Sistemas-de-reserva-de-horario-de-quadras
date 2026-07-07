class Modalidade:
    """Modelo de domínio da tabela Modalidade (esporte/pratica da quadra)."""

    def __init__(self, id_modalidade: int, nome: str):
        self.id_modalidade = id_modalidade
        self.nome = nome

    def __str__(self):
        return f"Modalidade(ID: {self.id_modalidade} | {self.nome})"

    def __repr__(self):
        return f"Modalidade(id_modalidade={self.id_modalidade}, nome='{self.nome}')"
