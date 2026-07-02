from models.espaco import Espaco
from repositories.espaco_repository import EspacoRepository

class EspacoService:
    def __init__(self):
        self.repository = EspacoRepository()

    def cadastrar_espaco(self, nome, descricao, tamanho, valor):
        val_float = float(valor.replace(",", "."))
        espaco = Espaco(0, nome, descricao, tamanho, val_float)
        self.repository.inserir(espaco)

    def listar_espacos(self):
        return self.repository.listar_todos()

    def excluir_espaco(self, id_espaco: int):
        self.repository.excluir(id_espaco)