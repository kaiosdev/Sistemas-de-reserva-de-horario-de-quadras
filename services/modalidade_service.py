from models.modalidade import Modalidade
from repositories.modalidade_repository import ModalidadeRepository

class ModalidadeService:
    def __init__(self):
        self.repository = ModalidadeRepository()

    def cadastrar_modalidade(self, nome: str):
        if not nome or not nome.strip():
            raise ValueError("O nome da modalidade e obrigatorio.")
        modalidade = Modalidade(0, nome.strip())
        return self.repository.inserir(modalidade)

    def atualizar_modalidade(self, id_modalidade: int, nome: str):
        if not nome or not nome.strip():
            raise ValueError("O nome da modalidade e obrigatorio.")
        self.repository.atualizar(id_modalidade, nome.strip())

    def listar_modalidades(self):
        return self.repository.listar_todos()

    def excluir_modalidade(self, id_modalidade: int):
        self.repository.excluir(id_modalidade)
