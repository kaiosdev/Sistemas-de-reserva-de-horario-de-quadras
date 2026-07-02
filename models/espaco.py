class Espaco:
    def __init__(self, id_espaco: int, nome: str, descricao: str, tamanho_quadra: str, valor_hora: float):
        self.id_espaco = id_espaco
        self.nome = nome
        self.descricao = descricao
        self.tamanho_quadra = tamanho_quadra
        self.valor_hora = valor_hora

    def __str__(self):
        return f"Espaco: {self.nome} ({self.tamanho_quadra}) - {self.descricao}"

    def __repr__(self):
        return f"Espaco(id_espaco={self.id_espaco}, nome='{self.nome}', valor_hora={self.valor_hora})"