from models.espaco import Espaco
from repositories.espaco_repository import EspacoRepository

class EspacoService:
    def __init__(self):
        self.repository = EspacoRepository()

    def cadastrar_espaco(self, nome, descricao, tamanho, valor):
        espaco = Espaco(0, nome, descricao, tamanho, float(valor.replace(",", ".")))
        self.repository.inserir(espaco)

    def atualizar_espaco(self, id_espaco, nome, descricao, tamanho, valor):
        self.repository.atualizar(id_espaco, nome, descricao, tamanho, float(valor.replace(",", ".")))

    def listar_espacos(self):
        return self.repository.listar_todos()

    def excluir_espaco(self, id_espaco: int):
        self.repository.excluir(id_espaco)