from database.connection import get_connection
from models.modalidade import Modalidade


class ModalidadeRepository:
    def listar_todos(self):
        conexao = get_connection()
        modalidades = []
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("SELECT id_modalidade, nome FROM Modalidade ORDER BY nome")
                for linha in cursor.fetchall():
                    modalidades.append(Modalidade(linha[0], linha[1]))
            finally:
                cursor.close()
                conexao.close()
        return modalidades
