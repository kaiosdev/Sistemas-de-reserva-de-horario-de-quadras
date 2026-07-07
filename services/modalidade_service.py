from database.connection import get_connection
from repositories.modalidade_repository import ModalidadeRepository
from models.modalidade import Modalidade


class ModalidadeService:
    """Regras de negocio da entidade Modalidade.

    Modalidade e uma categoria esportiva (ex.: Futsal, Basquete) que classifica
    os espacos/quadras. A modalidade padrao ('Geral') e criada pelo schema.sql.
    """

    def __init__(self):
        self.repository = ModalidadeRepository()

    def listar_todos(self):
        return self.repository.listar_todos()

    def cadastrar(self, nome: str):
        nome = (nome or "").strip()
        if not nome:
            raise ValueError("O nome da modalidade e obrigatorio.")

        conexao = get_connection()
        if not conexao:
            raise RuntimeError("Sem conexao com o banco.")
        try:
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO Modalidade (nome) VALUES (%s) RETURNING id_modalidade", (nome,))
            novo_id = cursor.fetchone()[0]
            conexao.commit()
            return Modalidade(novo_id, nome)
        finally:
            cursor.close()
            conexao.close()
