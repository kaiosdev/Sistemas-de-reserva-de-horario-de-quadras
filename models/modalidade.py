class Modalidade:
    def __init__(self, id_modalidade: int, nome: str):
        self.id_modalidade = id_modalidade
        self.nome = nome

    def __str__(self):
        return f"Modalidade: {self.nome}"

    def __repr__(self):
        return f"Modalidade(id_modalidade={self.id_modalidade}, nome='{self.nome}')"

    def __eq__(self, outro):
        if not isinstance(outro, Modalidade):
            return False
        return self.id_modalidade == outro.id_modalidade
