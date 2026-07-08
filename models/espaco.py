class Espaco:
    def __init__(self, id_espaco: int, nome: str, descricao: str, tamanho_quadra: str, valor_hora: float, id_modalidade: int, nome_modalidade: str = ""):
        self.id_espaco = id_espaco
        self.nome = nome
        self.descricao = descricao
        self.tamanho_quadra = tamanho_quadra
        self.valor_hora = valor_hora
        self.id_modalidade = id_modalidade
        self.nome_modalidade = nome_modalidade

    def __str__(self):
        mod_info = self.nome_modalidade if self.nome_modalidade else f"Modalidade {self.id_modalidade}"
        return f"Espaco: {self.nome} ({self.tamanho_quadra}) | {mod_info}"

    def __repr__(self):
        return f"Espaco(id_espaco={self.id_espaco}, nome='{self.nome}', id_modalidade={self.id_modalidade})"