from database.connection import get_connection
from models.modalidade import Modalidade

class ModalidadeRepository:
    def inserir(self, modalidade: Modalidade):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = "INSERT INTO Modalidade (nome) VALUES (%s) RETURNING id_modalidade"
                cursor.execute(sql, (modalidade.nome,))
                id_gerado = cursor.fetchone()[0]
                modalidade.id_modalidade = id_gerado
                conexao.commit()
                return id_gerado
            finally:
                cursor.close()
                conexao.close()

    def listar_todos(self):
        conexao = get_connection()
        modalidades = []
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = "SELECT id_modalidade, nome FROM Modalidade ORDER BY id_modalidade"
                cursor.execute(sql)
                for linha in cursor.fetchall():
                    modalidades.append(Modalidade(linha[0], linha[1]))
            finally:
                cursor.close()
                conexao.close()
        return modalidades

    def atualizar(self, id_modalidade: int, nome: str):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = "UPDATE Modalidade SET nome=%s WHERE id_modalidade=%s"
                cursor.execute(sql, (nome, id_modalidade))
                conexao.commit()
            finally:
                cursor.close()
                conexao.close()

    def excluir(self, id_modalidade: int):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = "DELETE FROM Modalidade WHERE id_modalidade = %s"
                cursor.execute(sql, (id_modalidade,))
                conexao.commit()
            finally:
                cursor.close()
                conexao.close()
